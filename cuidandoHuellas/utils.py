from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import EmailMessage

def session_required_and_rol_permission(*roles):
	def decorador(func):
		def decorada(*args, **kwargs):
			autenticado = args[0].session.get("pista", False)
			if autenticado:
				if len(roles) == 0 or (autenticado["rol"] in roles):
					print(f"Sesión OK y Rol Ok: {autenticado['rol']}")
					return func(*args, **kwargs)
				else:
					messages.info(args[0], "Usted no está autorizado...")
					return redirect("pagina_principal")
			else:
				messages.warning(args[0], "Usted no ha iniciado sesión...")
				return redirect("iniciar_sesion")
		return decorada
	return decorador


def send_email_with_attachment(subject, body, to_emails, attachments=None, from_email=None):
    """
    Envía un correo electrónico con posibilidad de archivos adjuntos.
    """

    email = EmailMessage(
        subject,
        body,
        from_email,
        to_emails
    )

    if attachments:
        for filename, content, mimetype in attachments:
            email.attach(filename, content, mimetype)

    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False