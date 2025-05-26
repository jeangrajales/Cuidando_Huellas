from django.shortcuts import render, redirect, get_object_or_404
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
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import TicketSoporte, RespuestaTicket, EstadoTicket, PreguntaFrecuente, CategoriaTicket
from .forms import TicketSoporteForm, RespuestaTicketForm, FiltroTicketsForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Case, When, Value, IntegerField
from django.views.decorators.http import require_POST
# Create your views here.

# Usuarios
from django.core.exceptions import ValidationError
import re
from django.core.mail import send_mail
from django.conf import settings
# -------------------

def correos1(request):
    try:
        send_mail(
            "Cuidando Huellas - Pruebas",
            "Mensaje de prueba para Yoiner: Te quiero, De Valentina....... <strong> desde </strong> Django",
            settings.EMAIL_HOST_USER,       # correo de la aplicación settings.py
            ["jean.estudio.7@gmail.com"],    # correo destino
            fail_silently=False,
        )
        return HttpResponse(f"Correo enviado!!")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    
def correos2(request):
    try:
        html_message = """
            Hola Profe <strong style='color:red;'>Los mejores </strong> desde mi app Cuidando HUellas...
            <br>
            Bienvenido!!
        """
        send_mail(
            "Cuidando_Huellas",
            "",     # mensaje anterior vacío
            settings.EMAIL_HOST_USER,         # correo de la aplicación settings.py
            ["misena.jor@gmail.com"],    # correo destino
            fail_silently=False,
            html_message=html_message
        )

        return HttpResponse("Correo enviado!! Gracias")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    
def correos3(request):
    import os
    # envío de correo con .zip adjunto
    
    subject = "Cuidando Huellas - Backup"
    body = "Archivo adjunto de la aplicación - Cuidando Huellas"
    to_emails = ['misena.jor@gmail.com']
    archivo_adjunto = '/home/tarde/Cuidando_Huellas/db.sqlite3.zip'

    # Ejemplo de un archivo adjunto (podrías leerlo de un archivo real)
    file_path = archivo_adjunto
    if os.path.exists(archivo_adjunto):
        with open(file_path, 'rb') as f:
            file_content = f.read()
        attachments = [('db.sqlite3.zip', file_content, 'application/zip')]
    else:
        attachments = None

    if send_email_with_attachment(subject, body, to_emails, attachments, settings.EMAIL_HOST_USER):
        print("Correo electrónico enviado con éxito.")
        return HttpResponse("Correo electrónico enviado con éxito.")
    else:
        print("Error al enviar el correo electrónico.")
        return HttpResponse("Error al enviar el correo electrónico.")

def iniciar_sesion(request):
    datos_form = {}  # Diccionario para mantener los datos del formulario
    
    if request.method == "POST":
        correo = request.POST.get("correo")
        contraseña = request.POST.get("contraseña")
        
        # Guardamos los datos del formulario (excepto la contraseña por seguridad)
        datos_form = {'correo': correo}
        
        try:
            q = Usuario.objects.get(correo=correo)
            # Validar la contraseña encriptada
            if check_password(contraseña, q.contraseña):
                # Todo OK si la contraseña coincide, crear sesión y redirigir
                request.session["pista"] = {
                    "foto_perfil": q.foto_perfil.url if q.foto_perfil else None,
                    "telefono": q.telefono,
                    "id": q.id_usuario,
                    "rol": q.rol,
                    "nombre_completo": q.nombre_completo,
                    "es_administrador": q.es_administrador,
                }
                messages.success(request, "Bienvenido a Cuidando Huellas !!")
                
                if q.rol == 1:
                    return redirect("pagina_administrador")
                elif q.rol == 2:
                    return redirect("pagina_usuario")
            else:
                # Contraseña incorrecta
                messages.error(request, "Usuario o contraseña incorrectos...")
                return render(request, "usuarios/iniciar_sesion.html", {'datos_form': datos_form})
                
                
        except Usuario.DoesNotExist:
            # Usuario no existe
            request.session["pista"] = None
            messages.error(request, "El usuario no existe")
            return render(request, "usuarios/iniciar_sesion.html", {'datos_form': datos_form})
    else:
        # Capturamos la variable sesión
        verificar = request.session.get("pista", False)
        if verificar:
            return redirect("pagina_principal")
    
    return render(request, "usuarios/iniciar_sesion.html", {'datos_form': datos_form})

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
        # Obtener los datos del formulario
        form_data = {
            'nombre_completo': request.POST.get("nombre_completo"),
            'telefono': request.POST.get("telefono"),
            'ciudad': request.POST.get("ciudad"),
            'correo': request.POST.get("correo"),
        }
        
        contraseña = request.POST.get("contraseña")
        confirmar_contraseña = request.POST.get("confirmar_contraseña")

        # Verificar si el correo ya existe
        if Usuario.objects.filter(correo=form_data['correo']).exists():
            messages.error(request, "El correo electrónico ya está registrado")
            return render(request, 'usuarios/registrarse.html', {'form_data': form_data})

        # Verificar que las contraseñas coincidan
        if contraseña.strip() != confirmar_contraseña.strip():
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, 'usuarios/registrarse.html', {'form_data': form_data})

        try:
            # Crear el usuario
            crear_usuario = Usuario(
                nombre_completo=form_data['nombre_completo'],
                telefono=form_data['telefono'],
                ciudad=form_data['ciudad'],
                correo=form_data['correo'],
                contraseña=contraseña  # Contraseña encriptada
            )

            crear_usuario.full_clean()
            crear_usuario.save()

            # Iniciar sesión directamente
            request.session['pista'] = {
                'id': crear_usuario.id_usuario,
                'nombre_completo': crear_usuario.nombre_completo,
                'correo': crear_usuario.correo,
                'rol': crear_usuario.rol
            }
            messages.success(request, "Bienvenido " +  crear_usuario.nombre_completo  + ", Disfruta de nuestros Servicios")
            return redirect('pagina_usuario')

        except ValidationError as e:
            for field, error_list in e.message_dict.items():
                for error in error_list:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'usuarios/registrarse.html', {'form_data': form_data})

    # Si es GET, mostrar formulario vacío
    return render(request, "usuarios/registrarse.html")

