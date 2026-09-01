# ventas/urls.py
from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('carrito/', views.ver_carrito, name='carrito'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar'),
    path('eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar'),
    path('checkout/', views.checkout, name='checkout'),
    path('mis-compras/', views.mis_compras, name='mis_compras'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('pago/exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago/fallido/', views.pago_fallido, name='pago_fallido'),
    path('pago/pendiente/', views.pago_pendiente, name='pago_pendiente'),
    path('webhook/mercadopago/', views.webhook_mercadopago, name='webhook_mp'),
]