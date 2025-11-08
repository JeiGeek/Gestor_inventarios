from django.contrib import admin
from .models import Producto, Marca, Sucursal

admin.site.register(Producto)
admin.site.register(Marca)
admin.site.register(Sucursal)