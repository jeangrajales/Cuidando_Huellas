from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
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
import os
from PIL import Image
from io import BytesIO

# Create your views here.

# Usuarios

# -------------------
@session_required_and_rol_permission(1)  # Solo para rol 1 (admin)
def panel_administrador(request):
    return render(request, 'administrador/pagina_administrador.html')

def iniciar_sesion(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        contraseña = request.POST.get("contraseña")

        try:
            q = Usuario.objects.get(correo=correo)
            # Validar la contraseña encriptada
            if check_password(contraseña, q.contraseña):
                # Todo OK si la contraseña coincide, crear sesión y redirigir
                request.session["pista"] = {
                "telefono": q.telefono,
                "id": q.id_usuario,
                "rol": q.rol,
                "nombre_completo": q.nombre_completo,
                "es_administrador": q.es_administrador,  # Usando la propiedad
            }# Autenticación: creamos la variable session
                messages.success(request, "Bienvenido a Cuidando Huellas !!")

                if q.rol == 1:  
                    return redirect("pagina_administrador")
                elif q.rol == 2:
                    return render(request, "usuarios/pagina_usuario.html")
            else:
                # Contraseña incorrecta
                messages.error(request, "Usuario o contraseña incorrectos...")
                return redirect("iniciar_sesion")

        except Usuario.DoesNotExist:
            # Usuario no existe
            request.session["pista"] = None  # Autenticación: vaciamos la variable session
            messages.error(request, "El usuario no existe")
            return redirect("iniciar_sesion")
    else:
        # Capturamos la variable sesión
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
    if request.method == "POST":
        nombre_completo = request.POST.get("nombre_completo")
        telefono = request.POST.get("telefono")
        ciudad = request.POST.get("ciudad")
        correo = request.POST.get("correo")
        contraseña = request.POST.get("contraseña")
        confirmar_contraseña = request.POST.get("confirmar_contraseña")

        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "El correo electrónico ya está registrado")
            return render(request, 'usuarios/registrarse.html')

        if contraseña.strip() != confirmar_contraseña:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, 'usuarios/registrarse.html')

        crear_usuario = Usuario(
            nombre_completo=nombre_completo,
            telefono=telefono,
            ciudad=ciudad,
            correo=correo,
            contraseña=contraseña  # Contraseña encriptada
        )

        try:
            crear_usuario.full_clean()
            crear_usuario.save()
            messages.success(request, "Cuenta creada exitosamente, por favor inicia sesión.")
            return render(request,'usuarios/pagina_usuario.html')
        
        except ValidationError as e:
            for field, error_list in e.message_dict.items():
                for error in error_list:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'usuarios/registrarse.html')

    return render(request, "usuarios/registrarse.html")

@session_required_and_rol_permission(1,2,3)
def editar_usuario(request):
    return render(request, 'usuarios/editar_usuario.html')

def pagina_principal(request):
    return render(request, 'pagina_principal.html')
    

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
    # Productos normales
    list_productos = Producto.objects.all()
    
    # Productos más vendidos (ordenados por veces_comprado y fecha reciente)
    productos_mas_vendidos = Producto.objects.filter(veces_comprado__gt=0)\
                              .order_by('-veces_comprado', '-ultima_compra')[:8]
    
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
        "productos_mas_vendidos": productos_mas_vendidos,
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
        if traer_usuarios.rol == 1:
            messages.error(request,'Error, el administrador no se puede eliminar')
        else:
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
        
        try:
            precio = float(precio)
            if precio <= 0:
                messages.error(request, "Error: El precio debe ser mayor a 0")
                return redirect('agregar_productos')
        except (ValueError, TypeError):
            messages.error(request, "Error: Ingrese un precio válido")
            return redirect('agregar_productos')
            
        try:
            cantidad = int(cantidad)
            if cantidad < 1:
                messages.error(request, "Error: La cantidad debe ser al menos 1")
                return redirect('agregar_productos')
        except (ValueError, TypeError):
            messages.error(request, "Error: Ingrese una cantidad válida")
            return redirect('agregar_productos')
        
        # Validación del archivo de imagen
        if foto_producto:
            # 1. Validar extensión del archivo
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            ext = os.path.splitext(foto_producto.name)[1].lower()
            
            if ext not in allowed_extensions:
                messages.error(request, "Error: Solo se permiten imágenes (JPG, JPEG, PNG, GIF, WEBP)")
                return redirect('agregar_productos')
            
            # 2. Validar que el archivo sea realmente una imagen
            try:
                # Leer los primeros bytes para verificar el tipo de archivo
                image_header = foto_producto.read(1024)
                foto_producto.seek(0)  # Rebobinar el archivo
                
                # Verificar cabeceras de imagen conocidas
                if not any(
                    image_header.startswith(signature) for signature in [
                        b'\xFF\xD8\xFF',  # JPEG
                        b'\x89PNG',       # PNG
                        b'GIF87a',        # GIF
                        b'GIF89a',        # GIF
                        b'RIFF....WEBPVP' # WEBP (simplificado)
                    ]
                ):
                    messages.error(request, "Error: El archivo no es una imagen válida")
                    return redirect('agregar_productos')
                
                # 3. Validación más estricta con PIL
                try:
                    img = Image.open(foto_producto)
                    img.verify()  # Verifica que sea una imagen válida
                    foto_producto.seek(0)  # Rebobinar para guardar
                    
                    # 4. Validar tamaño máximo del archivo (5MB)
                    max_size_bytes = 5 * 1024 * 1024
                    if foto_producto.size > max_size_bytes:
                        messages.error(request, "Error: La imagen es demasiado grande (máximo 5MB)")
                        return redirect('agregar_productos')
                        
                except Exception as e:
                    messages.error(request, "Error: El archivo no es una imagen válida o está corrupto")
                    return redirect('agregar_productos')
                    
            except Exception as e:
                messages.error(request, "Error al procesar la imagen")
                return redirect('agregar_productos')
        
        # Resto de tu lógica...
        if Producto.objects.filter(nombre_producto=nombre_producto).exists():
            messages.error(request, "Error: Ya existe un producto con este nombre")
            return redirect('agregar_productos')
        else:
            crear_producto = Producto(
                nombre_producto=nombre_producto,
                precio=precio,
                cantidad=cantidad,
                descripcion=descripcion,
                foto_producto=foto_producto,
                categoria=categoria,
                estado=estado
            )
            crear_producto.save()
            messages.success(request, "Se agregó producto exitosamente")
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

