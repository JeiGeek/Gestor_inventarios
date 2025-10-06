from django.contrib import admin
from .models import Inventario, TipoInventario, InventarioProducto

admin.site.register(TipoInventario)
admin.site.register(Inventario)
