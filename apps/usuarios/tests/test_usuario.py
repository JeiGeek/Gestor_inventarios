import pytest
from django.contrib.auth import get_user_model
from apps.usuarios.models import Rol

Usuario = get_user_model()

# ============================================================
# 1. Crear usuario normal
# ============================================================
@pytest.mark.django_db
def test_crear_usuario():
    user = Usuario.objects.create_user(
        email="test@gmail.com",
        nombre="Juan",
        password="123456"
    )

    assert user.email == "test@gmail.com"
    assert user.nombre == "Juan"
    assert user.check_password("123456") is True
    assert user.is_active is True


# ============================================================
# 2. Crear superusuario
# ============================================================
@pytest.mark.django_db
def test_crear_superusuario():
    admin = Usuario.objects.create_superuser(
        email="admin@gmail.com",
        nombre="Admin",
        password="admin123"
    )

    assert admin.is_staff is True
    assert admin.is_superuser is True
    assert admin.check_password("admin123") is True


# ============================================================
# 3. Email debe ser único
# ============================================================
@pytest.mark.django_db
def test_email_unico():
    Usuario.objects.create_user(email="rep@gmail.com", nombre="Test", password="1234")

    with pytest.raises(Exception):
        Usuario.objects.create_user(email="rep@gmail.com", nombre="Otro", password="1234")


# ============================================================
# 4. Username único
# ============================================================
@pytest.mark.django_db
def test_username_unico():
    Usuario.objects.create(
        email="u1@gmail.com",
        username="user123",
        password="pass"
    )

    with pytest.raises(Exception):
        Usuario.objects.create(
            email="u2@gmail.com",
            username="user123",
            password="pass"
        )


# ============================================================
# 5. NO crear usuario sin email
# ============================================================
@pytest.mark.django_db
def test_no_crear_usuario_sin_email():
    with pytest.raises(ValueError):
        Usuario.objects.create_user(
            email="",
            nombre="Juan",
            password="123"
        )




# ============================================================
# 6. Superusuario siempre is_staff e is_superuser
# ============================================================
@pytest.mark.django_db
def test_superusuario_flags_obligatorios():
    admin = Usuario.objects.create_superuser(
        email="admin2@gmail.com",
        nombre="Admin",
        password="pass"
    )

    assert admin.is_staff is True
    assert admin.is_superuser is True


# ============================================================
# 7. Usuario con Rol asignado
# ============================================================
@pytest.mark.django_db
def test_usuario_con_rol():
    rol = Rol.objects.create(nombre="worker")

    user = Usuario.objects.create_user(
        email="rol@gmail.com",
        nombre="Mario",
        password="12345",
        rol=rol
    )

    assert user.rol.nombre == "worker"


# ============================================================
# 8. Crear usuario sin nombre (opcional)
# ============================================================
@pytest.mark.django_db
def test_crear_usuario_sin_nombre():
    user = Usuario.objects.create_user(
        email="noname@gmail.com",
        password="abc123"
    )

    assert user.nombre is None


# ============================================================
# 9. Teléfono opcional
# ============================================================
@pytest.mark.django_db
def test_telefono_opcional():
    user = Usuario.objects.create_user(
        email="tel@gmail.com",
        nombre="Tel Test",
        password="1234",
        numero_telefono=None
    )

    assert user.numero_telefono is None


# ============================================================
# 10. Actualizar información del usuario
# ============================================================
@pytest.mark.django_db
def test_actualizar_usuario():
    user = Usuario.objects.create_user(
        email="update@gmail.com",
        nombre="Pedro",
        password="1234"
    )

    user.nombre = "Pedro Actualizado"
    user.numero_telefono = "3001234567"
    user.save()

    updated = Usuario.objects.get(email="update@gmail.com")

    assert updated.nombre == "Pedro Actualizado"
    assert updated.numero_telefono == "3001234567"


# ============================================================
# 11. Cambiar contraseña
# ============================================================
@pytest.mark.django_db
def test_cambiar_password():
    user = Usuario.objects.create_user(
        email="pass@gmail.com",
        nombre="Carlos",
        password="1234"
    )

    user.set_password("nueva123")
    user.save()

    assert user.check_password("nueva123") is True


# ============================================================
# 12. Eliminar usuario
# ============================================================
@pytest.mark.django_db
def test_eliminar_usuario():
    user = Usuario.objects.create_user(
        email="delete@gmail.com",
        nombre="Maria",
        password="1234"
    )

    user_id = user.id
    user.delete()

    assert not Usuario.objects.filter(id=user_id).exists()



# ============================================================
# 13. Cambiar rol del usuario
# ============================================================
@pytest.mark.django_db
def test_actualizar_rol():
    rol1 = Rol.objects.create(nombre="worker")
    rol2 = Rol.objects.create(nombre="Administrador")

    user = Usuario.objects.create_user(
        email="rolupdate@gmail.com",
        nombre="Luis",
        password="1234",
        rol=rol1,
    )

    user.rol = rol2
    user.save()

    assert user.rol.nombre == "Administrador"
