from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import TipoInventario, Inventario, InventarioProducto
from .serializers import TipoInventarioSerializer, InventarioSerializer
from apps.productos.models import Producto, Sucursal

# temporal
from rest_framework.permissions import AllowAny

############################# -- Tipo Inventario -- ################################
class TipoInventarioListCreateView(APIView):
    #temporal
    permission_classes = [AllowAny]
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
    #temporal
    permission_classes = [AllowAny]
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


############################# -- Inventario -- ################################

class InventarioListCreateView(APIView):
    #temporal
    permission_classes = [AllowAny]
    """
    API para listar y crear inventarios.
    """
    def get(self, request):
        inventarios = Inventario.objects.all().order_by('-fecha_creacion')
        serializer = InventarioSerializer(inventarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        # Si es un solo objeto (un inventario)
        if isinstance(data, dict):
            serializer = InventarioSerializer(data=data)
            if serializer.is_valid():
                inventario = serializer.save()
                return Response(InventarioSerializer(inventario).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Si es una lista de objetos (varios inventarios a la vez)
        elif isinstance(data, list):
            created_items = []
            for item in data:
                serializer = InventarioSerializer(data=item)
                serializer.is_valid(raise_exception=True)
                inventario = serializer.save()
                created_items.append(InventarioSerializer(inventario).data)
            return Response(created_items, status=status.HTTP_201_CREATED)

        return Response({"error": "Formato de datos inválido"}, status=status.HTTP_400_BAD_REQUEST)
    


class InventarioDetailView(APIView):
    #temporal
    permission_classes = [AllowAny]
    """
    API para obtener, actualizar (PATCH) o eliminar un inventario por ID.
    """
    def get_object(self, pk):
        try:
            return Inventario.objects.get(pk=pk)
        except Inventario.DoesNotExist:
            return None

    def get(self, request, pk):
        inventario = self.get_object(pk)
        if not inventario:
            return Response({'error': 'Inventario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = InventarioSerializer(inventario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        inventario = self.get_object(pk)
        if not inventario:
            return Response({'error': 'Inventario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        comentario = request.data.get('comentario', None)

        if comentario is not None:
            inventario.comentario = comentario
            inventario.save()

        serializer = InventarioSerializer(inventario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        inventario = self.get_object(pk)
        if not inventario:
            return Response({'error': 'Inventario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        inventario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

