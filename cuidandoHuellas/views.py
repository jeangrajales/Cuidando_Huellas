from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
from .utils import *
from django.db import IntegrityError
from django.core.mail import send_mail 
from .forms import *
# Create your views here.

# Usuarios

# -------------------

def iniciar_sesion(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        contraseña = request.POST.get("contraseña")

        try:
            q = Usuario.objects.get(correo = correo, contraseña = contraseña)
            #Todo Ok si existe el usuario, crear sesion y ir al principal
            
            request.session["pista"] = {
                "telefono": q.telefono,
                "id": q.id_usuario,
                "rol": q.rol,
                "nombre_completo": q.nombre_completo

            }  # Autenticacion: creamos la variable session
            messages.success(request, "Bienvenido a cuidando Huellas !!")
            
            if q.rol == 1:
                return render(request, 'administrador/pagina_administrador.html')
            elif q.rol == 2:
                return render(request, 'usuarios/pagina_usuario.html')
            else:
                return render(request, 'quienes_somos.html')
        
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
            return render(request, "usuarios/iniciar_sesion.html")
        
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
            return render(request, 'usuarios/registrarse.html')
        
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
            return redirect('pagina_usuario')
    else:
        # Si el metodo no es POST No entra por la condicion
          return render(request, "usuarios/registrarse.html")     
              
    if request.session.get('pista'):
        messages.info(request, 'Ya tienes una sesion iniciada')
        return render(request,'pagina_principal.html')
    else:
        return render(request,'usuarios/registrarse.html')

def pagina_principal(request):
    return render(request, 'pagina_principal.html')
    
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

@session_required_and_rol_permission(1,2,3)
def mascotas_perdidas(request):
    return render(request,'usuarios/mascotas_perdidas.html')

def adopciones(request):
    return render(request,'usuarios/adopciones.html')

def quienes_somos(request):
    return render(request, 'quienes_somos.html')

@session_required_and_rol_permission(1,2,3)
def pagina_usuario(request):
    return render(request, 'usuarios/pagina_usuario.html' )

@session_required_and_rol_permission(1,2,3)
def productos_usuarios(request):
    list_productos = Producto.objects.all()
    contexto = {"dato_producto_usuario": list_productos}
    return render(request, 'usuarios/productos_usuarios.html', contexto)

@session_required_and_rol_permission(1,2,3)
def veterinarias_asociadas(request):
    return render(request,'usuarios/veterinarias_asociadas.html')

def producto_compra(request):
    return render(request, 'usuarios/producto_compra.html')

# --------------------------------------------------------------
# Administrador

@session_required_and_rol_permission(1)
def pagina_administrador(request):
    return render(request, 'administrador/pagina_administrador.html')

@session_required_and_rol_permission(1)
def listar_usuarios(request):
    list_usuarios = Usuario.objects.all()
    contexto = {"dato": list_usuarios}
    return render(request, 'administrador/usuarios/listar_usuarios.html', contexto)

@session_required_and_rol_permission(1)
def eliminar_usuarios(request, id_usuario):
    try:
        traer_usuarios = Usuario.objects.get(pk = id_usuario)
        traer_usuarios.delete()
        messages.success(request,"Usuario eliminado correctamente")
    except Usuario.DoesNotExist:
        messages.warning(request, "Error: El usuario no existe")
    return redirect('listar_usuarios')

@session_required_and_rol_permission(1)
def listar_productos(request):
    list_productos = Producto.objects.all()
    contexto = {"dato_producto": list_productos}
    return render(request, 'administrador/productos/listar_productos.html', contexto)



    

@session_required_and_rol_permission(1)
def agregar_productos(request):
    if request.method == "POST":
        nombre_producto = request.POST.get("nombre_producto")
        precio = request.POST.get("precio")
        cantidad = request.POST.get("cantidad")
        descripcion = request.POST.get("descripcion")
        foto_producto = request.FILES.get("foto_producto")
        categoria = request.POST.get("categoria")
        estado = request.POST.get("estado")
        
        if Producto.objects.filter(nombre_producto = nombre_producto).exists():
            messages.error(request,"Error: Ya existe un producto con este nombre")
            return redirect('agregar_productos')
        else:
            crear_producto = Producto(
                nombre_producto = nombre_producto,
                precio = precio,
                cantidad = cantidad,
                descripcion = descripcion,
                foto_producto = foto_producto,
                categoria = categoria,
                estado = estado
            )
            crear_producto.save()
            messages.success(request, "Se agrego producto exitosamente")
            return redirect('listar_productos')
    else:
        return render(request, "administrador/productos/agregar_productos.html")
    
@session_required_and_rol_permission(1)
def eliminar_productos(request, id_producto):
    try:
        traer_producto = Producto.objects.get(pk = id_producto)
        traer_producto.delete()
        messages.success(request, "El producto se ha eliminado correctamente")
    except Producto.DoesNotExist:
        messages.warning(request, "Error: El producto no existe")
    return redirect('listar_productos')

@session_required_and_rol_permission(1)
def editar_productos(request, id_producto):
    try:
        traer_producto = Producto.objects.get(pk = id_producto)
    
    except Producto.DoesNotExist:
        messages.error(request,"Error Capa 8: El producto no existe")
        return redirect('listar productos')
    
    if request.method == 'POST':
        nombre_producto = request.POST.get("nombre_producto")
        precio = request.POST.get("precio")
        cantidad = request.POST.get("cantidad")
        descripcion = request.POST.get("descripcion")
        foto_producto = request.FILES.get("foto_producto")
        categoria = request.POST.get("categoria")
        estado = request.POST.get("estado")
        
        traer_producto.nombre_producto = nombre_producto
        traer_producto.precio = precio
        traer_producto.cantidad = cantidad
        traer_producto.descripcion = descripcion
        traer_producto.foto_producto = foto_producto
        traer_producto.categoria = categoria
        traer_producto.estado = estado
        traer_producto.save()
        messages.success(request, "Se ha actualizado el producto correctamente")
        return redirect('listar_productos')
        
    else:
        traer_producto = Producto.objects.get(pk=id_producto)
        return render(request, "administrador/productos/agregar_productos.html", {"dato": traer_producto})
        
