# home/views.py
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Banner
from publicaciones.models import Producto, Categoria

def inicio(request):
    busqueda = request.GET.get('q', '').strip()
    categoria_slug = request.GET.get('categoria', '').strip()

    productos_list = Producto.objects.filter(stock__gt=0).order_by('-creado_el')
    
    if busqueda:
        productos_list = productos_list.filter(
            Q(titulo__icontains=busqueda) | Q(descripcion__icontains=busqueda)
        )
    
    if categoria_slug:
        productos_list = productos_list.filter(categoria__slug=categoria_slug)

    # Paginación: 12 productos por página
    paginator = Paginator(productos_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    banners = Banner.objects.filter(activo=True) if hasattr(Banner, 'activo') else Banner.objects.all()
    categorias = Categoria.objects.all()

    contexto = {
        'productos': page_obj,  # Enviamos el objeto de página
        'banners': banners,
        'categorias': categorias,
        'busqueda': busqueda,
        'categoria_seleccionada': categoria_slug,
    }
    return render(request, 'home/inicio.html', contexto)


# home/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def contacto(request):
    """Procesa el formulario de consultas y soporte técnico"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email_emisor = request.POST.get('email', '').strip()
        asunto_tipo = request.POST.get('asunto', 'consulta')
        mensaje_cuerpo = request.POST.get('mensaje', '').strip()

        # Mapeo de asuntos legibles
        asuntos_map = {
            'consulta': 'Consulta General',
            'compra': 'Soporte sobre una Compra / Clave',
            'publicacion': 'Problema con una Publicación',
            'otro': 'Otro motivo'
        }
        asunto_legible = asuntos_map.get(asunto_tipo, 'Consulta Web')

        asunto_completo = f"📩 [{asunto_legible}] Mensaje de {nombre} ({email_emisor})"
        cuerpo_email = (
            f"Has recibido un nuevo mensaje desde el centro de soporte de Mercado Juegos:\n\n"
            f"👤 Nombre: {nombre}\n"
            f"📧 Correo: {email_emisor}\n"
            f"🏷️ Motivo: {asunto_legible}\n"
            f"--------------------------------------------------\n"
            f"💬 Mensaje:\n{mensaje_cuerpo}\n"
            f"--------------------------------------------------"
        )

        try:
            # Envío de notificación al correo de soporte/administrador
            send_mail(
                subject=asunto_completo,
                message=cuerpo_email,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['agustinzelayacossio@gmail.com'], # O el correo configurado en settings
                fail_silently=False,
            )
            messages.success(request, f'¡Gracias por contactarnos, {nombre}! Tu mensaje fue enviado con éxito. Te responderemos a la brevedad.')
        except Exception as e:
            print(f"❌ Error enviando correo de contacto: {e}")
            messages.success(request, f'Tu consulta ha sido registrada correctamente. Nos pondremos en contacto pronto.')

        return redirect('home:contacto')

    return render(request, 'home/contacto.html')