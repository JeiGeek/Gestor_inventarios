from django.db import models

# MARCAS
class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


# SUCURSALES
class Sucursal(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=200, unique=False)
    encargado = models.CharField(max_length=100, unique=False)

    def __str__(self):
        return self.nombre


# PRODUCTOS
class Producto(models.Model):
    nombre = models.CharField(max_length=255, editable=False)  # Nombre generado automáticamente
    caja = models.CharField(max_length=100)
    amperaje = models.PositiveIntegerField()
    polaridad = models.CharField(max_length=5)
    voltaje = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()

    # Imagen
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    # Llaves foraneas
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Convertir el nombre con la combinacion requerida
        self.nombre = f"{self.marca.nombre} {self.caja} {self.amperaje} {self.polaridad}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


# PRODUCTOS - SUCURSALES
class ProductoSucursal(models.Model):

    # Llaves foraneas
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('producto', 'sucursal') # Asegura que no haya duplicados

    def __str__(self):
        return f'Producto Sucursal {self.id} - Fecha de Creación: {self.fecha_creacion}'

