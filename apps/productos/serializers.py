from rest_framework import serializers
from apps.productos.models import Producto, Marca, Sucursal, ProductoSucursal

class ProductoSerializer(serializers.ModelSerializer):
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    sucursal_nombre = serializers.SerializerMethodField()
    sucursal_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'caja', 'amperaje', 'polaridad', 'voltaje', 
            'stock', 'imagen', 'marca', 'marca_nombre', 'sucursal_id', 'sucursal_nombre'
        ]

    def get_sucursal_nombre(self, obj):
        relacion = ProductoSucursal.objects.filter(producto=obj).first()
        if relacion and relacion.sucursal:
            return relacion.sucursal.nombre
        return None

    def create(self, validated_data):
        sucursal_id = validated_data.pop('sucursal_id', None)
        producto = Producto.objects.create(**validated_data)

        # Verifica que la sucursal exista antes de crear la relación
        if sucursal_id:
            try:
                sucursal = Sucursal.objects.get(pk=sucursal_id)
                ProductoSucursal.objects.create(producto=producto, sucursal=sucursal)
            except Sucursal.DoesNotExist:
                raise serializers.ValidationError({"sucursal_id": "La sucursal especificada no existe."})

        return producto

class MarcaSerializer(serializers.ModelSerializer):
    
    class Meta:
        # Especificar el modelo y los campos a serializar
        model = Marca
        fields = ['id', 'nombre']

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['id', 'nombre', 'direccion', 'encargado']