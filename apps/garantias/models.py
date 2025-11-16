from django.db import models
from apps.productos.models import Producto, Sucursal
from apps.clientes.models import Cliente
from datetime import date
from dateutil.relativedelta import relativedelta
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Estado(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
    

class Garantia(models.Model):
    serial = models.CharField(max_length=100)
    fecha_inicio_garantia = models.DateField()
    fecha_fin_garantia = models.DateField()
    alerta_garantia = models.BooleanField(default=False)
    cliente = models.CharField(max_length=600, default="Sin cliente")
    telefono_cliente = models.CharField(max_length=20, blank=True, null=True)

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    
    @property
    def tiempo_restante(self):
        hoy = date.today()

        if hoy > self.fecha_fin_garantia:
            delta = relativedelta(hoy, self.fecha_fin_garantia)
            return f"Vencida hace {delta.years} años, {delta.months} meses, {delta.days} días"

        delta = relativedelta(self.fecha_fin_garantia, hoy)
        return f"{delta.years} años, {delta.months} meses y {delta.days} días"

    @property
    def dias_restantes(self):
        hoy = date.today()
        return (self.fecha_fin_garantia - hoy).days

    @property
    def en_alerta(self):
        return self.dias_restantes <= 8
    
    @property
    
    def nombre_estado(self):
        return self.estado.nombre
    
    @property
    def nombre_producto(self):
        return self.producto.nombre
    
    def refresh_estado(self):
        hoy = date.today()
        dias = (self.fecha_fin_garantia - hoy).days

        self.alerta_garantia = dias <= 8
        
        # Actualizar estado
        if dias < 0:
            self.estado_id = 2  # inactiva
        else:
            self.estado_id = 1  # activa
        
        self.save(update_fields=['alerta_garantia', 'estado'])


@receiver(pre_save, sender=Garantia)
def actualizar_alerta(sender, instance, **kwargs):
    hoy = date.today()
    dias = (instance.fecha_fin_garantia - hoy).days

    # Actualizar alerta
    instance.alerta_garantia = dias <= 8

    # Cambiar estado automáticamente
    if dias < 0 and instance.estado_id != 2:  
        instance.estado_id = 2  # INACTIVA (ID = 2)
    elif dias >= 0 and instance.estado_id != 1:
        instance.estado_id = 1  # ACTIVA (ID = 1)

