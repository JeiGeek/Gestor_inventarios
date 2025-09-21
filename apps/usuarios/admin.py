from django.contrib import admin
from .models import Usuario, Rol

# Registro básico
admin.site.register(Usuario)
admin.site.register(Rol)

# Personalización del sitio de administración
admin.site.site_header = "Administración de Usuarios"
admin.site.site_title = "Panel de Control"
admin.site.index_title = "Bienvenido al Panel de Control"
