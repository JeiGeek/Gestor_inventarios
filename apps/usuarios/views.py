from django.shortcuts import render

#para los endpoints
from rest_framework import viewsets, generics
from .serializers import RegistroUsuarioSerializer, UsuarioSerializer, RolSerializer
from .models import Usuario, Rol
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.views import TokenObtainPairView
User = get_user_model()
from rest_framework import viewsets, status # Añadir 'status'
from rest_framework.decorators import action # Añadir 'action'
from rest_framework.response import Response # Añadir 'Response'
#ayudan a crear los endpoints de forma automatica
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all() #traer todos los usuarios
    serializer_class = UsuarioSerializer #usar el serializador de usuarios
    
    # Acción personalizada para el registro: Crea el endpoint /usuarios/registro/
    @action(detail=False, methods=['post'] )#, permission_classes=[AllowAny])
    def registro(self, request):
        # 1. Usar el Serializador de Registro para validar y crear el usuario
        serializer = RegistroUsuarioSerializer(data=request.data)
        
        # 2. Validar la data
        if serializer.is_valid():
            # 3. Guardar el nuevo usuario (la lógica de creación está en el serializador)
            serializer.save()
            
            # 4. Respuesta de éxito 201 Created
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # 5. Respuesta de error 400 Bad Request si la validación falla
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer



# Vista para el registro de usuarios personalizados
# class RegistroUsuarioView(generics.CreateAPIView):
#     queryset = Usuario.objects.all()
#     serializer_class = RegistroUsuarioSerializer



#Vista para roles
class RegistroRolView(viewsets.ModelViewSet):  #esto me trae todos lo metodos get, post, put, delete
    queryset = Rol.objects.all()
    serializer_class = RolSerializer


