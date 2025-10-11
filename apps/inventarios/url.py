from django.urls import path
from .views import TipoInventarioListCreateView, TipoInventarioDetailView, InventarioListCreateView, InventarioDetailView

urlpatterns = [

    # --- RUTAS CRUD TIPOINVENTARIO ---

    # Listar y crear tipos de inventario
    path('api/tipos-inventario/', TipoInventarioListCreateView.as_view(), name='tipo-inventario-list-create'),
    # Obtener, actualizar o eliminar un tipo de inventario por ID
    path('api/tipos-inventario/<int:pk>', TipoInventarioDetailView.as_view(), name='tipo-inventario-detail'),

    # --- RUTAS CRUD INVENTARIO ---

    # Listar y crear inventarios
    path('inventarios/', InventarioListCreateView.as_view(), name='inventario-list-create'),
    # Obtener, actualizar o eliminar un inventario por ID
    path('inventarios/<int:pk>', InventarioDetailView.as_view(), name='inventario-detail'),


]