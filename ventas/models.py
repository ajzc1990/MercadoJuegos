from django.db import models
from django.contrib.auth.models import User
from publicaciones.models import Producto

class Pedido(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente de pago'),
        ('pagado', 'Pagado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    )

    comprador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compras', verbose_name="Comprador")
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total ($)")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', verbose_name="Estado del Pedido")
    direccion_envio = models.CharField(max_length=255, verbose_name="Dirección de Envío")
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-creado_el']

    def __str__(self):
        return f"Pedido #{self.id} - {self.comprador.username}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles', verbose_name="Pedido")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name="Producto")
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio Unitario ($)")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")

    class Meta:
        verbose_name = "Detalle del Pedido"
        verbose_name_plural = "Detalles de Pedidos"

    def __str__(self):
        return f"{self.cantidad}x {self.producto.titulo}"

    def get_subtotal(self):
        return self.precio_unitario * self.cantidad

# ventas/models.py (al final del archivo)
from publicaciones.models import ClaveProducto

class EntregaClave(models.Model):
    detalle_pedido = models.ForeignKey(DetallePedido, on_delete=models.CASCADE, related_name='claves_entregadas')
    clave_producto = models.OneToOneField(ClaveProducto, on_delete=models.PROTECT, verbose_name="Clave Asignada")
    fecha_entrega = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entrega #{self.id} -> {self.clave_producto.clave}"