@session_required_and_rol_permission(1, 2, 3)
def editar_usuario(request):
    # Verificar sesión y obtener usuario
    try:
        usuario_session = request.session.get("pista")
        if not usuario_session:
            messages.error(request, 'Debes iniciar sesión primero')
            return redirect('iniciar_sesion')
            
        usuario_obj = Usuario.objects.get(id_usuario=usuario_session["id"])
    except KeyError:
        messages.error(request, 'Información de sesión incompleta')
        return redirect('iniciar_sesion')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('pagina_principal')
    except Exception as e:
        messages.error(request, f'Error al cargar el perfil: {str(e)}')
        return redirect('pagina_principal')

    if request.method == 'POST':
        try:
            # Procesar datos básicos
            usuario_obj.nombre_completo = request.POST.get('name', usuario_obj.nombre_completo)
            usuario_obj.telefono = request.POST.get('phone', usuario_obj.telefono)
            usuario_obj.ciudad = request.POST.get('city', usuario_obj.ciudad)
            
            # Bandera para saber si cambió la foto
            foto_actualizada = False
            
            # Procesar foto de perfil
            if 'profilePicInput' in request.FILES:
                foto = request.FILES['profilePicInput']
                
                # Validar imagen
                if foto.size > 5 * 1024 * 1024:  # 5MB máximo
                    messages.error(request, 'La imagen es demasiado grande (máximo 5MB)')
                    return redirect('editar_usuario')
                
                if not foto.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    messages.error(request, 'Formato no válido. Use JPG, JPEG o PNG.')
                    return redirect('editar_usuario')
                
                # Guardar la nueva imagen con timestamp para evitar caché
                timestamp = str(now().timestamp()).replace('.', '')
                fs = FileSystemStorage()
                
                # Eliminar imagen anterior si existe
                if usuario_obj.foto_perfil:
                    try:
                        if os.path.exists(usuario_obj.foto_perfil.path):
                            os.remove(usuario_obj.foto_perfil.path)
                    except Exception as e:
                        print(f"Error eliminando imagen anterior: {str(e)}")
                
                # Guardar nueva imagen
                filename = fs.save(
                    f'perfiles/user_{usuario_obj.id_usuario}_{timestamp}.jpg', 
                    foto
                )
                usuario_obj.foto_perfil = filename
                foto_actualizada = True
                messages.success(request, 'Foto de perfil actualizada correctamente')
            
            # Procesar cambio de contraseña
            current_password = request.POST.get('currentPassword')
            new_password = request.POST.get('newPassword')
            confirm_password = request.POST.get('confirmPassword')
            
            if current_password or new_password or confirm_password:
                if not all([current_password, new_password, confirm_password]):
                    messages.error(request, 'Complete todos los campos para cambiar la contraseña')
                    return redirect('editar_usuario')
                
                if not usuario_obj.check_password(current_password):
                    messages.error(request, 'Contraseña actual incorrecta')
                    return redirect('editar_usuario')
                
                if new_password != confirm_password:
                    messages.error(request, 'Las nuevas contraseñas no coinciden')
                    return redirect('editar_usuario')
                
                if len(new_password) < 8:
                    messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
                    return redirect('editar_usuario')
                
                usuario_obj.contraseña = make_password(new_password)
                messages.success(request, 'Contraseña actualizada correctamente')
            
            # Guardar todos los cambios
            usuario_obj.save()
            
            # Actualizar sesión con timestamp para evitar caché
            foto_url = usuario_obj.foto_perfil.url if usuario_obj.foto_perfil else None
            if foto_url and foto_actualizada:
                foto_url += f"?v={timestamp}"
            
            request.session['pista'] = {
                'id': usuario_obj.id_usuario,
                'nombre_completo': usuario_obj.nombre_completo,
                'telefono': usuario_obj.telefono,
                'rol': usuario_obj.rol,
                'es_administrador': usuario_obj.es_administrador,
                'foto_perfil': foto_url
            }
            request.session.modified = True
            
            # Forzar actualización de publicaciones (opcional)
            if foto_actualizada:
                from django.db.models import F
                PublicacionMascota.objects.filter(usuario=usuario_obj).update(
                    fecha_publicacion=F('fecha_publicacion')
                )
            
            return redirect('pagina_usuario')  # Redirigir a la página de usuario
            
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')
            return redirect('editar_usuario')
    
    # GET request - Mostrar formulario
    context = {'usuario': usuario_obj}
    return render(request, 'usuarios/editar_usuario.html', context)

def pagina_principal(request):
    publicaciones = PublicacionMascota.objects.all().order_by('-fecha_publicacion')
    productos = Producto.objects.all()  # Obtenemos todos los productos
    return render(request, "pagina_principal.html", {
        "publicaciones": publicaciones,
        "productos": productos  # Pasamos los productos al contexto
    })

    

