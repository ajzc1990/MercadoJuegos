# entregas/services.py
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from publicaciones.models import ClaveProducto
from ventas.models import EntregaClave


def despachar_producto_digital(pedido):
    """
    Procesa un pedido pagado:
    1. Asigna claves digitales disponibles de cada producto si no fueron asignadas.
    2. Recopila claves y contenido digital (.zip / enlaces).
    3. Envía un correo HTML profesional con las claves de activación.
    """
    comprador = pedido.comprador
    email_destino = comprador.email or 'agustinzelayacossio@gmail.com'
    asunto = f'🎮 ¡Tus claves y juegos están listos! - Orden #{pedido.id}'

    items_digitales = []
    archivos_para_adjuntar = []

    for detalle in pedido.detalles.all():
        producto = detalle.producto

        # 1. Asignar claves si aún no tiene claves vinculadas
        claves_actuales = detalle.claves_entregadas.all()
        if not claves_actuales.exists():
            claves_disponibles = ClaveProducto.objects.filter(
                producto=producto, disponible=True
            )[:detalle.cantidad]

            for c in claves_disponibles:
                c.disponible = False
                c.save()
                EntregaClave.objects.create(detalle_pedido=detalle, clave_producto=c)

            # Actualizar stock del producto
            producto.stock = producto.claves.filter(disponible=True).count()
            producto.save()

        # 2. Recopilar claves asignadas
        claves_list = [
            entrega.clave_producto.clave
            for entrega in detalle.claves_entregadas.all()
        ]

        # 3. Contenido digital opcional (.zip / enlaces)
        contenido = getattr(producto, 'contenido_digital', None)
        if contenido and getattr(contenido, 'archivo_zip', None):
            try:
                if contenido.archivo_zip.storage.exists(contenido.archivo_zip.name):
                    archivos_para_adjuntar.append(contenido.archivo_zip.path)
            except Exception as e:
                print(f"⚠️ Error al verificar archivo zip para {producto.titulo}: {e}")

        items_digitales.append({
            'producto': producto,
            'cantidad': detalle.cantidad,
            'precio_unitario': detalle.precio_unitario,
            'claves': claves_list,
            'contenido': contenido,
        })

    # Contexto para el template de correo
    context = {
        'pedido': pedido,
        'comprador': comprador,
        'items_digitales': items_digitales,
    }

    # Renderizar el HTML y generar la versión en texto plano como respaldo
    html_content = render_to_string('entregas/emails/entrega_juego.html', context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=asunto,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email_destino],
    )
    email.attach_alternative(html_content, "text/html")

    # Adjuntar archivos físicos si existen
    for ruta_archivo in archivos_para_adjuntar:
        try:
            email.attach_file(ruta_archivo)
        except Exception as e:
            print(f"⚠️ No se pudo adjuntar {ruta_archivo}: {e}")

    # Enviar correo
    email.send(fail_silently=False)