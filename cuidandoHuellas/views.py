from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
from .utils import *
from django.db import IntegrityError
from django.core.mail import send_mail 
from .forms import *
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
            messages.success(request, "Bienvenido a cuidando Huellas !!")
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
    # Metodo De la solicitud del formulario debe ser POST 
    if request.method == "POST":
        # Nos traemos los datos del formulario registrarse
        nombre_completo = request.POST.get("nombre_completo")
        telefono = request.POST.get("telefono")
        ciudad = request.POST.get("ciudad")
        correo = request.POST.get("correo")
        contraseña = request.POST.get("contraseña")
        
        # Se valida si el usuario ya existe mediante el correo electronico
        if Usuario.objects.filter(correo = correo).exists():
            messages.error(request,"Error, el correo electronico ya se encuentra registrado")
            return render(request, 'registrarse.html')
        
        #Si el usuario no existe se crea el usuario y se guarda
        else:
            crear_usuario = Usuario(
                nombre_completo = nombre_completo,
                telefono = telefono,
                ciudad = ciudad,
                correo = correo,
                contraseña = contraseña
            )
            crear_usuario.save()
            messages.success(request,"Se ha creado la cuenta correctamente, inicie sesion")
    else:
        # Si el metodo no es POST No entra por la condicion
          return render(request, "registrarse.html")     
              
    if request.session.get('pista'):
        messages.info(request, 'Ya tienes una sesion iniciada')
        return render(request,'pagina_principal.html')
    else:
        return render(request,'registrarse.html')

def pagina_principal(request):
    return render(request,'pagina_principal.html', {"mostrar_fondo": True})

def nuestros_servicios(request):
    return render(request, 'nuestros_servicios.html', {'mostrar_fondo': True})

def contactanos(request):
    
    if request.method == 'POST':
        
        nombre = request.POST.get("nombre","").strip()
        correo = request.POST.get("correo","").strip()
        mensaje = request.POST.get("mensaje","").strip()    
        
        if not nombre or not correo or not mensaje:
            messages.error(request,"Debe llenar todos los campos")
            return render(request, "contactanos.html")
        else:
            asunto = f'Nuevo mensaje de {nombre}'
            contenido = f'Correo: {correo}\n\n Mensaje:\n {mensaje}'

            send_mail(asunto, contenido, 'jean.estudio.7@gmail.com', ['cuidandohuellass@hotmail.com', "jeancg2004@hotmail.com"])
            messages.success(request, "Se ha enviado el mensaje correctamente")
            return redirect('contactanos')
    else:
        return render(request,"contactanos.html")


def mascotas_perdidas(request):
    return render(request,'mascotas_perdidas.html')

def productos(request):
    pass

def adopciones(request):
    return render(request,'adopciones.html')


# Administrador

def pagina_administrador(request):
    return render(request, 'administrador/pagina_administrador.html')

# Usuarios

def listar_usuarios(request):
    list_usuarios = Usuario.objects.all()
    contexto = {"dato": list_usuarios}
    return render(request, 'administrador/usuarios/listar_usuarios.html', contexto)

#Productos

def listar_productos(request):
    list_productos = Producto.objects.all()
    contexto = {"dato_producto": list_productos}
    return render(request, 'administrador/productos/listar_productos.html', contexto)