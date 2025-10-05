from django.contrib import admin
from .models import Producto, Marca, Sucursal

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca','stock', 'imagen')

admin.site.register(Marca)
admin.site.register(Sucursal)