from django.db import models
from apps.usuarios.models import Usuario
from apps.productos.models import Producto, Sucursal


# TIPOS DE INVENTARIO
class TipoInventario(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

# LOTE DE INVENTARIOS (identificador simple para creaciones en bloque)
class LoteInventario(models.Model):
    # id autoincremental entero “sencillo”
    # (AutoField es entero consecutivo por defecto)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # El id es justo el número que quieres ver como identificador
        return f"Lote #{self.id}"

# INVENTARIOS
class Inventario(models.Model):
    stock_anterior = models.IntegerField(default=0)
    conteo = models.IntegerField()
    ventas = models.IntegerField(null=True, blank=True)          # puede ser null si aplica
    num_diferencias = models.IntegerField(null=True, blank=True) # puede ser null si aplica
    comentario = models.TextField(null=True, blank=True)         # opcional
    diferencias_encontrada = models.BooleanField(default=False)  # true si se encontraron diferencias

    # Llaves foraneas
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_inventario = models.ForeignKey(TipoInventario, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    # Relación muchos a muchos con Producto a través de InventarioProducto
    productos = models.ManyToManyField(Producto, through='InventarioProducto', related_name='inventarios')

    lote = models.ForeignKey(LoteInventario, on_delete=models.SET_NULL, null=True, blank=True, related_name='inventarios')

    # Fecha de creación
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inventario: {self.conteo}, Ventas: {self.ventas}, Diferencias: {self.num_diferencias}, Comentarios: {self.comentario}"


# INVENTARIO - PRODUCTO
class InventarioProducto(models.Model):

    # Llaves foraneas
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)

    def __str__(self):
        return f'Inventario Producto {self.id} - Fecha de Creación: {self.fecha_creacion}'