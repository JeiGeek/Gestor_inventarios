# apps/usuarios/pipelines.py
from apps.usuarios.models import Rol
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.models import UserSocialAuth
from social_core.pipeline.social_auth import associate_user as original

def asignar_rol_por_defecto(strategy, details, backend, user=None, *args, **kwargs):
    """
    Asigna rol 'worker' solo si el usuario es nuevo (creado por Google).
    Si ya existía, mantiene su rol actual.
    """
    if backend.name != 'google-oauth2' or user is None:
        return

    # Verificar si el usuario fue recién creado por el pipeline
    is_new = kwargs.get('is_new', False)

    try:
        if is_new:
            # Solo para usuarios nuevos creados por Google
            rol_worker, _ = Rol.objects.get_or_create(nombre='worker')
            user.rol = rol_worker
            user.is_staff = False
            user.is_superuser = False
            user.save()
            print(f"✅ Nuevo usuario Google → {user.email} asignado a rol 'worker'")
        else:
            # Usuario ya existente: mantener su rol actual
            print(f"🔹 Usuario existente detectado: {user.email}, mantiene su rol actual ({user.rol})")
    except Exception as e:
        print(f"⚠️ Error asignando rol por defecto: {e}")


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'google-oauth2' or user is None:
        return
    user.nombre = response.get('name') or response.get('given_name') or user.nombre or 'Usuario'
    if not user.username:
        user.username = (response.get('email') or '').split('@')[0]
    user.save()

def create_jwt_token_with_role(strategy, backend, user, *args, **kwargs):
    if user is None:
        return
    refresh = RefreshToken.for_user(user)
    refresh['rol'] = user.rol.nombre if getattr(user, 'rol', None) else 'sin_rol'
    refresh['nombre'] = user.nombre or user.first_name or ""
    refresh['email'] = user.email or ""
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    frontend_url = "https://proyecto-powervolt.onrender.com/"
    return strategy.redirect(f"{frontend_url}?token={access_token}&refresh={refresh_token}")

# safe wrappers (optional, pueden adaptarse)
def associate_user_safe(backend, uid, user=None, *args, **kwargs):

    try:
        return original(backend, uid, user=user, *args, **kwargs)
    except Exception:
        # no forzamos asociación con user que venga; devolvemos sin fallo
        return {}

def social_user_safe(backend, uid, user=None, *args, **kwargs):
    """
    Si hay un UserSocialAuth para este uid/provider, devolverlo.
    Si no, devolver {'user': None} para que se cree usuario nuevo.
    """
    try:
        social = UserSocialAuth.objects.get(provider=backend.name, uid=uid)
        print(f" Encontrado vínculo social para uid {uid}, usuario: {social.user.email}")
        return {'user': social.user}
    except UserSocialAuth.DoesNotExist:
        print(f" No existe vínculo social para uid {uid}; se creará usuario nuevo")
        return {'user': None}


from django.contrib.auth import get_user_model
from django.db.models import Q

from social_core.exceptions import AuthForbidden  

def associate_by_email(strategy, details, backend, uid=None, user=None, *args, **kwargs):
    print("🚀 Entró al pipeline associate_by_email")
    print("Detalles recibidos:", details)
    email = (details.get('email') or '').strip().lower()
    print(f"Email detectado: {email}")

    if user:
        print(f"⚠️ Ignorando usuario logueado ({getattr(user, 'email', None)}) para buscar coincidencia real.")
        user = None

    Usuario = get_user_model()
    print(f"🧩 Modelo de usuario activo: {Usuario}")

    if not email:
        print("⚠️ No se recibió email, no se puede asociar.")
        return None

    try:
        usuario_existente = Usuario.objects.filter(Q(email__iexact=email)).first()
        if usuario_existente:
            if not usuario_existente.is_active:
                print(f"🚫 Usuario {email} está desactivado, no puede ingresar con Google.")
                raise AuthForbidden(backend)

            print(f"✅ Usuario existente encontrado: {usuario_existente.email}")
            return {'user': usuario_existente}
        else:
            print(f"⛔ No existe usuario con el correo {email}. Acceso denegado.")
            # 🚫 Bloquear el acceso inmediatamente
            raise AuthForbidden(backend)
    except Exception as e:
        print(f"💥 Error en associate_by_email: {e}")
        raise AuthForbidden(backend)