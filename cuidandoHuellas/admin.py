from django.contrib import admin

# Register your models here.

from . models import *


@admin.register(Usuario)

class usuarioAdmin(admin.ModelAdmin):
     list_display = ['id', 'nombre_completo', 'ciudad', 'telefono', 'correo', 'rol']