@session_required_and_rol_permission(1,2,3)
def mascotas_perdidas(request):
    publicaciones = PublicacionMascota.objects.filter(tipo_publicacion='perdida').order_by('-fecha_publicacion')
    return render(request, "usuarios/mascotas_perdidas.html", {
        "publicaciones": publicaciones
    })

@session_required_and_rol_permission(1,2,3)
def adopciones(request):
    # Obtener parámetros de filtrado del request
    edad = request.GET.get('edad', '')
    sexo = request.GET.get('sexo', '')
    
    # Filtrar solo publicaciones de adopción
    publicaciones = PublicacionMascota.objects.filter(tipo_publicacion='adopcion')
    
    # Aplicar filtros si existen
    if edad:
        if edad == 'cachorro':
            publicaciones = publicaciones.filter(edad__lte=2)
        elif edad == 'joven':
            publicaciones = publicaciones.filter(edad__range=(3, 5))
        elif edad == 'adulto':
            publicaciones = publicaciones.filter(edad__range=(6, 8))
        elif edad == 'mayor':
            publicaciones = publicaciones.filter(edad__gt=8)
    
    if sexo:
        publicaciones = publicaciones.filter(sexo=sexo)
    
    # Ordenar por fecha más reciente primero
    publicaciones = publicaciones.order_by('-fecha_publicacion')
    
    # Si es una petición AJAX, devolver solo el partial
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'usuarios/lista_adopciones.html', {
            'publicaciones': publicaciones
        })
    
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
    
    # Datos del formulario que se preservarán en caso de error
    form_data = {
        'tipo_publicacion': '',
        'descripcion': '',
        'nombre_mascota': '',
        'raza': '',
        'edad': '',
        'sexo': '',
        'contacto': ''
    }

    if request.method == "POST":
        try:
            # Obtener datos del formulario
            tipo_publicacion = request.POST.get('tipo_publicacion')
            descripcion = request.POST.get('descripcion', '').strip()
            nombre_mascota = request.POST.get('nombre_mascota', '').strip()
            raza = request.POST.get('raza', '').strip()
            edad = request.POST.get('edad', '').strip()
            sexo = request.POST.get('sexo', '').strip() 
            contacto = request.POST.get('contacto', '').strip()
            imagenes = request.FILES.getlist('imagenes')

            # Validaciones específicas según tus requerimientos
            if tipo_publicacion not in ['perdida', 'adopcion']:
                raise ValidationError("Debes seleccionar un tipo de publicación válido")
            
            if not descripcion or len(descripcion) < 10:
                raise ValidationError("La descripción debe tener al menos 10 caracteres")

            if nombre_mascota and not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', nombre_mascota):
                raise ValidationError("El nombre de la mascota solo puede contener letras y espacios")

            if raza and not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', raza):
                raise ValidationError("La raza solo puede contener letras y espacios")

            if edad:
                try:
                    edad_int = int(edad)
                    if edad_int < 1 or edad_int > 15:
                        raise ValidationError("La edad debe estar entre 1 y 15 años")
                    # Guardamos la edad validada
                    form_data['edad'] = str(edad_int)
                except ValueError:
                    raise ValidationError("La edad debe ser un número válido")
                
            if not sexo or sexo not in ['Hembra', 'Macho']:
                raise ValidationError("Selecciona un sexo válido (Macho o Hembra)")

            if contacto and not re.match(r'^\d{7,15}$', contacto):
                raise ValidationError("El contacto debe contener entre 7 y 15 dígitos")

            if not imagenes:
                raise ValidationError("Debes subir al menos una imagen")

            # Validar imágenes
            for imagen in imagenes:
                # Validar extensión
                allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
                ext = os.path.splitext(imagen.name)[1].lower()
                if ext not in allowed_extensions:
                    raise ValidationError("Solo se permiten imágenes (JPG, JPEG, PNG, GIF, WEBP)")

                # Validar tamaño (5MB máximo)
                if imagen.size > 5 * 1024 * 1024:
                    raise ValidationError("Cada imagen debe pesar menos de 5MB")

            # Crear publicación
            publicacion = PublicacionMascota.objects.create(
                usuario=usuario,
                tipo_publicacion=tipo_publicacion,
                descripcion=descripcion,
                nombre_mascota=nombre_mascota,
                raza=raza,
                edad=form_data['edad'],  # Usamos la edad ya validada
                sexo=sexo,
                contacto=contacto
            )

            # Guardar imágenes
            for imagen in imagenes:
                FotoMascota.objects.create(publicacion=publicacion, imagen=imagen)

            messages.success(request, "Publicación creada exitosamente!")
            return redirect("pagina_usuario")

        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Ocurrió un error al crear la publicación: {str(e)}")

    publicaciones = PublicacionMascota.objects.all().order_by('-fecha_publicacion')
    return render(request, "usuarios/pagina_usuario.html", {
        "usuario": usuario,
        "publicaciones": publicaciones,
        "form_data": form_data  # Pasamos los datos del formulario al template
    })

