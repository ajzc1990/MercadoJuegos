# entregas/models.py
from django.db import models
from publicaciones.models import Producto

class ContenidoDigital(models.Model):
    producto = models.OneToOneField(
        Producto, 
        on_delete=models.CASCADE, 
        related_name='contenido_digital'
    )
    archivo_zip = models.FileField(
        upload_to='juegos_zips/', 
        blank=True, 
        null=True,
        help_text="Archivo .zip del juego para adjuntar en correo"
    )
    url_drive = models.URLField(
        blank=True, 
        null=True, 
        help_text="Enlace alternativo de Google Drive/Mega si el archivo es muy pesado"
    )

    def __str__(self):
        return f"Contenido Digital - {self.producto.titulo}"