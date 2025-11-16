import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.productos.models import Marca, Sucursal, Producto, ProductoSucursal

# ============================================================
# 1. Crear marca
# ============================================================
@pytest.mark.django_db
def test_crear_marca():
    marca = Marca.objects.create(nombre="MAC")
    assert marca.nombre == "MAC"

# ============================================================
# 2. Marca única
# ============================================================
@pytest.mark.django_db
def test_marca_unica():
    Marca.objects.create(nombre="MAC")
    with pytest.raises(Exception):
        Marca.objects.create(nombre="MAC")

# ============================================================
# 3. Crear sucursal
# ============================================================
@pytest.mark.django_db
def test_crear_sucursal():
    suc = Sucursal.objects.create(
        nombre="Sucursal 1",
        direccion="Calle 123",
        encargado="Juan"
    )
    assert suc.nombre == "Sucursal 1"

# ============================================================
# 4. Crear producto
# ============================================================
@pytest.mark.django_db
def test_crear_producto():
    marca = Marca.objects.create(nombre="MAC")

    producto = Producto.objects.create(
        marca=marca,
        caja="A1",
        amperaje=100,
        polaridad="D",
        voltaje=12,
        stock=10
    )

    assert producto.caja == "A1"
    assert producto.stock == 10

# ============================================================
# 5. Nombre generado automáticamente
# ============================================================
@pytest.mark.django_db
def test_nombre_generado():
    marca = Marca.objects.create(nombre="MAC")

    producto = Producto.objects.create(
        marca=marca,
        caja="A1",
        amperaje=100,
        polaridad="D",
        voltaje=12,
        stock=10
    )

    assert producto.nombre == "MAC A1 100 D"

# ============================================================
# 6. Stock aumenta → reset flags
# ============================================================
@pytest.mark.django_db
def test_stock_aumenta_resetea_flags():
    marca = Marca.objects.create(nombre="MAC")

    producto = Producto.objects.create(
        marca=marca,
        caja="A1",
        amperaje=60,
        polaridad="I",
        voltaje=12,
        stock=2,  # bajo
        notificado_stock_bajo=True,
        notificado_sin_stock=True
    )

    producto.stock = 5
    producto.save()

    assert producto.notificado_stock_bajo is False
    assert producto.notificado_sin_stock is False

# ============================================================
# 7. Stock disminuye → NO resetear flags
# ============================================================
@pytest.mark.django_db
def test_stock_disminuye_no_resetea_flags():
    marca = Marca.objects.create(nombre="MAC")

    producto = Producto.objects.create(
        marca=marca,
        caja="A1",
        amperaje=60,
        polaridad="I",
        voltaje=12,
        stock=10,
        notificado_stock_bajo=True
    )

    producto.stock = 5
    producto.save()

    assert producto.notificado_stock_bajo is True  # NO se resetea

# ============================================================
# 8. Producto sin imagen
# ============================================================
@pytest.mark.django_db
def test_producto_sin_imagen():
    marca = Marca.objects.create(nombre="MAC")

    producto = Producto.objects.create(
        marca=marca,
        caja="B2",
        amperaje=80,
        polaridad="D",
        voltaje=12,
        stock=4,
        imagen=None
    )

    assert producto.imagen == None

# ============================================================
# 9. Producto con imagen
# ============================================================
@pytest.mark.django_db
def test_producto_con_imagen():
    marca = Marca.objects.create(nombre="MAC")

    imagen = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

    producto = Producto.objects.create(
        marca=marca,
        caja="B2",
        amperaje=80,
        polaridad="D",
        voltaje=12,
        stock=4,
        imagen=imagen
    )

    assert producto.imagen is not None

# ============================================================
# 10. Asociar producto a sucursal
# ============================================================
@pytest.mark.django_db
def test_asociar_producto_sucursal():
    marca = Marca.objects.create(nombre="MAC")
    suc = Sucursal.objects.create(nombre="Bodega", direccion="Calle 1", encargado="Pedro")

    prod = Producto.objects.create(
        marca=marca,
        caja="C1",
        amperaje=90,
        polaridad="I",
        voltaje=12,
        stock=5
    )

    rel = ProductoSucursal.objects.create(producto=prod, sucursal=suc)

    assert rel.producto == prod
    assert rel.sucursal == suc



# ============================================================
# 11. Actualizar producto
# ============================================================
@pytest.mark.django_db
def test_actualizar_producto():
    marca = Marca.objects.create(nombre="MAC")

    producto = Producto.objects.create(
        marca=marca,
        caja="A1",
        amperaje=100,
        polaridad="D",
        voltaje=12,
        stock=10
    )

    producto.caja = "A2"
    producto.amperaje = 120
    producto.save()

    assert producto.nombre == "MAC A2 120 D"

# ============================================================
# 12. Eliminar producto
# ============================================================
@pytest.mark.django_db
def test_eliminar_producto():
    marca = Marca.objects.create(nombre="MAC")

    producto = Producto.objects.create(
        marca=marca,
        caja="A1",
        amperaje=100,
        polaridad="D",
        voltaje=12,
        stock=10
    )

    pk = producto.pk
    producto.delete()

    assert not Producto.objects.filter(pk=pk).exists()

# ============================================================
# 13. Validar stock mínimo
# ============================================================
@pytest.mark.django_db
def test_stock_minimo():
    marca = Marca.objects.create(nombre="MAC")

    producto = Producto.objects.create(
        marca=marca,
        caja="B1",
        amperaje=50,
        polaridad="I",
        voltaje=12,
        stock=2  # menor al mínimo
    )

    assert producto.stock < producto.stock_minimo

# ============================================================
# 14. Flags se resetean al subir stock
# ============================================================
@pytest.mark.django_db
def test_flags_reset_con_stock_alto():
    marca = Marca.objects.create(nombre="MAC")

    producto = Producto.objects.create(
        marca=marca,
        caja="B1",
        amperaje=50,
        polaridad="I",
        voltaje=12,
        stock=1,
        notificado_stock_bajo=True
    )

    producto.stock = 10
    producto.save()

    assert producto.notificado_stock_bajo is False