@session_required_and_rol_permission(1, 2, 3)
def mis_publicaciones(request):
    sesion = request.session.get("pista", None)
    
    if not sesion:
        return redirect("iniciar_sesion")
    try:
        usuario = Usuario.objects.get(id_usuario=sesion["id"])
    except Usuario.DoesNotExist:
        return HttpResponse("Usuario no encontrado", status=404)
    
    # Datos del formulario que se preservarán en caso de error
    form_data = {
        'tipo_publicacion': '',
        'descripcion': '',
        'nombre_mascota': '',
        'raza': '',
        'edad': '',
        'sexo': '',
        'contacto': ''
    }

    if request.method == "POST":
        try:
            # Obtener datos del formulario
            tipo_publicacion = request.POST.get('tipo_publicacion')
            descripcion = request.POST.get('descripcion', '').strip()
            nombre_mascota = request.POST.get('nombre_mascota', '').strip()
            raza = request.POST.get('raza', '').strip()
            edad = request.POST.get('edad', '').strip()
            sexo = request.POST.get('sexo', '').strip() 
            contacto = request.POST.get('contacto', '').strip()
            imagenes = request.FILES.getlist('imagenes')

            # Validaciones específicas según tus requerimientos
            if tipo_publicacion not in ['perdida', 'adopcion']:
                raise ValidationError("Debes seleccionar un tipo de publicación válido")
            
            if not descripcion or len(descripcion) < 10:
                raise ValidationError("La descripción debe tener al menos 10 caracteres")

            if nombre_mascota and not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', nombre_mascota):
                raise ValidationError("El nombre de la mascota solo puede contener letras y espacios")

            if raza and not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', raza):
                raise ValidationError("La raza solo puede contener letras y espacios")

            if edad:
                try:
                    edad_int = int(edad)
                    if edad_int < 1 or edad_int > 15:
                        raise ValidationError("La edad debe estar entre 1 y 15 años")
                    # Guardamos la edad validada
                    form_data['edad'] = str(edad_int)
                except ValueError:
                    raise ValidationError("La edad debe ser un número válido")
                
            if not sexo or sexo not in ['Hembra', 'Macho']:
                raise ValidationError("Selecciona un sexo válido (Macho o Hembra)")

            if contacto and not re.match(r'^\d{7,15}$', contacto):
                raise ValidationError("El contacto debe contener entre 7 y 15 dígitos")

            if not imagenes:
                raise ValidationError("Debes subir al menos una imagen")

            # Validar imágenes
            for imagen in imagenes:
                # Validar extensión
                allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
                ext = os.path.splitext(imagen.name)[1].lower()
                if ext not in allowed_extensions:
                    raise ValidationError("Solo se permiten imágenes (JPG, JPEG, PNG, GIF, WEBP)")

                # Validar tamaño (5MB máximo)
                if imagen.size > 5 * 1024 * 1024:
                    raise ValidationError("Cada imagen debe pesar menos de 5MB")

            # Crear publicación
            publicacion = PublicacionMascota.objects.create(
                usuario=usuario,
                tipo_publicacion=tipo_publicacion,
                descripcion=descripcion,
                nombre_mascota=nombre_mascota,
                raza=raza,
                edad=form_data['edad'],  # Usamos la edad ya validada
                sexo=sexo,
                contacto=contacto
            )

            # Guardar imágenes
            for imagen in imagenes:
                FotoMascota.objects.create(publicacion=publicacion, imagen=imagen)

            messages.success(request, "Publicación creada exitosamente!")
            return redirect("mis_publicaciones")

        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Ocurrió un error al crear la publicación: {str(e)}")

    try:
        usuario = Usuario.objects.get(id_usuario=sesion["id"])
    except Usuario.DoesNotExist:
        return HttpResponse("Usuario no encontrado", status=404)
    
    # Filtramos solo las publicaciones del usuario actual
    publicaciones = PublicacionMascota.objects.filter(usuario=usuario).order_by('-fecha_publicacion')
    
    # Usamos el mismo template de pagina_usuario pero con contexto diferente
    return render(request, "usuarios/pagina_usuario.html", {
        "usuario": usuario,
        "publicaciones": publicaciones,
        "solo_mis_publicaciones": True,
        "total_publicaciones": publicaciones.count(),
        "ultima_publicacion": publicaciones.first().fecha_publicacion if publicaciones.exists() else None  # Bandera para el template
    })

