from django.db import models
from apps.usuarios.models import Usuario
from apps.productos.models import Producto, Sucursal


# TIPOS DE INVENTARIO
class TipoInventario(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


# INVENTARIOS
class Inventario(models.Model):
    conteo = models.IntegerField()
    ventas = models.IntegerField()
    num_diferencias = models.IntegerField()
    comentario = models.TextField()

    # Llaves foraneas
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_inventario = models.ForeignKey(TipoInventario, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    def __str__(self):
        return f"Inventario: {self.conteo}, Ventas: {self.ventas}, Diferencias: {self.num_diferencias}, Comentarios: {self.comentario}"


# INVENTARIO - PRODUCTO
class InventarioProducto(models.Model):

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Llaves foraneas
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return f'Inventario Producto {self.id} - Fecha de Creación: {self.fecha_creacion}'