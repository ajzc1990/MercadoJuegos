from decimal import Decimal
from publicaciones.models import Producto

class Carrito:
    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get('carrito')
        if not carrito:
            carrito = self.session['carrito'] = {}
        self.carrito = carrito

    def agregar(self, producto, cantidad=1):
        producto_id = str(producto.id)

        # 1. Si no hay stock directo en la DB, no agregar nada
        if producto.stock <= 0:
            return False

        # 2. Inicializar en la sesión si es la primera vez
        if producto_id not in self.carrito:
            self.carrito[producto_id] = {
                'cantidad': 0,
                'precio': str(producto.precio)
            }
        
        # 3. Validar no superar el stock disponible
        nueva_cantidad = self.carrito[producto_id]['cantidad'] + cantidad
        if nueva_cantidad <= producto.stock:
            self.carrito[producto_id]['cantidad'] = nueva_cantidad
            self.guardar()
            return True
        else:
            # Si el producto se había inicializado en 0 por esta llamada, limpiar la clave para no dejar basura
            if self.carrito[producto_id]['cantidad'] == 0:
                del self.carrito[producto_id]
            return False

    def restar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            self.carrito[producto_id]['cantidad'] -= 1
            if self.carrito[producto_id]['cantidad'] <= 0:
                self.eliminar(producto)
            else:
                self.guardar()

    def eliminar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar()

    def guardar(self):
        self.session.modified = True

    def limpiar(self):
        if 'carrito' in self.session:
            del self.session['carrito']
            self.guardar()

    def __iter__(self):
        producto_ids = self.carrito.keys()
        productos = Producto.objects.filter(id__in=producto_ids)
        carrito_copia = self.carrito.copy()

        for producto in productos:
            if str(producto.id) in carrito_copia:
                carrito_copia[str(producto.id)]['producto'] = producto

        for item in list(carrito_copia.values()):
            # Solo iterar si el producto existe y fue asignado
            if 'producto' in item:
                item['precio'] = Decimal(item['precio'])
                item['subtotal'] = item['precio'] * item['cantidad']
                yield item

    def __len__(self):
        return sum(item['cantidad'] for item in self.carrito.values())

    def get_total(self):
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.carrito.values())