@session_required_and_rol_permission(1, 2, 3)
def editar_publicacion(request, publicacion_id):
    try:
        publicacion = PublicacionMascota.objects.get(id=publicacion_id, usuario__id_usuario=request.session["pista"]["id"])
        
        if request.method == "POST":
            # Procesa los datos del formulario
            publicacion.tipo_publicacion = request.POST.get('tipo_publicacion')
            publicacion.nombre_mascota = request.POST.get('nombre_mascota')
            publicacion.raza = request.POST.get('raza')
            publicacion.edad = request.POST.get('edad')
            publicacion.sexo = request.POST.get('sexo')
            publicacion.contacto = request.POST.get('contacto')
            publicacion.descripcion = request.POST.get('descripcion')
            # Actualiza todos los campos necesarios
            
            # Manejar imágenes eliminadas
            deleted_images = request.POST.getlist('deleted_images')
            for image_id in deleted_images:
                try:
                    foto = FotoMascota.objects.get(id=image_id, publicacion=publicacion)
                    # Eliminar archivo físico
                    if os.path.exists(foto.imagen.path):
                        default_storage.delete(foto.imagen.path)
                    # Eliminar registro de la base de datos
                    foto.delete()
                except FotoMascota.DoesNotExist:
                    pass
            
            # Manejar imágenes que se mantienen
            keep_images = request.POST.getlist('keep_images')
            FotoMascota.objects.filter(publicacion=publicacion).exclude(id__in=keep_images).delete()
            
            # Agregar nuevas imágenes
            nuevas_imagenes = request.FILES.getlist('imagenes')
            for imagen in nuevas_imagenes:
                # Validar tamaño (máximo 5MB)
                if imagen.size > 5 * 1024 * 1024:
                    messages.warning(request, f'La imagen {imagen.name} es demasiado grande (máximo 5MB)')
                    continue
                
                # Validar tipo de archivo
                extension = os.path.splitext(imagen.name)[1].lower()
                if extension not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    messages.warning(request, f'Formato no soportado para {imagen.name}')
                    continue
                
                # Guardar la imagen
                foto = FotoMascota(publicacion=publicacion)
                foto.imagen.save(imagen.name, ContentFile(imagen.read()), save=True)
                
            publicacion.save()
            messages.success(request, "Publicación actualizada correctamente")
            return redirect('mis_publicaciones')
            
        return render(request, 'usuarios/editar_publicacion.html', {
            'publicacion': publicacion
        })
        
    except PublicacionMascota.DoesNotExist:
        messages.error(request, "Publicación no encontrada")
        return redirect('pagina_usuario')
    
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
    total_items = 0  # Cantidad total de productos en el carrito

    if id_usuario:
        try:
            usuario = Usuario.objects.get(id_usuario=id_usuario)
            carrito, creado = Carrito.objects.get_or_create(usuario=usuario)
            # Calcular el total de ítems en el carrito
            total_items = sum(item.cantidad for item in carrito.items.all())
        except Usuario.DoesNotExist:
            carrito = None

    contexto = {
        "dato_producto_usuario": list_productos,
        "productos_mas_vendidos": productos_mas_vendidos,
        "carrito": carrito,
        "total_items": total_items
    }

    return render(request, 'usuarios/productos_usuarios.html', contexto)


def configuracion(request):
    return render(request, 'usuarios/configuracion.html')


def eliminar_cuenta(request):
    if request.method == 'POST':
        confirmacion = request.POST.get('confirmacion')
        
        try:
            # Acceder al id_usuario desde la sesión
            usuario = Usuario.objects.get(id_usuario=request.session['pista']['id'])
            
            # Verificar si la contraseña es correcta
            if usuario.check_password(confirmacion):
                usuario.delete()
                # Cerrar la sesión del usuario
                logout(request)
                messages.success(request, "Tu cuenta ha sido eliminada permanentemente.")
                return redirect('iniciar_sesion')  # Redirige a la página de inicio
            else:
                messages.error(request, "La contraseña ingresada es incorrecta.")
                return redirect('configuracion')  # Redirige a la página de configuración
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return redirect('configuracion')  # Redirige a la página de configuración

@session_required_and_rol_permission(1,2,3)
def veterinarias_asociadas(request):
    return render(request,'usuarios/veterinarias_asociadas.html')

def producto_compra(request):
    return render(request, 'usuarios/producto_compra.html')

# --------------------------------------------------------------
# Administrador

@session_required_and_rol_permission(1)
def pagina_administrador(request):
    if not request.session.get('pista') or request.session['pista'].get('rol') != 1:  # Asume que 1 es admin
        return redirect('pagina_principal')
    try:
        # Obtener el objeto usuario completo
        usuario_admin = Usuario.objects.get(id_usuario=request.session['pista']['id'])
    except Usuario.DoesNotExist:
        return redirect('pagina_principal')
    
    # Obtener estadísticas
    reportes_pendientes = Reporte.objects.filter(revisado=False).count()

    
    # Últimos 5 reportes no revisados
    ultimos_reportes = Reporte.objects.filter(revisado=False).select_related(
        'publicacion', 'usuario_reportero'
    ).order_by('-fecha_reporte')[:5]
    
    context = {
        'reportes_pendientes_count': reportes_pendientes,
        'ultimos_reportes': ultimos_reportes,
        'usuario_admin': usuario_admin,
    }
    return render(request, 'administrador/pagina_administrador.html', context)

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
        messages.error(request, "El producto se ha eliminado correctamente")
    except Producto.DoesNotExist:
        messages.warning(request, "Error: El producto no existe")
    return redirect('listar_productos')

