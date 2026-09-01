from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from publicaciones.models import Producto

from .models import Perfil
from .forms import RegistroUsuarioForm, UserUpdateForm, PerfilUpdateForm


def registro_view(request):
    """Registro de nuevos usuarios"""
    if request.user.is_authenticated:
        return redirect('home:inicio')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f'¡Bienvenido a Mercado Juegos, {usuario.username}!')
            return redirect('home:inicio')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'cuentas/registro.html', {'form': form})


def login_view(request):
    """Inicio de sesión de usuarios"""
    if request.user.is_authenticated:
        return redirect('home:inicio')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            usuario = authenticate(username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                messages.info(request, f'Has iniciado sesión como {username}.')
                return redirect('home:inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()

    return render(request, 'cuentas/login.html', {'form': form})


def logout_view(request):
    """Cierre de sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('home:inicio')


@login_required
def perfil_view(request):
    """Ver y editar el perfil del usuario autenticado"""
    # Garantiza obtener o crear el perfil asignado al atributo `usuario`
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = PerfilUpdateForm(request.POST, instance=perfil)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado con éxito!')
            return redirect('cuentas:perfil')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = PerfilUpdateForm(instance=perfil)

    contexto = {
        'u_form': u_form,
        'p_form': p_form,
        'perfil': perfil,
    }
    return render(request, 'cuentas/perfil.html', contexto)

def despedida(request):
    """Página introductoria que se muestra inmediatamente después de cerrar sesión."""
    # Traemos los 4 productos más recientes con stock disponible para la vidriera
    juegos_destacados = Producto.objects.filter(stock__gt=0).order_by('-creado_el')[:4]
    
    return render(request, 'cuentas/despedida.html', {
        'juegos_destacados': juegos_destacados
    })