from rest_framework import serializers
from .models import Garantia

class GarantiaSerializer(serializers.ModelSerializer):
    dias_restantes = serializers.SerializerMethodField()
    tiempo_restante = serializers.CharField(read_only=True)
    en_alerta = serializers.BooleanField(read_only=True)
    nombre_estado = serializers.CharField(read_only=True)
    nombre_producto = serializers.CharField(read_only=True)
    
    def to_representation(self, instance):
        instance.refresh_estado()
        return super().to_representation(instance)

    class Meta:
        model = Garantia
        fields = '__all__'

    def get_dias_restantes(self, obj):
        return obj.dias_restantes
