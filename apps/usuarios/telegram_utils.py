import requests
from django.conf import settings


def enviar_telegram(chat_id: int | str, texto: str):
    """
    Envía un mensaje de texto a un chat de Telegram usando el bot.
    chat_id puede ser un ID de usuario o de grupo (suele ser int o string).
    """
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN no está configurado en settings.")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": texto,
    }

    response = requests.post(url, data=data)
    # Opcional: puedes hacer debug si algo sale mal
    try:
        response.raise_for_status()
    except Exception as e:
        # En proyectos reales podrías loguear esto
        print("Error enviando mensaje a Telegram:", e, response.text)
