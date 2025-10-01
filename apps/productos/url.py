from django.urls import path
from .views import ProductoListCreateView, MarcaListCreateView, MarcaDetailView

urlpatterns = [

    # --- RUTAS CRUD MARCAS ---

    # Listar y crear marcas
    path('api/marcas/', MarcaListCreateView.as_view(), name='api_marcas'),
    # Obtener, actualizar o eliminar una marca por ID
    path('api/marcas/<int:pk>', MarcaDetailView.as_view(), name='api_marcas_detalle'),


    # --- RUTAS CRUD PRODUCTOS ---

    # Busqueda y filtrado de productos
    path('api/productos/', ProductoListCreateView.as_view(), name='api_productos'),
    
]
