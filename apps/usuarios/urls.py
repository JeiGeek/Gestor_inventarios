from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, RolViewSet

# Rutas del router (usuarios y roles)
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'roles', RolViewSet, basename='roles')

urlpatterns = [

    path('', include(router.urls)),

]
