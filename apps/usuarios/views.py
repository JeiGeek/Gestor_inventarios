from django.shortcuts import render

#para los endpoints
from rest_framework import viewsets, generics
from .serializers import RegistroUsuarioSerializer, UsuarioSerializer, RolSerializer,CustomTokenObtainPairSerializer
from .models import Usuario, Rol
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.views import TokenObtainPairView
User = get_user_model()
from rest_framework import viewsets, status 
from rest_framework.decorators import action 
from rest_framework.response import Response 


#ayudan a crear los endpoints de forma automatica
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all() #traer todos los usuarios
    serializer_class = UsuarioSerializer #usar el serializador de usuarios
    
    
    @action(detail=True, methods=['put'])
    def toggle_active(self, request, pk=None):
            try:
                usuario = self.get_object()
                
                # Alternar
                usuario.is_active = not usuario.is_active
                usuario.save()  # ✅ Guarda realmente en BD

                return Response(
                    {"message": "Estado actualizado", "is_active": usuario.is_active},
                    status=status.HTTP_200_OK
                )

            except Usuario.DoesNotExist:
                return Response(
                    {"error": "Usuario no encontrado"},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )


            
    # Acción personalizada para el registro: Crea el endpoint /usuarios/registro/
    @action(detail=False, methods=['post'])
    def registro(self, request):
        # Usar el Serializador de Registro para validar y crear el usuario
        serializer = RegistroUsuarioSerializer(data=request.data)
        
        # Validar la data
        if serializer.is_valid():
            # Guardar el nuevo usuario (la lógica de creación está en el serializador)
            serializer.save()
            
            # Respuesta de éxito 201 Created
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Respuesta de error 400 Bad Request si la validación falla
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer




#Vista para roles
class RegistroRolView(viewsets.ModelViewSet):  #esto me trae todos lo metodos get, post, put, delete
    queryset = Rol.objects.all()
    serializer_class = RolSerializer



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



