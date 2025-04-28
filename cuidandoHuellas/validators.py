import os
from django.core.exceptions import ValidationError


# Esta función valida la extensión del archivo
def validar_extension_imagen(imagen):
    # Extraemos la extensión del archivo (por ejemplo .jpg o .png)
    extension = os.path.splitext(imagen.name)[1]

    # Definimos las extensiones permitidas
    extensiones_permitidas = ['.jpg', '.jpeg', '.png']

    # Si la extensión no está permitida, lanzamos un error
    if not extension.lower() in extensiones_permitidas:
        raise ValidationError('Solo se permiten archivos con extensión .jpg, .jpeg o .png.')
    
