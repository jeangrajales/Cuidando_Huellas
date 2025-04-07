from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
from .utils import *
from django.db import IntegrityError
from django.core.mail import send_mail 
from .forms import *
from django.utils import timezone
from datetime import datetime
from decimal import Decimal
from django.http import HttpResponse
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
                return redirect('pagina_administrador')
            elif q.rol == 2:
                return redirect('pagina_usuario')
            else:
                return render('quienes_somos')
        
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
    publicaciones = PublicacionMascota.objects.filter(tipo_publicacion='perdida').order_by('-fecha_publicacion')
    return render(request, "usuarios/mascotas_perdidas.html", {
        "publicaciones": publicaciones
    })

def adopciones(request):
    publicaciones = PublicacionMascota.objects.filter(tipo_publicacion='adopcion').order_by('-fecha_publicacion')
    return render(request, "usuarios/adopciones.html", {
        "publicaciones": publicaciones
    })

def quienes_somos(request):
    return render(request, 'quienes_somos.html')

@session_required_and_rol_permission(1, 2, 3)
def pagina_usuario(request):
    sesion = request.session.get("pista", None)

    if not sesion:
        return redirect("iniciar_sesion")

    try:
        usuario = Usuario.objects.get(id_usuario=sesion["id"])
    except Usuario.DoesNotExist:
        return HttpResponse("Usuario no encontrado", status=404)

    if request.method == "POST":
        tipo_publicacion = request.POST.get('tipo_publicacion')
        descripcion = request.POST.get('descripcion')
        nombre_mascota = request.POST.get('nombre_mascota')
        raza = request.POST.get('raza')
        edad = request.POST.get('edad')
        sexo = request.POST.get('sexo')
        contacto = request.POST.get('contacto')

        if tipo_publicacion and descripcion and nombre_mascota and raza and edad and sexo and contacto:
            publicacion = PublicacionMascota.objects.create(
                usuario=usuario,
                tipo_publicacion=tipo_publicacion,
                descripcion=descripcion,
                nombre_mascota=nombre_mascota,
                raza=raza,
                edad=edad,
                sexo=sexo,
                contacto=contacto
            )

            imagenes = request.FILES.getlist('imagenes')
            for imagen in imagenes:
                FotoMascota.objects.create(publicacion=publicacion, imagen=imagen)

            return redirect("pagina_usuario")

    publicaciones = PublicacionMascota.objects.all().order_by('-fecha_publicacion')

    return render(request, "usuarios/pagina_usuario.html", {
        "usuario": usuario,
        "publicaciones": publicaciones
    })
    
@session_required_and_rol_permission(1,2,3)
def productos_usuarios(request):
    list_productos = Producto.objects.all()
    
    # Obtener el id del usuario desde la sesión
    id_usuario = request.session.get("pista", {}).get("id")

    carrito = None
    if id_usuario:
        try:
            usuario = Usuario.objects.get(id_usuario=id_usuario)
            carrito, creado = Carrito.objects.get_or_create(usuario=usuario)
        except Usuario.DoesNotExist:
            carrito = None

    contexto = {
        "dato_producto_usuario": list_productos,
        "carrito": carrito
    }

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
        
def agregar_al_carrito(request, id_producto):
    # 1. Recuperar ID del usuario desde la sesión
    id_usuario = request.session.get("pista", {}).get("id", None)
    
    # Si no hay sesión activa, redirige
    if not id_usuario:
        return redirect("iniciar_sesion")

    try:
        # 2. Obtener usuario y producto
        usuario = Usuario.objects.get(id_usuario=id_usuario)
        producto = Producto.objects.get(id_producto=id_producto)
        
        # 3. Obtener o crear carrito para el usuario
        carrito, creado = Carrito.objects.get_or_create(usuario=usuario)
        
        # 4. Obtener o crear ítem en el carrito
        item, creado_item = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto
        )
        
        # 5. Si ya existía, solo aumenta la cantidad
        if not creado_item:
            item.cantidad += 1
            item.save()
    
    except (Usuario.DoesNotExist, Producto.DoesNotExist):
        pass  # Puedes loguear o mostrar mensaje si quieres

    return redirect("productos_usuarios")

def aumentar_cantidad(request, item_id):
    try:
        item = ItemCarrito.objects.get(id=item_id)
        item.cantidad += 1
        item.save()
    except ItemCarrito.DoesNotExist:
        pass
    return redirect('productos_usuarios')

def disminuir_cantidad(request, item_id):
    try:
        item = ItemCarrito.objects.get(id=item_id)
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
        else:
            item.delete()
    except ItemCarrito.DoesNotExist:
        pass
    return redirect('productos_usuarios')

