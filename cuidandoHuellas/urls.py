from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.pagina_principal,name="pagina_principal"),
    path('iniciar_sesion/',views.iniciar_sesion, name="iniciar_sesion"),
    path('cerrar_sesion/',views.cerrar_sesion, name="cerrar_sesion"),
    path('registrarse/',views.registrarse,name="registrarse"),
    path('nuestros_servicios/',views.nuestros_servicios,name="nuestros_servicios"),
    path('mascotas_perdidas/',views.mascotas_perdidas,name="mascotas_perdidas"),
    path('adopciones/',views.adopciones,name="adopciones"),
    path('contactanos/',views.contactanos,name="contactanos"),
    
    
]