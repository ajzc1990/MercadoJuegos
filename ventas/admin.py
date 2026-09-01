from django.contrib import admin
from .models import Pedido, DetallePedido

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ('producto', 'precio_unitario', 'cantidad')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'comprador', 'total', 'estado', 'creado_el')
    list_filter = ('estado', 'creado_el')
    search_fields = ('comprador__username', 'direccion_envio')
    inlines = [DetallePedidoInline]