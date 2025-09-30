from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, RolViewSet, RegisterView#, MyTokenObtainPairView 

#crea un enrutador y registrar el viewset de usuarios y roles
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'roles', RolViewSet)

#incluir las URL del enrutador
urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    #path("api/token1/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
]