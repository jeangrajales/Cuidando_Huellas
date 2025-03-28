from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
from django.db import IntegrityError
# Create your views here.


def iniciar_sesion(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        contraseña = request.POST.get("contraseña")

        try:
            q = Usuario.objects.get(correo = correo, contraseña = contraseña)
            #Todo Ok si existe el usuario, crear sesion y ir al principal
            
            request.session["pista"] = {

                "id": q.id,
                "rol": q.rol,
                "nombre_completo": q.nombre_completo

            }  # Autenticacion: creamos la variable session
            messages.success(request, "Bienvenido!!")
            return redirect("nuestros_servicios")
        
        except Usuario.DoesNotExist:
            #Usuario y contraseña incorrectos
            #Devolver al login
            request.session["pista"] = None # Autenticacion: vaciamos la variable session
            messages.error(request, "Usuario o Contraseña Incorrectas...")
            return redirect("iniciar_sesion")
    else:
         # Capturamos la variable sesion
        verificar = request.session.get("pista", False) 
        if verificar:
            return redirect("pagina_principal")
        else:
            return render(request, "iniciar_sesion.html")
        
def cerrar_sesion(request):
    try:
        messages.success(request, "Cerrado correctamente la sesion")
        del request.session["pista"]
        return redirect("iniciar_sesion")
    except:
        messages.error(request, "Ocurrio un error")
        return redirect("pagina_principal")


def registrarse(request):
    return render(request,'registrarse.html')

def pagina_principal(request):
    return render(request,'pagina_principal.html')

def nuestros_servicios(request):
    return render(request, 'nuestros_servicios.html')


def mascotas_perdidas(request):
    return render(request,'mascotas_perdidas.html')

def productos(request):
    pass

def adopciones(request):
    return render(request,'adopciones.html')