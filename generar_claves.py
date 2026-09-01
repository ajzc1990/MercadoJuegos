import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mercado_juegos.settings')
django.setup()

from publicaciones.models import Producto, ClaveProducto

def generar_stock():
    productos = Producto.objects.all()
    print(f"📦 Generando licencias para {productos.count()} videojuegos...")

    total_claves = 0
    for p in productos:
        # Generamos 3 claves por cada producto
        for i in range(1, 4):
            codigo_fake = f"{p.titulo[:4].upper().replace(' ', 'X')}-{uuid.uuid4().hex[:4].upper()}-{uuid.uuid4().hex[:4].upper()}-{uuid.uuid4().hex[:4].upper()}"
            _, created = ClaveProducto.objects.get_or_create(
                producto=p,
                clave=codigo_fake,
                defaults={'disponible': True}
            )
            if created:
                total_claves += 1
        
        # Sincronizamos el stock numérico del producto con las claves disponibles
        p.stock = p.claves.filter(disponible=True).count()
        p.save()

    print(f"✅ Se generaron {total_claves} claves digitales y se actualizó el stock.")

if __name__ == "__main__":
    generar_stock()