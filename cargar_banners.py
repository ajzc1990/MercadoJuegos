import os
import django
import requests
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mercado_juegos.settings')
django.setup()

from home.models import Banner

BANNERS_DATA = [
    {
        "titulo": "Grand Theft Auto V",
        "subtitulo": "Explorá Los Santos y dominá el mundo online.",
        "url_destino": "/?q=Grand+Theft+Auto",
        "img_url": "https://cdn.akamai.steamstatic.com/steam/apps/271590/header.jpg"
    },
    {
        "titulo": "Cyberpunk 2077",
        "subtitulo": "Night City te espera en la mayor aventura RPG de acción.",
        "url_destino": "/?q=Cyberpunk",
        "img_url": "https://cdn.akamai.steamstatic.com/steam/apps/1091500/header.jpg"
    },
    {
        "titulo": "The Witcher 3: Wild Hunt",
        "subtitulo": "Cazá monstruos y recorré un mundo abierto inolvidable.",
        "url_destino": "/?q=The+Witcher",
        "img_url": "https://cdn.akamai.steamstatic.com/steam/apps/292030/header.jpg"
    }
]

def recargar_banners():
    print("🧹 Limpiando registros antiguos de banners...")
    Banner.objects.all().delete()

    print("🎨 Creando nuevos banners con imágenes verificadas...")
    for i, item in enumerate(BANNERS_DATA, start=1):
        banner = Banner(
            titulo=item["titulo"],
            subtitulo=item["subtitulo"],
            url_destino=item["url_destino"],
            activo=True
        )
        try:
            res = requests.get(item["img_url"], timeout=10)
            if res.status_code == 200:
                banner.imagen.save(f"banner_{i}.jpg", ContentFile(res.content), save=False)
                banner.save()
                print(f"✅ Banner guardado: {banner.titulo}")
            else:
                print(f"❌ Falló descarga ({res.status_code}) para: {item['titulo']}")
        except Exception as e:
            print(f"❌ Error descargando {item['titulo']}: {e}")

if __name__ == "__main__":
    recargar_banners()