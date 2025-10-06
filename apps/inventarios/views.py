from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import TipoInventario, Inventario, InventarioProducto
from .serializers import TipoInventarioSerializer

############################# -- Tipo Inventario -- ################################
class TipoInventarioListCreateView(APIView):
    """
    API para listar y crear tipos de inventario.
    """
    def get(self, request):
        # Listar todas las marcas
        tipoInventario = TipoInventario.objects.all()
        serializer = TipoInventarioSerializer(tipoInventario, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Crear un nuevo tipo de inventario
        serializer = TipoInventarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TipoInventarioDetailView(APIView):
    """
    API para obtener, actualizar o eliminar un tipo de inventario por ID.
    """
    def get_object(self, pk):
        # Obtener un tipo de inventario por su ID o retornar None si no existe
        try:
            return TipoInventario.objects.get(pk=pk)
        except TipoInventario.DoesNotExist:
            return None

    def get(self, request, pk):
        # Obtener un tipo de inventario por su ID
        tipoInventario = self.get_object(pk)
        if not tipoInventario:
            return Response({'error': 'Tipo de inventario no encontrado'}, status=status.HTTP_404_NOT_FOUND) 
        
        # Serializar y retornar la marca
        serializer = TipoInventarioSerializer(tipoInventario)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        # Actualizar una marca por su ID
        tipoInventario = self.get_object(pk)
        if not tipoInventario:
            return Response({'error': 'Tipo de inventario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serializar y retornar la marca
        serializer = TipoInventarioSerializer(tipoInventario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Eliminar una marca por su ID
        tipoInventario = self.get_object(pk)
        if not tipoInventario:
            return Response({'error': 'Tipo de inventario no encontrado'}, status=status.HTTP_404_NOT_FOUND) 
        
        # Eliminar la marca
        tipoInventario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
