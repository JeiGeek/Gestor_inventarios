from django.shortcuts import render

#para los endpoints
from rest_framework import viewsets, generics
from .serializers import UsuarioSerializer, RolSerializer, RegisterSerializer
from .models import Usuario, Rol

from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

#ayudan a crear los endpoints de forma automatica
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all() #traer todos los usuarios
    serializer_class = UsuarioSerializer #usar el serializador de usuarios


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny] #cualquiera puede registrarse
    serializer_class = RegisterSerializer
    
