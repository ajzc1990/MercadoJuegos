from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Categoría")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    OPCIONES_CONDICION = (
        ('nuevo', 'Nuevo'),
        ('usado', 'Usado'),
    )

    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productos', verbose_name="Vendedor")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos', verbose_name="Categoría")
    titulo = models.CharField(max_length=200, verbose_name="Título del Producto")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    precio = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio ($)")
    stock = models.PositiveIntegerField(default=1, verbose_name="Stock disponible")
    condicion = models.CharField(max_length=10, choices=OPCIONES_CONDICION, default='usado', verbose_name="Condición")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name="Imagen Principal")
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.titulo


class Pregunta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='preguntas', verbose_name="Producto")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Comprador")
    texto_pregunta = models.TextField(verbose_name="Pregunta")
    texto_respuesta = models.TextField(blank=True, null=True, verbose_name="Respuesta del vendedor")
    creado_el = models.DateTimeField(auto_now_add=True)
    respondido_el = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
        ordering = ['-creado_el']

    def __str__(self):
        return f"Pregunta de {self.usuario.username} en {self.producto.titulo}"


# publicaciones/models.py (al final del archivo)

class ClaveProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='claves', verbose_name="Producto")
    clave = models.CharField(max_length=100, unique=True, verbose_name="Código de Activación / Key")
    disponible = models.BooleanField(default=True, verbose_name="¿Está disponible para venta?")
    fecha_agregada = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Clave de Producto"
        verbose_name_plural = "Claves de Productos"

    def __str__(self):
        estado = "Disponible" if self.disponible else "Vendida"
        return f"{self.producto.titulo} - [{estado}] {self.clave}"