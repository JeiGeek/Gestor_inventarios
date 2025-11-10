from rest_framework import serializers
from apps.productos.models import Producto, Marca, Sucursal, ProductoSucursal

class ProductoSerializer(serializers.ModelSerializer):

    # Campo adicional para mostrar el nombre de la marca
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    sucursal_nombre = serializers.SerializerMethodField()
    sucursal_id = serializers.IntegerField(write_only=True, required=False)

    # Campos del modelo Producto
    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'caja', 'amperaje', 'polaridad', 'voltaje', 
            'stock', 'imagen', 'marca', 'marca_nombre', 'sucursal_id', 'sucursal_nombre'
        ]

    # Método para obtener el nombre de la sucursal asociada
    def get_sucursal_nombre(self, obj):
        # Mejor usa la relación directa, evita otra consulta
        s = obj.sucursales.first()
        return s.nombre if s else None

    # Método para crear un producto y asociarlo a una sucursal
    def create(self, validated_data):
        sucursal_id = validated_data.pop('sucursal_id', None)
        producto = Producto.objects.create(**validated_data)

        # Verifica que la sucursal exista antes de crear la relación
        if sucursal_id is not None:
            try:
                sucursal = Sucursal.objects.get(pk=sucursal_id)
                # Reemplaza cualquier relación previa (si la hubiera)
                producto.sucursales.set([sucursal])
            except Sucursal.DoesNotExist:
                raise serializers.ValidationError({"sucursal_id": "La sucursal especificada no existe."})
        return producto
    
    def update(self, instance, validated_data):
        sucursal_id = validated_data.pop('sucursal_id', None)

        # Actualiza campos simples
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()  # esto también recalcula 'nombre' en tu modelo

        # Si vino sucursal_id en el PUT/PATCH, reemplaza la relación through
        if sucursal_id is not None:
            try:
                sucursal = Sucursal.objects.get(pk=sucursal_id)
                instance.sucursales.set([sucursal])  # reemplaza filas en ProductoSucursal
            except Sucursal.DoesNotExist:
                raise serializers.ValidationError({"sucursal_id": "La sucursal especificada no existe."})

        return instance

class MarcaSerializer(serializers.ModelSerializer):
    
    class Meta:
        # Especificar el modelo y los campos a serializar
        model = Marca
        fields = ['id', 'nombre']

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['id', 'nombre', 'direccion', 'encargado']