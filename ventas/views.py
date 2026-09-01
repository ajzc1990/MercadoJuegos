import json
import mercadopago
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from entregas.services import despachar_producto_digital
from publicaciones.models import Producto

from .cart import Carrito
from .models import DetallePedido, Pedido


def ver_carrito(request):
    """Vista general del carrito de compras"""
    carrito = Carrito(request)
    return render(request, 'ventas/carrito.html', {'carrito': carrito})


def agregar_al_carrito(request, producto_id):
    """Agrega, incrementa o decrementa la cantidad de un producto en el carrito"""
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)

    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except ValueError:
        cantidad = 1

    if cantidad < 0:
        if hasattr(carrito, 'restar'):
            carrito.restar(producto)
        elif hasattr(carrito, 'agregar'):
            carrito.agregar(producto=producto, cantidad=cantidad)
        messages.info(
            request, f'Se actualizó la cantidad de "{producto.titulo}".'
        )
        return redirect('ventas:carrito')

    try:
        exito = carrito.agregar(producto=producto, cantidad=cantidad)
    except TypeError:
        exito = carrito.agregar(producto=producto)

    if exito is False:
        messages.error(
            request,
            f'No se pudo agregar "{producto.titulo}". Stock insuficiente (Disponibles: {producto.stock}).',
        )
    else:
        messages.success(
            request, f'"{producto.titulo}" se actualizó en el carrito.'
        )

    return redirect('ventas:carrito')


def eliminar_del_carrito(request, producto_id):
    """Elimina un producto del carrito"""
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.eliminar(producto)
    messages.info(request, f'"{producto.titulo}" fue quitado del carrito.')
    return redirect('ventas:carrito')


@login_required
def checkout(request):
    """Procesar la compra y generar la preferencia de pago en Mercado Pago"""
    carrito = Carrito(request)
    if len(carrito) == 0:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('home:inicio')

    perfil = getattr(request.user, 'perfil', None)

    if request.method == 'POST':
        direccion = request.POST.get(
            'direccion', getattr(perfil, 'direccion', 'Entrega Digital (Email)')
        )
        ciudad = request.POST.get(
            'ciudad', getattr(perfil, 'ciudad', 'Digital')
        )

        # 1. Crear el Pedido en estado 'pendiente'
        pedido = Pedido.objects.create(
            comprador=request.user,
            total=carrito.get_total(),
            estado='pendiente',
            direccion_envio=direccion,
            ciudad=ciudad,
        )

        # 2. Crear los Detalles del Pedido y preparar items para Mercado Pago
        items_mp = []
        for item in carrito:
            producto = item['producto']
            cantidad = item['cantidad']
            precio = float(item['precio'])

            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                precio_unitario=precio,
                cantidad=cantidad,
            )

            items_mp.append({
                'title': producto.titulo,
                'quantity': cantidad,
                'unit_price': precio,
                'currency_id': 'ARS',
            })

        # 3. Inicializar el SDK de Mercado Pago
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

        # 4. Configurar la preferencia de pago
        preference_data = {
            'items': items_mp,
            'payer': {
                'name': request.user.first_name or request.user.username,
                'email': request.user.email or 'cliente@email.com',
            },
            'back_urls': {
                'success': request.build_absolute_uri(
                    reverse('ventas:pago_exitoso')
                ),
                'failure': request.build_absolute_uri(
                    reverse('ventas:pago_fallido')
                ),
                'pending': request.build_absolute_uri(
                    reverse('ventas:pago_pendiente')
                ),
            },
            'external_reference': str(pedido.id),
        }

        preference_response = sdk.preference().create(preference_data)
        response = preference_response.get('response', {})

        init_point = response.get('sandbox_init_point') or response.get('init_point')

        if init_point:
            return redirect(init_point)
        else:
            print('❌ Error de Mercado Pago:', preference_response)
            messages.error(
                request,
                'No se pudo conectar con Mercado Pago. Verifica tus credenciales de Access Token.',
            )
            return redirect('ventas:carrito')

    contexto = {'carrito': carrito, 'perfil': perfil}
    return render(request, 'ventas/checkout.html', contexto)


