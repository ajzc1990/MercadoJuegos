import os
import django
import requests
from django.core.files.base import ContentFile

# 1. Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mercado_juegos.settings')
django.setup()

from django.contrib.auth.models import User
from publicaciones.models import Producto, Categoria

RAWG_API_KEY = '5a97b131941449cd85595770f72ea533'

JUEGOS_BUSCAR = [
    "Grand Theft Auto V",
    "Elden Ring",
    "Cyberpunk 2077",
    "Red Dead Redemption 2",
    "The Witcher 3: Wild Hunt"
]

def importar_juegos():
    # Obtener el superusuario vendedor
    vendedor = User.objects.filter(is_superuser=True).first()
    if not vendedor:
        print("❌ Error: No se encontró un superusuario para asignar como vendedor.")
        return

    # Obtener o crear la categoría por defecto
    categoria, _ = Categoria.objects.get_or_create(
        nombre="Juegos",
        defaults={'slug': 'juegos'}
    )

    for nombre_juego in JUEGOS_BUSCAR:
        url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&search={nombre_juego}"
        response = requests.get(url).json()

        results = response.get('results', [])
        if not results:
            print(f"❌ No se encontró el juego: {nombre_juego}")
            continue

        data = results[0]
        titulo_juego = data['name']

        # Verificar si el juego ya fue creado
        if Producto.objects.filter(titulo=titulo_juego).exists():
            print(f"⏩ [Ya existía] Juego: {titulo_juego}")
            continue

        # Crear el producto
        producto = Producto(
            vendedor=vendedor,
            categoria=categoria,
            titulo=titulo_juego,
            descripcion=f"Juego de acción/aventura. Calificación RAWG: {data.get('rating', 'N/A')}/5.",
            precio=18500.00,
            stock=5,
            condicion='nuevo'
        )

        # Descargar la imagen de RAWG y asignarla al ImageField
        image_url = data.get('background_image')
        if image_url:
            img_res = requests.get(image_url)
            if img_res.status_code == 200:
                file_name = f"{data['slug']}.jpg"
                producto.imagen.save(file_name, ContentFile(img_res.content), save=False)

        producto.save()
        print(f"✅ [Creado] Juego: {producto.titulo}")

if __name__ == "__main__":
    importar_juegos()
