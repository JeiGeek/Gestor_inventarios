from rest_framework import serializers
from apps.productos.models import Producto, Marca

class ProductoSerializer(serializers.ModelSerializer):

    # Incluir el nombre de la marca en la representación del producto
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)

    class Meta:

        # Especificar el modelo y los campos a serializar
        model = Producto
        fields = ['id', 'nombre', 'caja', 'amperaje', 'polaridad', 'voltaje', 'stock', 'imagen', 'marca_nombre']


class MarcaSerializer(serializers.ModelSerializer):
    
    class Meta:
        # Especificar el modelo y los campos a serializar
        model = Marca
        fields = ['id', 'nombre']