from django.contrib import admin
from .models import Perfil

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'ciudad', 'es_vendedor', 'reputacion')
    list_filter = ('es_vendedor', 'ciudad')
    search_fields = ('usuario__username', 'usuario__email', 'telefono')