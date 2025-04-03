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
    path('quienes_somos/',views.quienes_somos,name="quienes_somos"),
    path('pagina_usuario/',views.pagina_usuario,name="pagina_usuario"),
    path('mascotas_perdidas/',views.mascotas_perdidas,name="mascotas_perdidas"),
    path('productos_usuarios/',views.productos_usuarios,name="productos_usuarios"),
    path('producto_compra/',views.producto_compra,name="producto_compra"),
    path('productos_usuarios/',views.productos_usuarios,name="productos_usuarios"),
    path('adopciones/',views.adopciones, name="adopciones"),
    path('veterinarias_asociadas/', views.veterinarias_asociadas,name="veterinaria_asociadas"),


    #Administrador
    path('pagina_administrador/',views.pagina_administrador, name="pagina_administrador"),
    #Usuarios
    path('listar_usuarios/',views.listar_usuarios, name="listar_usuarios"),
    #Productos
    path('listar_productos/',views.listar_productos, name="listar_productos"),
    path('agregar_productos/',views.agregar_productos, name="agregar_productos"),
    path('eliminar_productos/<int:id_producto>',views.eliminar_productos, name="eliminar_productos"),
    path('editar_productos/<int:id_producto>',views.editar_productos, name="editar_productos"),
    
    
    
]