from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Producto, Marca
from .serializers import ProductoSerializer, MarcaSerializer

############################# -- Marca-- ################################

class MarcaListCreateView(APIView):
    """
    API para listar y crear marcas.
    """
    def get(self, request):

        # Listar todas las marcas
        marcas = Marca.objects.all()
        serializer = MarcaSerializer(marcas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Crear una nueva marca
        serializer = MarcaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarcaDetailView(APIView):
    """
    API para obtener, actualizar o eliminar una marca por ID.
    """
    def get_object(self, pk):
        # Obtener una marca por su ID o retornar None si no existe
        try:
            return Marca.objects.get(pk=pk)
        except Marca.DoesNotExist:
            return None

    def get(self, request, pk):
        # Obtener una marca por su ID
        marca = self.get_object(pk)
        if not marca:
            return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND) 
        
        # Serializar y retornar la marca
        serializer = MarcaSerializer(marca)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # Actualizar una marca por su ID
        marca = self.get_object(pk)
        if not marca:
            return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serializar y retornar la marca
        serializer = MarcaSerializer(marca, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Eliminar una marca por su ID
        marca = self.get_object(pk)
        if not marca:
            return Response({'error': 'Marca no encontrada'}, status=status.HTTP_404_NOT_FOUND) 
        
        # Eliminar la marca
        marca.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

############################# -- Producto -- ################################

class ProductoListCreateView(APIView):
    """
    API para listar productos con búsqueda por palabra y filtrado por marca.
    """

    def get(self, request):
        # Obtener parámetros de consulta
        query = request.GET.get('q', '') # palabra a buscar
        marca_nombre = request.GET.get('marca', '') # filtro por marca

        # Filtrar productos por búsqueda y marca
        productos = Producto.objects.all()

        # filtrar por palabra clave (nombre)
        if query:
            productos = productos.filter(Q(nombre__icontains=query))

        # filtrar por marca
        if marca_nombre:
            productos = productos.filter(marca__nombre__icontains=marca_nombre)

        # Serializar y retornar la respuesta
        serializer = ProductoSerializer(productos, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
