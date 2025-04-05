from django.contrib import messages
from django.shortcuts import redirect

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


