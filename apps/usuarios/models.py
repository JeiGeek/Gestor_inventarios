from django.db import models
from django.contrib.auth.models import AbstractUser

# ROLES
class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


# USUARIOS
class Usuario(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    numera_telefono = models.PositiveIntegerField(unique=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    # Llave foranea a otro modelo
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return self.username