def modal_carrito(request):
    return render(request,'usuarios/modal_carrito.html')

@session_required_and_rol_permission(1,2,3)
def agregar_al_carrito(request, id_producto):
    id_usuario = request.session.get("pista", {}).get("id", None)
    
    if not id_usuario:
        return redirect("iniciar_sesion")

    try:
        usuario = Usuario.objects.get(id_usuario=id_usuario)
        producto = Producto.objects.get(id_producto=id_producto)
        
        if producto.cantidad <= 0:
            messages.error(request, f"El producto '{producto.nombre_producto}' está agotado.")
            return redirect("productos_usuarios")

        # Obtener o crear carrito para el usuario
        carrito, creado = Carrito.objects.get_or_create(usuario=usuario)
        
        # Obtener o crear ítem en el carrito
        item, creado_item = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto
        )
        
        if not creado_item:
            item.cantidad += 1
            item.save()
            
        messages.success(request, f"¡{producto.nombre_producto} agregado al carrito!")
    
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado")
    except Producto.DoesNotExist:
        messages.error(request, "Producto no encontrado")

    return redirect("productos_usuarios")

@session_required_and_rol_permission(1,2,3)
def aumentar_cantidad(request, item_id):
    try:
        # Obtener el ítem del carrito
        item = ItemCarrito.objects.get(id=item_id)

        # Asegúrate de que item.producto es un objeto Producto
        producto = item.producto

        # Verificar el stock del producto
        if item.cantidad >= producto.cantidad:
            messages.error(request, f"Solo quedan {producto.cantidad} unidades disponibles.")

        # Aumentar la cantidad
        item.cantidad += 1
        item.save()
        messages.success(request, f"Cantidad aumentada para {producto.nombre_producto}.")
    except ItemCarrito.DoesNotExist:
        messages.error(request, "El ítem no existe.")
    except Exception as e:
        messages.error(request, f"Ocurrió un error: {str(e)}")
    return redirect('productos_usuarios')

@session_required_and_rol_permission(1,2,3)
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
        carrito = Carrito.objects.get(usuario=usuario)
        items = carrito.items.all()

        if not items.exists():
            messages.warning(request, "No hay productos en el carrito para facturar")
            return redirect('productos_usuarios')

        total = sum(item.subtotal() for item in items)

        # Crear factura
        factura = Factura.objects.create(
            usuario=usuario,
            fecha=timezone.now(),
            total=Decimal(total)
        )

        # Crear detalles de factura y actualizar contadores
        detalles = []
        for item in items:
            # Incrementar contador de compras SOLO AQUÍ
            item.producto.veces_comprado += item.cantidad
            item.producto.ultima_compra = timezone.now()
            item.producto.save()

            detalle = DetalleFactura.objects.create(
                factura=factura,
                producto=item.producto,
                cantidad=item.cantidad,
                subtotal=item.subtotal()
            )
            detalles.append(detalle)

            # Descontar stock
            item.producto.cantidad -= item.cantidad
            item.producto.save()

        # Vaciar carrito
        items.delete()

        fecha_actual = factura.fecha.strftime('%Y-%m-%d')
        hora_actual = factura.fecha.strftime('%H:%M:%S')

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