@session_required_and_rol_permission(1)
def editar_productos(request, id_producto):
    try:
        producto = Producto.objects.get(pk=id_producto)
    except Producto.DoesNotExist:
        messages.error(request, "Error: El producto no existe")
        return redirect('listar_productos')
    
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre_producto = request.POST.get("nombre_producto")
        precio = request.POST.get("precio")
        cantidad = request.POST.get("cantidad")
        descripcion = request.POST.get("descripcion")
        foto_producto = request.FILES.get("foto_producto")
        categoria = request.POST.get("categoria")
        estado = request.POST.get("estado")
        eliminar_foto = request.POST.get("eliminar_foto", False) == "on"  # Checkbox para eliminar foto
        
        # Validación de campos obligatorios
        if not all([nombre_producto, precio, cantidad, categoria, estado]):
            messages.error(request, "Todos los campos obligatorios deben ser completados")
            return render(request, "administrador/productos/agregar_productos.html", {"dato": producto})
        
        try:
            # Actualizar campos básicos
            producto.nombre_producto = nombre_producto
            producto.precio = float(precio)
            producto.cantidad = int(cantidad)
            producto.descripcion = descripcion
            producto.categoria = categoria
            producto.estado = estado
            
            # Manejo avanzado de la imagen
            if eliminar_foto:
                # Eliminar imagen existente si el checkbox está marcado
                if producto.foto_producto:
                    producto.foto_producto.delete(save=False)
                producto.foto_producto = None
            elif foto_producto:
                # Validar tipo y tamaño de imagen
                valid_extensions = ['image/jpeg', 'image/png', 'image/gif']
                if foto_producto.content_type not in valid_extensions:
                    messages.error(request, "Formato de imagen no válido. Use JPG, PNG o GIF.")
                    return render(request, "administrador/productos/agregar_productos.html", {"dato": producto})
                
                if foto_producto.size > 5*1024*1024:  # 5MB
                    messages.error(request, "La imagen es demasiado grande (máximo 5MB)")
                    return render(request, "administrador/productos/agregar_productos.html", {"dato": producto})
                
                # Si pasa validaciones, actualizar la imagen
                producto.foto_producto = foto_producto
            # Si no hay cambios en la imagen, se mantiene la existente
            
            producto.save()
            messages.success(request, "Producto actualizado correctamente")
            return redirect('listar_productos')
            
        except ValueError as e:
            messages.error(request, f"Error en los datos numéricos: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error al actualizar el producto: {str(e)}")
        
        return render(request, "administrador/productos/agregar_productos.html", {"dato": producto})
    
    else:
        # Método GET - Mostrar formulario con datos actuales
        return render(request, "administrador/productos/agregar_productos.html", {"dato": producto})

def modal_carrito(request):
    return render(request,'usuarios/modal_carrito.html')

def soporte(request):
    return render(request,'usuarios/soporte.html')

def suspender_cuenta(request):
    return render(request,'usuarios/suspender_cuenta.html')

def notificaciones(request):
    return render(request,'usuarios/notificaciones.html')

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

        # Calcular la nueva cantidad propuesta
        nueva_cantidad = item.cantidad + 1

        # Verificar si hay suficiente stock disponible
        if nueva_cantidad > producto.cantidad:
            messages.error(request, f"Solo quedan {producto.cantidad} unidades disponibles de {producto.nombre_producto}.")
        else:
            # Aumentar la cantidad
            item.cantidad = nueva_cantidad
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
        messages.success(request, "Carrito Vaciado Correctamente")
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

# ------------------- VISTAS PARA REPORTES -------------------
@session_required_and_rol_permission(1)  # Solo admin
def listar_reportes(request):
    reportes = Reporte.objects.filter(revisado=False).select_related(
        'publicacion', 
        'usuario_reportero',
        'publicacion__usuario'
    ).order_by('-fecha_reporte')
    
    return render(request, 'administrador/listar_reportes.html', {
        'reportes': reportes
    })

@session_required_and_rol_permission(1)  # Solo admin
def ver_reporte(request, reporte_id):
    reporte = get_object_or_404(
        Reporte.objects.select_related(
            'publicacion',
            'usuario_reportero',
            'publicacion__usuario'
        ), 
        id=reporte_id
    )
    
    return render(request, 'administrador/detalle_reporte.html', {
        'reporte': reporte
    })

@session_required_and_rol_permission(1)  # Solo admin
def resolver_reporte(request, reporte_id):
    if request.method == 'POST':
        reporte = get_object_or_404(Reporte, id=reporte_id)
        reporte.revisado = True
        reporte.save()
        messages.success(request, 'Reporte marcado como resuelto.')
    return redirect('listar_reportes')

@session_required_and_rol_permission(2, 3)  # Para usuarios normales (roles 2 y 3)
def reportar_publicacion(request):
    if request.method == 'POST':
        publicacion_id = request.POST.get('publicacion_id')
        tipo_reporte = request.POST.get('tipo_reporte')
        motivo = request.POST.get('motivo', '')
        
        try:
            publicacion = PublicacionMascota.objects.get(id=publicacion_id)
            usuario_reportero = Usuario.objects.get(id_usuario=request.session['pista']['id'])
            
            # Validar que no sea el dueño
            if usuario_reportero == publicacion.usuario:
                return JsonResponse({
                    'success': False,
                    'error': 'No puedes reportar tu propia publicación'
                }, status=400)
                
            # Verificar si ya reportó
            existe = Reporte.objects.filter(
                publicacion=publicacion,
                usuario_reportero=usuario_reportero,
                revisado=False
            ).exists()
            
            if existe:
                return JsonResponse({
                    'success': False,
                    'error': 'Ya has reportado esta publicación'
                }, status=400)
            
            # Crear reporte
            Reporte.objects.create(
                publicacion=publicacion,
                tipo_reporte=tipo_reporte,
                usuario_reportero=usuario_reportero,
                motivo=motivo
            )
            
            return JsonResponse({'success': True})
            
        except PublicacionMascota.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Publicación no encontrada'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'success': False}, status=400)

def configuracion_cuenta(request):
    """Vista para la configuración de cuenta, que incluye la sección de soportes"""
    # Obtener tickets del usuario
    tickets = TicketSoporte.objects.filter(usuario=request.user).order_by('-fecha_creacion')[:5]
    
    # Obtener preguntas frecuentes
    preguntas_frecuentes = PreguntaFrecuente.objects.filter(activo=True)[:5]
    
    # Estados para mostrar como badges
    estados = EstadoTicket.objects.all()
    
    # Categorías para el formulario de nuevo ticket
    categorias = CategoriaTicket.objects.filter(activo=True)
    
    context = {
        'tickets': tickets,
        'preguntas_frecuentes': preguntas_frecuentes,
        'estados': estados,
        'categorias': categorias,
    }
    
    return render(request, 'administrador/configuracion_cuenta.html', context)


