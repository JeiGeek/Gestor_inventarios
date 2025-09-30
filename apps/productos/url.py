from django.urls import path
from .views import ProductoListCreateView

urlpatterns = [
    path('api/productos/', ProductoListCreateView.as_view(), name='api_productos'),
]
