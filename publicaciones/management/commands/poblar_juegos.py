import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from publicaciones.models import Categoria, Producto


class Command(BaseCommand):
    help = 'Pobla la base de datos con 100 productos de videojuegos y categorías'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Iniciando carga de datos...'))

        # 1. Crear o recuperar Categorías
        categorias_datos = [
            'Juegos de PS5',
            'Juegos de PS4',
            'Juegos de Xbox Series X',
            'Juegos de Nintendo Switch',
            'Consolas y Accesorios'
        ]
        
        categorias = []
        for nombre_cat in categorias_datos:
            cat, _ = Categoria.objects.get_or_create(
                nombre=nombre_cat,
                defaults={'slug': slugify(nombre_cat)}
            )
            categorias.append(cat)

        # 2. Crear o recuperar Usuarios Demo (vendedores)
        usuarios_datos = ['gamer_pro', 'pixel_store', 'retro_king', 'tech_house', 'game_zone']
        usuarios = []
        for username in usuarios_datos:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@example.com'}
            )
            if created:
                user.set_password('Django1234!')
                user.save()
            usuarios.append(user)

        # 3. Listas para armar los títulos y combinaciones
        titulos_base = [
            'The Legend of Zelda: Tears of the Kingdom', 'God of War Ragnarök', 
            'Elden Ring', 'EA Sports FC 24', 'Cyberpunk 2077', 
            'Resident Evil 4 Remake', 'Grand Theft Auto V', 'Red Dead Redemption 2',
            'Spider-Man 2', 'Super Mario Bros. Wonder', 'Final Fantasy XVI',
            'Call of Duty: Modern Warfare III', 'Minecraft', 'The Witcher 3: Wild Hunt',
            'Hogwarts Legacy', 'Diablo IV', 'Starfield', 'Baldur\'s Gate 3',
            'Halo Infinite', 'Forza Horizon 5'
        ]

        ediciones = ['Edición Estándar', 'Edición Coleccionista', 'Steelbook Edition', 'Digital Deluxe', 'Edición GOTY']

        descripciones = [
            'Producto en excelente estado, caja original incluida. Listo para jugar.',
            'Juego completamente nuevo y sellado de fábrica. Garantía de 6 meses.',
            'Disco impecable sin ningún rayón. Envío inmediato a todo el país.',
            'Incluye todos los DLCs y contenido descargable de reserva.',
            'Versión física importada en español Latinoamérica.'
        ]

        productos_creados = 0

        # 4. Generar los 100 registros de Productos
        for i in range(100):
            titulo_juego = random.choice(titulos_base)
            edicion = random.choice(ediciones)
            categoria_sel = random.choice(categorias)

            titulo_final = f"{titulo_juego} - {edicion} #{i + 1}"
            
            precio = round(random.uniform(15000, 120000), -2)  # Entre $15.000 y $120.000
            stock = random.randint(1, 25)
            vendedor = random.choice(usuarios)
            condicion = random.choice(['nuevo', 'usado'])
            
            descripcion = (
                f"{random.choice(descripciones)}\n\n"
                f"Categoría: {categoria_sel.nombre}\n"
                f"Estado del producto: {condicion.capitalize()}"
            )

            Producto.objects.create(
                vendedor=vendedor,
                categoria=categoria_sel,
                titulo=titulo_final,
                descripcion=descripcion,
                precio=precio,
                stock=stock,
                condicion=condicion,
            )

            productos_creados += 1

        self.stdout.write(
            self.style.SUCCESS(f'¡Éxito! Se crearon {productos_creados} productos y sus categorías correctamente.')
        )