import os
import django
import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify

# 1. Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mercado_juegos.settings')
django.setup()

from django.contrib.auth.models import User
from publicaciones.models import Producto, Categoria

RAWG_API_KEY = '5a97b131941449cd85595770f72ea533'  # Reemplazá con tu clave de rawg.io
TOTAL_OBJETIVO = 50

# Precios de referencia simulados en ARS
TABLA_PRECIOS = {
    'high': 28500.00,
    'mid': 19900.00,
    'classic': 12500.00
}

def importar_catalogo_masivo():
    vendedor = User.objects.filter(is_superuser=True).first()
    if not vendedor:
        print("❌ Error: No se encontró un superusuario para asignar como vendedor.")
        return

    print(f"🚀 Iniciando importación de {TOTAL_OBJETIVO} videojuegos...")
    
    juegos_procesados = 0
    pagina = 1

    while juegos_procesados < TOTAL_OBJETIVO:
        # Consultamos los títulos más populares ordenados por cantidad de agregados
        url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&page={pagina}&page_size=40&ordering=-added"
        res = requests.get(url)
        
        if res.status_code != 200:
            print(f"❌ Error al consultar la API de RAWG (Status {res.status_code})")
            break
            
        data = res.json()
        resultados = data.get('results', [])
        
        if not resultados:
            print("⚠️ No hay más resultados devueltos por la API.")
            break

        for item in resultados:
            if juegos_procesados >= TOTAL_OBJETIVO:
                break

            titulo = item.get('name')
            slug = item.get('slug')
            rating = item.get('rating', 'N/A')
            
            # 1. Asignar categoría principal del juego o fallback
            generos = item.get('genres', [])
            if generos:
                nombre_cat = generos[0]['name']
                slug_cat = generos[0]['slug']
            else:
                nombre_cat = "Acción"
                slug_cat = "accion"

            categoria, _ = Categoria.objects.get_or_create(
                slug=slug_cat,
                defaults={'nombre': nombre_cat}
            )

            # 2. Verificar si el producto ya existe en la base de datos
            if Producto.objects.filter(titulo=titulo).exists():
                print(f"⏩ [Omitido] {titulo} (ya registrado)")
                juegos_procesados += 1
                continue

            # 3. Lógica de precio según rating
            try:
                r_num = float(rating)
                if r_num >= 4.5:
                    precio = TABLA_PRECIOS['high']
                elif r_num >= 4.0:
                    precio = TABLA_PRECIOS['mid']
                else:
                    precio = TABLA_PRECIOS['classic']
            except (ValueError, TypeError):
                precio = TABLA_PRECIOS['mid']

            # 4. Crear instancia del Producto
            producto = Producto(
                vendedor=vendedor,
                categoria=categoria,
                titulo=titulo,
                descripcion=f"Juego original: {titulo}. Género principal: {nombre_cat}. Puntuación de la comunidad: {rating}/5.",
                precio=precio,
                stock=10,
                condicion='nuevo'
            )

            # 5. Descargar y adjuntar la imagen de portada
            image_url = item.get('background_image')
            if image_url:
                try:
                    img_res = requests.get(image_url, timeout=10)
                    if img_res.status_code == 200:
                        file_name = f"{slug}.jpg"
                        producto.imagen.save(file_name, ContentFile(img_res.content), save=False)
                except Exception as e:
                    print(f"⚠️ No se pudo descargar la portada para {titulo}: {e}")

            producto.save()
            juegos_procesados += 1
            print(f"✅ [{juegos_procesados}/{TOTAL_OBJETIVO}] Guardado: {producto.titulo} (${producto.precio})")

        pagina += 1

    print(f"\n🎉 ¡Proceso finalizado! Total de productos sincronizados: {juegos_procesados}")

if __name__ == "__main__":
    importar_catalogo_masivo()