def eliminar_item(request, item_id):
    try:
        item = ItemCarrito.objects.get(id=item_id)
        item.delete()
    except ItemCarrito.DoesNotExist:
        pass
    return redirect('productos_usuarios')

def vaciar_carrito(request):
    usuario_sesion = request.session.get("pista")
    if not usuario_sesion:
        return redirect("iniciar_sesion")

    try:
        usuario = Usuario.objects.get(id_usuario=usuario_sesion["id"])
        carrito = Carrito.objects.get(usuario=usuario)
        carrito.items.all().delete()
    except (Usuario.DoesNotExist, Carrito.DoesNotExist):
        pass
    return redirect('productos_usuarios')

def generar_factura(request):
    id_usuario = request.session.get('pista', {}).get('id')

    if not id_usuario:
        return redirect('iniciar_sesion')

    try:
        usuario = Usuario.objects.get(id_usuario=id_usuario)
        # Traer el carrito
        carrito = Carrito.objects.get(usuario=usuario)
        items = carrito.items.all()

        if not items.exists():
            messages.warning(request, "No hay productos en el carrito para facturar")
            return redirect('productos_usuarios')

        # Calcular el total exacto como decimal
        total = sum(item.subtotal() for item in items)

        # Crear factura
        factura = Factura.objects.create(
            usuario=usuario,
            fecha=timezone.now(),
            total=Decimal(total)
        )

        # Crear detalles de factura
        detalles = []
        for item in items:
            detalle = DetalleFactura.objects.create(
                factura=factura,
                producto=item.producto,
                cantidad=item.cantidad,
                subtotal=item.subtotal()
            )
            detalles.append(detalle)

            # Descontar stock del producto
            item.producto.cantidad -= item.cantidad
            item.producto.save()

        # Vaciar el carrito después de generar la factura
        items.delete()

        # Obtener fecha y hora formateadas
        fecha_actual = factura.fecha.strftime('%Y-%m-%d')
        hora_actual = factura.fecha.strftime('%H:%M:%S')

        # Redirigir a la vista de factura con todos los datos necesarios
        return render(request, 'usuarios/factura_generada.html', {
            'factura': factura,
            'detalles': detalles,
            'usuario': usuario,
            'fecha': fecha_actual,
            'hora': hora_actual
        })
    
    except (Usuario.DoesNotExist, Carrito.DoesNotExist):
        messages.error(request, "Ocurrió un error al generar la factura")
        return redirect('productos_usuarios')
    
def listar_mascotas_perdidas(request):
    list_mascotas_perdidas = PublicacionMascota.objects.all()
    contexto = {"dato_mascotas_perdidas": list_mascotas_perdidas}
    return render(request, 'administrador/mascotas/listar_mascotas_perdidas.html', contexto)

def eliminar_mascotas_perdidas(request, publicacion_id):
    try:
        traer_mascota_perdidas = PublicacionMascota.objects.get(id=publicacion_id)
        traer_mascota_perdidas.delete()
        messages.success(request, "La mascota se ha eliminado correctamente")
    except PublicacionMascota.DoesNotExist:
        messages.warning(request, "Error: La mascota  no existe")
    return redirect('listar_mascotas_perdidas')

def listar_mascotas_adopcion(request):
    list_mascotas_adopcion = PublicacionMascota.objects.filter(tipo_publicacion='adopcion')
    contexto = {"dato_mascotas_adopcion": list_mascotas_adopcion}
    return render(request, 'administrador/mascotas/listar_mascotas_adopcion.html', contexto)

def eliminar_mascotas_adopcion(request, publicacion_id):
    try:
        traer_mascota_adopcion = PublicacionMascota.objects.get(id=publicacion_id, tipo_publicacion='adopcion')
        traer_mascota_adopcion.delete()
        messages.success(request, "La mascota en adopción se ha eliminado correctamente")
    except PublicacionMascota.DoesNotExist:
        messages.warning(request, "Error: La mascota en adopción no existe")
    return redirect('listar_mascotas_adopcion')

def eliminar_publicacion(request, publicacion_id):
    try:
        id_usuario = request.session["pista"]["id"]
        usuario_actual = Usuario.objects.get(id_usuario=id_usuario)

        publicacion = PublicacionMascota.objects.get(id=publicacion_id)
        if publicacion.usuario == usuario_actual:
            publicacion.delete()
            messages.success(request, "Publicación eliminada correctamente.")
        else:
            messages.error(request, "No tienes permiso para eliminar esta publicación.")
    except Exception as e:
        print("Error al eliminar:", e)
        messages.error(request, "Ocurrió un error al intentar eliminar la publicación.")

    return redirect("pagina_usuario")