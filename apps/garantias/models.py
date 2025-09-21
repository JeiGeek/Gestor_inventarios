from django.db import models
from apps.productos.models import Producto, Sucursal
from apps.clientes.models import Cliente

# ESTADOS
class Estado(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    
# GARANTIAS
class Garantia(models.Model):
    serial = models.CharField(max_length=100)
    vigencia_garantia = models.DateField()
    alerta_garantia = models.BooleanField(default=False)

    # Llaves foraneas
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