@login_required
def mis_compras(request):
    """Listado del historial de compras del usuario autenticado"""
    pedidos = Pedido.objects.filter(comprador=request.user).order_by('-creado_el')
    return render(request, 'ventas/mis_compras.html', {'pedidos': pedidos})


@login_required
def detalle_pedido(request, pedido_id):
    """Muestra los juegos comprados en un pedido específico"""
    pedido = get_object_or_404(Pedido, id=pedido_id, comprador=request.user)
    return render(request, 'ventas/detalle_pedido.html', {'pedido': pedido})


def pago_exitoso(request):
    """Procesa el retorno exitoso desde Mercado Pago y redirige al detalle del pedido"""
    status = request.GET.get('status')
    pedido_id = request.GET.get('external_reference')

    if status == 'approved' and pedido_id:
        pedido = get_object_or_404(Pedido, id=pedido_id)

        # Evitar duplicar procesos si ya estaba pagado
        if pedido.estado != 'pagado':
            # 1. Actualizar estado
            pedido.estado = 'pagado'
            pedido.save()

            # 2. Descontar Stock
            for detalle in pedido.detalles.all():
                detalle.producto.stock -= detalle.cantidad
                detalle.producto.save()

            # 3. Despachar claves por email
            try:
                despachar_producto_digital(pedido)
            except Exception as e:
                print(f'❌ Error enviando mail: {e}')

            # 4. Vaciar Carrito
            carrito = Carrito(request)
            carrito.limpiar()

            messages.success(
                request,
                '¡Pago confirmado con éxito! 🎉 Ya podés acceder a tus claves digitales a continuación.',
            )
        else:
            messages.info(
                request,
                f'La orden #{pedido.id} ya se encuentra registrada como pagada.',
            )

        return redirect('ventas:detalle_pedido', pedido_id=pedido.id)

    messages.warning(
        request,
        'No se pudo verificar la transacción o el pago no fue aprobado.',
    )
    return redirect('ventas:mis_compras')


def pago_fallido(request):
    """Procesa un pago rechazado o cancelado"""
    messages.error(
        request,
        'Hubo un problema o cancelaste la operación en Mercado Pago. Intenta nuevamente.',
    )
    return redirect('ventas:carrito')


def pago_pendiente(request):
    """Procesa pagos en revisión o en medio de pago presencial"""
    messages.info(
        request, 'Tu pago se encuentra pendiente de acreditación.'
    )
    return redirect('ventas:mis_compras')


@csrf_exempt
def webhook_mercadopago(request):
    """Endpoint receptor de notificaciones IPN/Webhook de Mercado Pago"""
    if request.method == 'POST':
        topic = request.GET.get('topic') or request.GET.get('type')
        id_notificacion = request.GET.get('id') or request.GET.get('data.id')

        if not id_notificacion and request.body:
            try:
                data = json.loads(request.body.decode('utf-8'))
                topic = data.get('type', topic)
                id_notificacion = data.get('data', {}).get('id', id_notificacion)
            except Exception:
                pass

        if topic == 'payment' and id_notificacion:
            sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
            payment_info = sdk.payment().get(id_notificacion)
            
            if payment_info.get('status') == 200:
                payment_data = payment_info['response']
                status = payment_data.get('status')
                pedido_id = payment_data.get('external_reference')

                if status == 'approved' and pedido_id:
                    try:
                        pedido = Pedido.objects.get(id=pedido_id)
                        if pedido.estado != 'pagado':
                            pedido.estado = 'pagado'
                            pedido.save()

                            for detalle in pedido.detalles.all():
                                detalle.producto.stock -= detalle.cantidad
                                detalle.producto.save()

                            try:
                                despachar_producto_digital(pedido)
                            except Exception as e:
                                print(f"❌ Error en despacho webhook: {e}")

                    except Pedido.DoesNotExist:
                        pass

        return HttpResponse(status=200)

    return HttpResponse(status=400)