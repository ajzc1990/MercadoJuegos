# entregas/admin.py
from django.contrib import admin
from .models import ContenidoDigital

@admin.register(ContenidoDigital)
class ContenidoDigitalAdmin(admin.ModelAdmin):
    list_display = ('producto', 'archivo_zip', 'url_drive')
    search_fields = ('producto__titulo',)