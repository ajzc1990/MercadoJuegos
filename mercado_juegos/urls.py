# mercado_juegos/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('home.urls', 'home'), namespace='home')),
    path('cuentas/', include(('cuentas.urls', 'cuentas'), namespace='cuentas')), # <--- Aquí se define el prefijo 'cuentas/'
    path('publicaciones/', include(('publicaciones.urls', 'publicaciones'), namespace='publicaciones')),
    path('ventas/', include(('ventas.urls', 'ventas'), namespace='ventas')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)