from django.db import models

# CLIENTES
class Cliente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    cedula = models.PositiveIntegerField(unique=True)
    numero_telefono = models.PositiveIntegerField(unique=False)
    
    def __str__(self):
        return self.nombre

