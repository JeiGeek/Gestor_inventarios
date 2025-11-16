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

    # Relacion muchos a muchos con Sucursal a través de ProductoSucursal
    sucursales = models.ManyToManyField(Sucursal, through='ProductoSucursal', related_name='productos')

    # nivel mínimo aceptable de stock
    stock_minimo = models.PositiveIntegerField(default=3)
    # banderas para no enviar alertas duplicadas
    notificado_stock_bajo = models.BooleanField(default=False)
    notificado_sin_stock = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Si el producto ya existía, vemos cómo cambió el stock
        if self.pk is not None:
            try:
                anterior = Producto.objects.get(pk=self.pk)
            except Producto.DoesNotExist:
                anterior = None

            if anterior is not None:
                # Si el stock AUMENTÓ respecto al valor anterior,
                # reseteamos las banderas para permitir nuevas alertas
                if self.stock > anterior.stock:
                    self.notificado_stock_bajo = False
                    self.notificado_sin_stock = False

        # Actualizamos el nombre
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
        return f'Producto Sucursal {self.id}'

