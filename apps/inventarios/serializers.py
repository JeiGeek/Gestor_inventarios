from rest_framework import serializers
from .models import Inventario, TipoInventario, InventarioProducto

class TipoInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoInventario
        fields = ['id', 'nombre']