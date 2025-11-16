from django.core.management.base import BaseCommand
from apps.inventarios.telegram_alertas import revisar_alertas

class Command(BaseCommand):
    help = "Revisa stock y garantías y envía alertas por Telegram"

    def handle(self, *args, **kwargs):
        revisar_alertas()
        self.stdout.write(self.style.SUCCESS("Proceso de alertas ejecutado correctamente"))
