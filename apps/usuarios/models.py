from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# ROLES
class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


# MANAGER PERSONALIZADO
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre=None, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')

        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nombre, password, **extra_fields)


# MODELO DE USUARIO PERSONALIZADO
class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    nombre = models.CharField(max_length=150, null=True, blank=True)
    numero_telefono = models.PositiveIntegerField(null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'          # Usar email para login
    REQUIRED_FIELDS = ['nombre']      # Campos extra requeridos al crear superusuario

    def __str__(self):
        return self.email
