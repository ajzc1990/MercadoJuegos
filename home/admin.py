# home/admin.py
from django.contrib import admin
from .models import Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'subtitulo', 'url_destino', 'activo', 'creado_el')
    list_filter = ('activo', 'creado_el')
    search_fields = ('titulo', 'subtitulo', 'url_destino')
    list_editable = ('activo',)