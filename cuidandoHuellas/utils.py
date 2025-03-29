from django.contrib import messages
from django.shortcuts import redirect

def session_rol_permission(roles):
    def decorador(func):
        def decorada(request,args, kwargs):
            autenticado = request.session.get("pista", False)
            if autenticado:
                if len(roles) == 0 or (autenticado["rol"] in roles):
                    print(f"Sesion y Rol OK: {autenticado['rol']}")
                    return func(request, *args, kwargs)
                else:
                    messages.info(request, "Usted no esta autorizado")
                    return redirect("pagina_principal")
            else:
                messages.warning(request, "Usted no ha iniciado sesion")
                return redirect("iniciar_sesion")
        return decorada
    return decorador