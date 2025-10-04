#pasar de un objeto de Django a json
from rest_framework import serializers
from .models import Usuario, Rol
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.permissions import AllowAny


class UsuarioSerializer(serializers.ModelSerializer):
    permission_classes = [AllowAny]
    
    #para encriptar la contraseña
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}  # nunca devolver la contraseña

    def create(self, validated_data):
        # Encriptamos la contraseña antes de guardar
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Si viene un campo password, lo encriptamos
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)
    

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'



#serializador para el registro de usuarios personalizado
class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    permission_classes = [AllowAny]
    # Usar PrimaryKeyRelatedField para aceptar el ID en la entrada
    rol_id = serializers.PrimaryKeyRelatedField(
        queryset=Rol.objects.all(), # Asegura que el ID exista en el modelo Rol
        required=True # Asegúrate de que este campo es obligatorio
    )
    
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'nombre', 'username', 'numero_telefono', 'rol_id', 'password']

    def create(self, validated_data):
        rol_instance = validated_data.pop('rol_id')  # Extraer la instancia del rol
        rol_id_entero = rol_instance.id  # Obtener el ID entero del rol
        usuario = Usuario.objects.create_user(
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            password=validated_data['password'],
            username=validated_data.get('username', ''),
            numero_telefono=validated_data.get('numero_telefono', None),
            rol_id=rol_id_entero  # asignar el rol
            
        )
        return usuario
