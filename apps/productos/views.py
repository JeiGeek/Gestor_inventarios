from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Producto, Marca, Sucursal
from .serializers import ProductoSerializer, MarcaSerializer, SucursalSerializer

# temporal
from rest_framework.permissions import AllowAny


############################# -- Marca-- ################################

class MarcaListCreateView(APIView):
    #temporal
    permission_classes = [AllowAny]

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
    #temporal
    permission_classes = [AllowAny]

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


############################# -- Sucursal -- ################################

class SucursalListCreateView(APIView):
    #temporal
    permission_classes = [AllowAny]

    """
    API para listar y crear sucursales.
    """
    def get(self, request):
        # Listar todas las sucursales
        sucursales = Sucursal.objects.all()
        serializer = SucursalSerializer(sucursales, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Crear una nueva sucursal
        serializer = SucursalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SucursalDetailView(APIView):
    #temporal
    permission_classes = [AllowAny]
    
    """
    API para obtener, actualizar o eliminar una sucursal por ID.
    """
    def get_object(self, pk):
        # Obtener una sucursal por su ID o retornar None si no existe
        try:
            return Sucursal.objects.get(pk=pk)
        except Sucursal.DoesNotExist:
            return None

    def get(self, request, pk):
        # Obtener una sucursal por su ID
        sucursal = self.get_object(pk)
        if not sucursal:
            return Response({'error': 'Sucursal no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SucursalSerializer(sucursal)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # Actualizar una sucursal por su ID
        sucursal = self.get_object(pk)
        if not sucursal:
            return Response({'error': 'Sucursal no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SucursalSerializer(sucursal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Eliminar una sucursal por su ID
        sucursal = self.get_object(pk)
        if not sucursal:
            return Response({'error': 'Sucursal no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        sucursal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

############################# -- Producto -- ################################

class ProductoListCreateView(APIView):

    #temporal
    permission_classes = [AllowAny]

    """
    API para listar productos con búsqueda por palabra y filtrado por marca.
    """
    def post(self, request):
        """
        Permite crear uno o varios productos a la vez.
        Si el cuerpo es una lista, crea múltiples registros.
        """
        data = request.data

        # Si el cuerpo es una lista (muchos productos)
        if isinstance(data, list):
            serializer = ProductoSerializer(data=data, many=True)
        else:
            serializer = ProductoSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request):
        # Obtener parámetros de consulta
        query = request.GET.get('q', '') # palabra a buscar
        marca_nombre = request.GET.get('marca', '') # filtro por marca
        # filtro por sucursal
        sucursal_nombre = request.GET.get('sucursal','')

        # Filtrar productos por búsqueda y marca
        productos = Producto.objects.all().prefetch_related('sucursales', 'marca')

        if query or marca_nombre or sucursal_nombre:
            # filtrar por palabra clave (nombre)
            if query:
                productos = productos.filter(Q(nombre__icontains=query))

            # filtrar por marca
            if marca_nombre:
                productos = productos.filter(marca__nombre__icontains=marca_nombre)
            
            # filtrar por sucursal
            if sucursal_nombre:
                productos = productos.filter(sucursales__nombre__icontains=sucursal_nombre)

        # Serializar y retornar la respuesta
        serializer = ProductoSerializer(productos, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductoDetailView(APIView):

    #temporal
    permission_classes = [AllowAny]

    """
    API para obtener, actualizar o eliminar un producto por ID.
    """

    def get_object(self, pk):
        # Obtener un producto por su ID o retornar None si no existe
        try:
            return Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Obtener un producto por su ID.
        """
        producto = self.get_object(pk)
        if not producto:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductoSerializer(producto, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Actualizar un producto existente.
        """
        producto = self.get_object(pk)
        if not producto:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()  # El nombre se actualiza automáticamente desde el modelo
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        """
        Actualizar parcialmente un producto existente (solo algunos campos).
        """
        producto = self.get_object(pk)
        if not producto:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductoSerializer(producto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Eliminar un producto por ID.
        """
        producto = self.get_object(pk)
        if not producto:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
