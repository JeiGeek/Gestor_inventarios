from django.urls import path
from .views import ProductoListCreateView, ProductoDetailView, MarcaListCreateView, MarcaDetailView, SucursalListCreateView, SucursalDetailView

urlpatterns = [

    # --- RUTAS CRUD MARCAS ---

    # Listar y crear marcas
    path('api/marcas/', MarcaListCreateView.as_view(), name='api_marcas'),
    # Obtener, actualizar o eliminar una marca por ID
    path('api/marcas/<int:pk>', MarcaDetailView.as_view(), name='api_marcas_detalle'),


    # --- RUTAS CRUD SUCURSALES ---

    # Listar y crear sucursales
    path('api/sucursales/', SucursalListCreateView.as_view(), name='api_sucursales'),
    # Obtener, actualizar o eliminar una sucursal por ID
    path('api/sucursales/<int:pk>', SucursalDetailView.as_view(), name='api_sucursales_detalle'),


    # --- RUTAS CRUD PRODUCTOS ---

    # Busqueda y filtrado de productos
    path('api/productos/', ProductoListCreateView.as_view(), name='api_productos'),
    # Obtener, actualizar o eliminar un producto por ID
    path('api/productos/<int:pk>', ProductoDetailView.as_view(), name='api_productos_detalle'),

    
]
