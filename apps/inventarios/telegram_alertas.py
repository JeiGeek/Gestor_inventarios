from datetime import date, timedelta

from django.conf import settings
from django.db.models import F

from apps.productos.models import Producto
from apps.garantias.models import Garantia
from apps.usuarios.telegram_utils import enviar_telegram


def revisar_alertas():
    chat_id = settings.TELEGRAM_DEFAULT_CHAT_ID
    if not chat_id:
        print("⚠️ TELEGRAM_DEFAULT_CHAT_ID no está configurado.")
        return

    hoy = date.today()
    dias_aviso = 8

    # 1) STOCK BAJO
    productos_bajo_stock = Producto.objects.filter(
        stock__gt=0,
        stock__lte=F("stock_minimo"),
        notificado_stock_bajo=False,
    )

    for p in productos_bajo_stock:
        mensaje = (
            f"⚠️ Stock bajo\n\n"
            f"Producto: {p.nombre}\n"
            f"Stock actual: {p.stock}\n"
            f"Stock mínimo: {p.stock_minimo}"
        )
        enviar_telegram(chat_id, mensaje)
        p.notificado_stock_bajo = True
        p.save(update_fields=["notificado_stock_bajo"])

    # 2) SIN STOCK
    productos_sin_stock = Producto.objects.filter(
        stock__lte=0,
        notificado_sin_stock=False,
    )

    for p in productos_sin_stock:
        mensaje = (
            f"⛔ Sin stock\n\n"
            f"Producto: {p.nombre}\n"
            f"Stock actual: {p.stock}"
        )
        enviar_telegram(chat_id, mensaje)
        p.notificado_sin_stock = True
        p.save(update_fields=["notificado_sin_stock"])

    # 3) GARANTÍAS POR VENCER
    limite_aviso = hoy + timedelta(days=dias_aviso)

    garantias_por_vencer = Garantia.objects.filter(
        fecha_fin_garantia__gte=hoy,
        fecha_fin_garantia__lte=limite_aviso,
        notificada_por_vencer=False,
    )

    for g in garantias_por_vencer:
        mensaje = (
            f"📅 Garantía por vencer\n\n"
            f"Producto: {g.producto.nombre}\n"
            f"Sucursal: {g.sucursal.nombre}\n"
            f"Serial: {g.serial}\n"
            f"Fecha fin garantía: {g.fecha_fin_garantia}\n"
            f"Días restantes: {g.dias_restantes}"
        )
        enviar_telegram(chat_id, mensaje)
        g.notificada_por_vencer = True
        g.save(update_fields=["notificada_por_vencer"])

    # 4) GARANTÍAS VENCIDAS
    garantias_vencidas = Garantia.objects.filter(
        fecha_fin_garantia__lt=hoy,
        notificada_vencida=False,
    )

    for g in garantias_vencidas:
        mensaje = (
            f"❌ Garantía vencida\n\n"
            f"Producto: {g.producto.nombre}\n"
            f"Sucursal: {g.sucursal.nombre}\n"
            f"Serial: {g.serial}\n"
            f"Fecha fin garantía: {g.fecha_fin_garantia}"
        )
        enviar_telegram(chat_id, mensaje)
        g.notificada_vencida = True
        g.save(update_fields=["notificada_vencida"])

    print("✅ Revisión de alertas finalizada.")