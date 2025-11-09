# pasar de un objeto de Django a JSON
from rest_framework import serializers
from .models import Usuario, Rol
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions

# ----------------------
# SERIALIZER USUARIO
# ----------------------
class UsuarioSerializer(serializers.ModelSerializer):
    permission_classes = [AllowAny]
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}  # nunca devolver la contraseña

    def create(self, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    
    def update(self, instance, validated_data):
        # Encriptar password solo si viene
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data.pop("password"))

        # Manejar rol
        rol_id = validated_data.get("rol_id", None)
        if rol_id is not None:
            try:
                rol_instance = Rol.objects.get(id=rol_id)
                instance.rol = rol_instance
                print("✅ Rol actualizado correctamente en el backend")
            except Rol.DoesNotExist:
                raise serializers.ValidationError({"rol_id": "El rol no existe"})
            
        # Manejar is_active
        if "is_active" in validated_data:
            instance.is_active = validated_data["is_active"]

        # Actualizar otros campos
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()  # ✅ FALTA ESTO PARA GUARDAR EN BD
        return instance




# ----------------------
# SERIALIZER ROL
# ----------------------
class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

# ----------------------
# SERIALIZER REGISTRO USUARIO
# ----------------------
class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    permission_classes = [AllowAny]

    # Usamos IntegerField para aceptar solo ID desde frontend
    rol_id = serializers.IntegerField(required=True)

    class Meta:
        model = Usuario
        fields = ['id', 'email', 'nombre', 'username', 'numero_telefono', 'rol_id', 'password']

    def create(self, validated_data):
        # Obtener instancia de rol desde el ID
        rol_id = validated_data.pop('rol_id')
        try:
            rol_instance = Rol.objects.get(id=rol_id)
        except Rol.DoesNotExist:
            raise serializers.ValidationError({"rol_id": "El rol especificado no existe"})

        # Crear usuario con password encriptada
        usuario = Usuario.objects.create_user(
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            password=validated_data['password'],
            username=validated_data.get('username', ''),
            numero_telefono=validated_data.get('numero_telefono', None),
            rol=rol_instance
        )
        return usuario

# ----------------------
# SERIALIZER TOKEN PERSONALIZADO
# ----------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)

        # ✅ Bloquear si el usuario está desactivado
        if not self.user.is_active:
            raise exceptions.AuthenticationFailed('Usuario desactivado', code='user_inactive')

        return data
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['nombre'] = user.nombre
        token['username'] = user.username

        if hasattr(user, 'rol') and user.rol:
            token['rol'] = user.rol.nombre

        return token
