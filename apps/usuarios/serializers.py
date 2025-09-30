#pasar de un objeto de Django a json
from rest_framework import serializers
from .models import Usuario, Rol
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
User = get_user_model()



class UsuarioSerializer(serializers.ModelSerializer):
    
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




#registrar usuarios con el modelo User de Django

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}# nunca devolver la contraseña

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ""),
            password=validated_data['password']
        )
        return user



