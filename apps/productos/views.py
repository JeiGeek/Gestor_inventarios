from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Producto
from .serializers import ProductoSerializer

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