def lista_tickets(request):
    """Vista para listar todos los tickets de soporte del usuario"""
    # Inicializar el formulario de filtrado
    filtro_form = FiltroTicketsForm(request.GET)
    
    # Obtener todos los tickets del usuario
    tickets = TicketSoporte.objects.filter(usuario=request.user)
    
    # Aplicar filtros si se proporcionan
    if filtro_form.is_valid():
        # Filtrar por estado
        if estado := filtro_form.cleaned_data.get('estado'):
            tickets = tickets.filter(estado__nombre__icontains=estado)
        
        # Filtrar por categoría
        if categoria := filtro_form.cleaned_data.get('categoria'):
            tickets = tickets.filter(categoria=categoria)
        
        # Buscar por número o asunto
        if busqueda := filtro_form.cleaned_data.get('busqueda'):
            tickets = tickets.filter(
                Q(numero_ticket__icontains=busqueda) | 
                Q(asunto__icontains=busqueda)
            )
        
        # Ordenar resultados
        orden = filtro_form.cleaned_data.get('orden', 'reciente')
        if orden == 'reciente':
            tickets = tickets.order_by('-fecha_creacion')
        elif orden == 'antiguo':
            tickets = tickets.order_by('fecha_creacion')
        elif orden == 'prioridad':
            # Ordenar por prioridad (urgente, alta, media, baja) y luego por fecha
            tickets = tickets.annotate(
                prioridad_orden=Case(
                    When(prioridad='urgente', then=Value(0)),
                    When(prioridad='alta', then=Value(1)),
                    When(prioridad='media', then=Value(2)),
                    When(prioridad='baja', then=Value(3)),
                    default=Value(4),
                    output_field=IntegerField()
                )
            ).order_by('prioridad_orden', '-fecha_creacion')
    else:
        # Ordenar por defecto (más recientes primero)
        tickets = tickets.order_by('-fecha_creacion')
    
    # Paginación
    paginator = Paginator(tickets, 10)  # 10 tickets por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estados para mostrar como badges
    estados = EstadoTicket.objects.all()
    
    context = {
        'page_obj': page_obj,
        'filtro_form': filtro_form,
        'estados': estados,
    }
    
    return render(request, 'administrador/tickets/lista_tickets.html', context)

def crear_ticket(request):
    """Vista para crear un nuevo ticket de soporte"""
    if request.method == 'POST':
        form = TicketSoporteForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.usuario = request.user
            
            # Asignar estado inicial (Pendiente)
            estado_pendiente = EstadoTicket.objects.filter(nombre__icontains='pendiente').first()
            if not estado_pendiente:
                # Si no existe el estado pendiente, crear uno
                estado_pendiente = EstadoTicket.objects.create(
                    nombre='Pendiente',
                    color='bg-warning',
                    orden=1
                )
            
            ticket.estado = estado_pendiente
            ticket.save()
            
            messages.success(request, f'Ticket #{ticket.numero_ticket} creado exitosamente.')
            return redirect('detalle_ticket', ticket_id=ticket.id)
    else:
        form = TicketSoporteForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'administrador/tickets/crear_ticket.html', context)


def detalle_ticket(request, ticket_id):
    """Vista para ver el detalle de un ticket y responder"""
    ticket = get_object_or_404(TicketSoporte, id=ticket_id, usuario=request.user)
    respuestas = ticket.respuestas.all().order_by('fecha_creacion')
    
    # Formulario para responder
    if request.method == 'POST':
        form = RespuestaTicketForm(request.POST, request.FILES)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.ticket = ticket
            respuesta.usuario = request.user
            respuesta.es_respuesta_admin = False  # El usuario no es admin
            respuesta.save()
            
            messages.success(request, 'Tu respuesta ha sido enviada.')
            return redirect('detalle_ticket', ticket_id=ticket.id)
    else:
        form = RespuestaTicketForm()
    
    context = {
        'ticket': ticket,
        'respuestas': respuestas,
        'form': form,
    }
    
    return render(request, 'administrador/tickets/detalle_ticket.html', context)

    
def cerrar_ticket(request, ticket_id):
    """Vista para cerrar un ticket de soporte"""
    ticket = get_object_or_404(TicketSoporte, id=ticket_id, usuario=request.user)
    
    # Buscar estado "Cerrado" o "Resuelto"
    estado_cerrado = EstadoTicket.objects.filter(
        Q(nombre__icontains='cerrado') | Q(nombre__icontains='resuelto')
    ).first()
    
    if not estado_cerrado:
        # Si no existe el estado, crear uno
        estado_cerrado = EstadoTicket.objects.create(
            nombre='Cerrado',
            color='bg-secondary',
            orden=99
        )
    
    # Actualizar el ticket
    ticket.estado = estado_cerrado
    ticket.fecha_cierre = timezone.now()
    ticket.save()
    
    messages.success(request, f'El ticket #{ticket.numero_ticket} ha sido cerrado.')
    return redirect('lista_tickets')


