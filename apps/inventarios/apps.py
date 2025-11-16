from django.apps import AppConfig
import threading
import time
import sys
import os


class InventariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.inventarios'

    def ready(self):
        """
        Este método se ejecuta cuando Django arranca la app.
        Aquí lanzamos un hilo que llama revisar_alertas() cada X minutos,
        pero solo cuando se ejecuta el servidor (runserver).
        """
        # Evitar que se ejecute en procesos que no sean el servidor
        if 'runserver' not in sys.argv:
            return

        # Evitar que el hilo se ejecute dos veces por el autoreloader
        if os.environ.get('RUN_MAIN') != 'true':
            return

        from apps.inventarios.telegram_alertas import revisar_alertas

        def scheduler():
            while True:
                print("▶ Ejecutando revisar_alertas() desde scheduler interno...")
                try:
                    revisar_alertas()
                    print("✅ Revisión de alertas completada.")
                except Exception as e:
                    print("❌ Error en scheduler de alertas:", e)
                # Esperar 10 minutos (600 segundos)
                time.sleep(30)

        # Lanzar el hilo en segundo plano
        hilo = threading.Thread(target=scheduler, daemon=True)
        hilo.start()
