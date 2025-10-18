from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

@reset_password_token_created.connect
def send_password_reset_email(sender, instance, reset_password_token, *args, **kwargs):
    subject = "Recuperación de contraseña - PowerStock"
    message = f"""
    Hola,

    Has solicitado restablecer tu contraseña.
    
    Tu token de recuperación es:  {reset_password_token.key}

    Si no solicitaste esto, ignora este mensaje.
    """
    send_mail(subject, message, "powerstock2025@gmail.com", [reset_password_token.user.email])
