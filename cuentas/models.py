from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    direccion = models.CharField(max_length=255, blank=True, verbose_name="Dirección de Envío")
    ciudad = models.CharField(max_length=100, blank=True, verbose_name="Ciudad / Localidad")
    es_vendedor = models.BooleanField(default=False, verbose_name="¿Es Vendedor?")
    reputacion = models.DecimalField(max_digits=3, decimal_places=2, default=5.00, verbose_name="Reputación")

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


# Signal unificada y segura para gestionar la creación/actualización del perfil
@receiver(post_save, sender=User)
def gestionar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)
    else:
        if hasattr(instance, 'perfil'):
            instance.perfil.save()