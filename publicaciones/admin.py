from django.contrib import admin
from .models import Categoria, Producto, Pregunta, ClaveProducto
from entregas.models import ContenidoDigital


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre',)


class ContenidoDigitalInline(admin.StackedInline):
    model = ContenidoDigital
    can_delete = False
    verbose_name = "Contenido Digital del Juego"
    verbose_name_plural = "Contenido Digital del Juego"
    extra = 0


class ClaveProductoInline(admin.TabularInline):
    """Permite ver, agregar y editar las claves directamente dentro de la ficha del juego"""
    model = ClaveProducto
    extra = 1
    fields = ('clave', 'disponible', 'fecha_agregada')
    readonly_fields = ('fecha_agregada',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'vendedor', 'categoria', 'precio', 'stock', 'condicion', 'creado_el')
    list_filter = ('categoria', 'condicion', 'creado_el')
    search_fields = ('titulo', 'descripcion', 'vendedor__username')
    list_editable = ('precio', 'stock')
    inlines = [ContenidoDigitalInline, ClaveProductoInline]


@admin.register(ClaveProducto)
class ClaveProductoAdmin(admin.ModelAdmin):
    """Panel individual para auditar, buscar y filtrar claves de activación"""
    list_display = ('producto', 'clave', 'disponible', 'fecha_agregada')
    list_filter = ('disponible', 'fecha_agregada', 'producto__categoria')
    search_fields = ('clave', 'producto__titulo')
    list_editable = ('disponible',)


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'usuario', 'creado_el', 'texto_respuesta')
    search_fields = ('texto_pregunta', 'texto_respuesta', 'producto__titulo', 'usuario__username')
    list_filter = ('creado_el',)