from rest_framework import serializers
from .models import Inventario, TipoInventario, InventarioProducto, LoteInventario
from apps.usuarios.models import Usuario
from apps.productos.models import Producto, Sucursal


class TipoInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoInventario
        fields = ['id', 'nombre']


class InventarioSerializer(serializers.ModelSerializer):
    tipo_inventario_id = serializers.IntegerField(write_only=True)
    sucursal_id = serializers.IntegerField(write_only=True)
    producto_id = serializers.IntegerField(write_only=True)

    tipo_inventario_nombre = serializers.CharField(source='tipo_inventario.nombre', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)

    lote_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    lote_numero = serializers.IntegerField(source='lote.id', read_only=True)

    class Meta:
        model = Inventario
        fields = [
            'id',
            'stock_anterior',
            'conteo',
            'ventas',
            'num_diferencias',
            'comentario',
            'diferencias_encontrada',
            'tipo_inventario_id',
            'sucursal_id',
            'producto_id',
            'lote_id',
            'tipo_inventario_nombre',
            'sucursal_nombre',
            'lote_numero',
            'fecha_creacion',
            'usuario'
        ]
        read_only_fields = ['fecha_creacion', 'stock_anterior', 'num_diferencias', 'diferencias_encontrada']

    def create(self, validated_data):
        tipo_inventario_id = validated_data.pop('tipo_inventario_id')
        sucursal_id = validated_data.pop('sucursal_id')
        producto_id = validated_data.pop('producto_id')
        usuario_id = validated_data.pop('usuario')

        conteo = validated_data.get('conteo')
        ventas = validated_data.get('ventas')

        lote_id = validated_data.pop('lote_id', None)


        # Validaciones
        tipo_inventario = TipoInventario.objects.filter(pk=tipo_inventario_id).first()
        if not tipo_inventario:
            raise serializers.ValidationError({"tipo_inventario_id": "Tipo de inventario no encontrado"})

        sucursal = Sucursal.objects.filter(pk=sucursal_id).first()
        if not sucursal:
            raise serializers.ValidationError({"sucursal_id": "Sucursal no encontrada"})

        # Validar usuario
        if isinstance(usuario_id, Usuario):
            usuario = usuario_id
        else:
            usuario = Usuario.objects.filter(pk=usuario_id).first()

        if not usuario:
            raise serializers.ValidationError({"usuario": f"Usuario con id {usuario_id} no encontrado"})

        producto = Producto.objects.filter(pk=producto_id).first()
        if not producto:
            raise serializers.ValidationError({"producto_id": f"Producto con id {producto_id} no encontrado"})
        
        # Obtener lote si se envió
        lote = None
        if lote_id is not None:
            lote = LoteInventario.objects.filter(pk=lote_id).first()
            if not lote:
                raise serializers.ValidationError({"lote_id": f"Lote con id {lote_id} no encontrado"})
        else:
            # Si no se envió ningún lote, crear uno automáticamente
            lote = LoteInventario.objects.create()


        # Tomar stock anterior del producto
        stock_anterior = producto.stock
        num_diferencias = stock_anterior - conteo - ventas
        diferencias_encontrada = num_diferencias != 0

        # Crear inventario
        inventario = Inventario.objects.create(
            tipo_inventario=tipo_inventario,
            sucursal=sucursal,
            usuario=usuario,
            stock_anterior=stock_anterior,
            num_diferencias=num_diferencias,
            diferencias_encontrada=diferencias_encontrada,
            lote=lote,
            **validated_data
        )

        # Asociar el producto
        InventarioProducto.objects.create(
            inventario=inventario,
            producto=producto
        )

        # Actualizar stock del producto
        producto.stock = conteo
        producto.save()

        return inventario