def preguntas_frecuentes(request):
    """Vista para mostrar todas las preguntas frecuentes agrupadas por categoría"""
    # Obtener todas las categorías que tienen preguntas asociadas
    categorias = CategoriaTicket.objects.filter(
        activo=True,
        preguntas_frecuentes__activo=True
    ).distinct()
    
    # Preparar diccionario de categorías con sus preguntas
    categorias_con_preguntas = {}
    for categoria in categorias:
        preguntas = PreguntaFrecuente.objects.filter(
            categoria=categoria,
            activo=True
        ).order_by('orden')
        categorias_con_preguntas[categoria] = preguntas
    
    # Preguntas sin categoría
    preguntas_sin_categoria = PreguntaFrecuente.objects.filter(
        categoria__isnull=True,
        activo=True
    ).order_by('orden')
    
    if preguntas_sin_categoria:
        categorias_con_preguntas['General'] = preguntas_sin_categoria
    
    context = {
        'categorias_con_preguntas': categorias_con_preguntas,
    }
    
    return render(request, 'administrador/tickets/preguntas_frecuentes.html', context)


def buscar_pregunta(request):
    """Vista para buscar en las preguntas frecuentes (AJAX)"""
    query = request.GET.get('q', '')
    if not query or len(query) < 3:
        return JsonResponse({'results': []})
    
    preguntas = PreguntaFrecuente.objects.filter(
        Q(pregunta__icontains=query) | Q(respuesta__icontains=query),
        activo=True
    )[:5]
    
    results = []
    for pregunta in preguntas:
        results.append({
            'id': pregunta.id,
            'pregunta': pregunta.pregunta,
            'respuesta': pregunta.respuesta[:150] + '...' if len(pregunta.respuesta) > 150 else pregunta.respuesta,
            'url': f"#pregunta-{pregunta.id}"
        })
    
    return JsonResponse({'results': results})

@require_POST
def agregar_comentario(request):
    try:
        publicacion_id = request.POST.get('publicacion_id')
        texto = request.POST.get('texto', '').strip()
        imagen = request.FILES.get('imagen')
        
        # Validaciones
        if not publicacion_id:
            return JsonResponse({'success': False, 'error': 'ID de publicación requerido'})
        
        if not texto and not imagen:
            return JsonResponse({'success': False, 'error': 'Debes escribir un comentario o subir una imagen'})
        
        if len(texto) > 500:
            return JsonResponse({'success': False, 'error': 'El comentario no puede exceder 500 caracteres'})
        
        # Obtener publicación y usuario
        publicacion = get_object_or_404(PublicacionMascota, id=publicacion_id)
        usuario_id = request.session.get('pista', {}).get('id')
        usuario = get_object_or_404(Usuario, id_usuario=usuario_id)
        
        # Crear comentario
        comentario = Comentario.objects.create(
            publicacion=publicacion,
            usuario=usuario,
            texto=texto,
            imagen=imagen
        )
        
        # Crear notificación (solo si no es el mismo usuario)
        if publicacion.usuario.id_usuario != usuario.id_usuario:
            Notificacion.objects.create(
                usuario=publicacion.usuario,
                tipo='comentario',
                titulo='Nuevo comentario en tu publicación',
                mensaje=f'{usuario.nombre_completo} comentó en tu publicación "{publicacion.nombre_mascota}"',
                publicacion=publicacion,
                comentario=comentario
            )
        
        # Preparar respuesta
        response_data = {
            'success': True,
            'comentario': {
                'id': comentario.id,
                'texto': comentario.texto,
                'usuario': comentario.usuario.nombre_completo,
                'foto_perfil': comentario.usuario.foto_perfil.url if comentario.usuario.foto_perfil else None,
                'fecha': comentario.fecha_comentario.strftime('%d/%m/%Y %H:%M'),
                'imagen': comentario.imagen.url if comentario.imagen else None,
                'es_propio': True
            }
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def obtener_comentarios(request, publicacion_id):
    try:
        publicacion = get_object_or_404(PublicacionMascota, id=publicacion_id)
        comentarios = publicacion.comentarios.all()
        usuario_actual_id = request.session.get('pista', {}).get('id')
        
        comentarios_data = []
        for comentario in comentarios:
            comentarios_data.append({
                'id': comentario.id,
                'texto': comentario.texto,
                'usuario': comentario.usuario.nombre_completo,
                'foto_perfil': comentario.usuario.foto_perfil.url if comentario.usuario.foto_perfil else None,
                'fecha': comentario.fecha_comentario.strftime('%d/%m/%Y %H:%M'),
                'imagen': comentario.imagen.url if comentario.imagen else None,
                'es_propio': comentario.usuario.id_usuario == usuario_actual_id
            })
        
        return JsonResponse({
            'success': True,
            'comentarios': comentarios_data
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def eliminar_comentario(request, comentario_id):
    try:
        usuario_id = request.session.get('pista', {}).get('id')
        comentario = get_object_or_404(Comentario, id=comentario_id, usuario__id_usuario=usuario_id)
        comentario.delete()
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def obtener_notificaciones(request):
    try:
        usuario_id = request.session.get('pista', {}).get('id')
        usuario = get_object_or_404(Usuario, id_usuario=usuario_id)

        notificaciones = Notificacion.objects.filter(usuario=usuario, leida=False).order_by('-fecha_creacion')
        
        notificaciones_data = [
            {
                'id': notificacion.id,
                'mensaje': notificacion.mensaje,
                'fecha': notificacion.fecha_creacion.strftime('%d/%m/%Y %H:%M')
            }
            for notificacion in notificaciones
        ]
        
        return JsonResponse({'success': True, 'notificaciones': notificaciones_data})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

