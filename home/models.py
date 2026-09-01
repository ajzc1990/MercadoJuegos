from django.db import models

class Banner(models.Model):
    titulo = models.CharField(max_length=150, verbose_name="Título del Banner")
    subtitulo = models.CharField(max_length=255, blank=True, verbose_name="Subtítulo")
    imagen = models.ImageField(upload_to='banners/', verbose_name="Imagen Promocional")
    url_destino = models.CharField(max_length=255, blank=True, default='#', verbose_name="Enlace de destino")
    activo = models.BooleanField(default=True, verbose_name="¿Está activo?")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden de visualización")
    creado_el = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Banner Promocional"
        verbose_name_plural = "Banners Promocionales"
        ordering = ['orden', '-creado_el']

    def __str__(self):
        return self.titulo