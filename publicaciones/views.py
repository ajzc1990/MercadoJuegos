from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Producto, Pregunta
from .forms import ProductoForm, PreguntaForm, RespuestaForm

def detalle_producto(request, pk):
    """Página de detalle del producto con sección de preguntas y respuestas"""
    producto = get_object_or_404(Producto, pk=pk)
    preguntas = producto.preguntas.all()
    form_pregunta = PreguntaForm()

    if request.method == 'POST' and 'btn_pregunta' in request.POST:
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión para hacer una pregunta.')
            return redirect('cuentas:login')
        
        form_pregunta = PreguntaForm(request.POST)
        if form_pregunta.is_valid():
            nueva_pregunta = form_pregunta.save(commit=False)
            nueva_pregunta.producto = producto
            nueva_pregunta.usuario = request.user
            nueva_pregunta.save()
            messages.success(request, '¡Tu pregunta fue enviada al vendedor!')
            return redirect('publicaciones:detalle', pk=producto.pk)

    contexto = {
        'producto': producto,
        'preguntas': preguntas,
        'form_pregunta': form_pregunta,
    }
    return render(request, 'publicaciones/detalle_producto.html', contexto)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def crear_producto(request):
    """Permite a los usuarios publicar un nuevo juego o consola"""
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user
            producto.save()
            messages.success(request, '¡Tu publicación se ha creado con éxito!')
            return redirect('publicaciones:detalle', pk=producto.pk)
    else:
        form = ProductoForm()

    return render(request, 'publicaciones/crear_producto.html', {'form': form})


@login_required
def responder_pregunta(request, pregunta_id):
    """Permite al vendedor responder preguntas realizadas en sus productos"""
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)

    # Validar que solo el vendedor del producto pueda responder
    if request.user != pregunta.producto.vendedor:
        messages.error(request, 'No tienes permisos para responder esta pregunta.')
        return redirect('publicaciones:detalle', pk=pregunta.producto.pk)

    if request.method == 'POST':
        form = RespuestaForm(request.POST, instance=pregunta)
        if form.is_valid():
            pregunta_editada = form.save(commit=False)
            pregunta_editada.respondido_el = timezone.now()
            pregunta_editada.save()
            messages.success(request, 'Respuesta publicada correctamente.')

    return redirect('publicaciones:detalle', pk=pregunta.producto.pk)