from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.pagina_principal,name="pagina_principal"),
    path("correos1/", views.correos1, name="correos1"),
    path("correos2/", views.correos2, name="correos2"),
    path("correos3/", views.correos3, name="correos3"),
    path('iniciar_sesion/',views.iniciar_sesion, name="iniciar_sesion"),
    path('cerrar_sesion/',views.cerrar_sesion, name="cerrar_sesion"),
    path('registrarse/',views.registrarse,name="registrarse"),
    path('mascotas_perdidas/',views.mascotas_perdidas,name="mascotas_perdidas"),
    path('adopciones/',views.adopciones,name="adopciones"),
    path('pagina_usuario/',views.pagina_usuario,name="pagina_usuario"),
    path('mascotas_perdidas/',views.mascotas_perdidas,name="mascotas_perdidas"),
    path('productos_usuarios/',views.productos_usuarios,name="productos_usuarios"),
    path('producto_compra/',views.producto_compra,name="producto_compra"),
    path('productos_usuarios/',views.productos_usuarios,name="productos_usuarios"),
    path('adopciones/',views.adopciones, name="adopciones"),
    path('veterinarias_asociadas/', views.veterinarias_asociadas,name="veterinarias_asociadas"),
    path('publicacion/<int:publicacion_id>/eliminar/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('editar_usuario/', views.editar_usuario, name="editar_usuario" ),
    path('mis-publicaciones/', views.mis_publicaciones, name='mis_publicaciones'),
    path('editar_publicacion/<int:publicacion_id>/', views.editar_publicacion, name='editar_publicacion'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('eliminar_cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),

    # Carrito
   
    path('agregar_al_carrito/<int:id_producto>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('aumentar_cantidad/<int:item_id>/', views.aumentar_cantidad, name='aumentar_cantidad'),
    path('disminuir_cantidad/<int:item_id>/', views.disminuir_cantidad, name='disminuir_cantidad'),
    path('eliminar_item/<int:item_id>/', views.eliminar_item, name='eliminar_item'),
    path('vaciar_carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('generar_factura/', views.generar_factura, name='generar_factura'),
    path('modal_carrito/', views.modal_carrito, name="modal_carrito"),


    #Administrador
    path('pagina_administrador/',views.pagina_administrador, name="pagina_administrador"),
    path('listar_usuarios/',views.listar_usuarios, name="listar_usuarios"),
    path('eliminar_usuarios/<int:id_usuario>',views.eliminar_usuarios, name="eliminar_usuarios"),
    path('listar_productos/',views.listar_productos, name="listar_productos"),
    path('agregar_productos/',views.agregar_productos, name="agregar_productos"),
    path('eliminar_productos/<int:id_producto>',views.eliminar_productos, name="eliminar_productos"),
    path('editar_productos/<int:id_producto>',views.editar_productos, name="editar_productos"),
    path('listar_mascotas_perdidas/',views.listar_mascotas_perdidas, name="listar_mascotas_perdidas"),
    path('eliminar_mascotas_perdidas/<int:publicacion_id>',views.eliminar_mascotas_perdidas, name="eliminar_mascotas_perdidas"),
    path('listar_mascotas_adopcion/',views.listar_mascotas_adopcion, name="listar_mascotas_adopcion"),
    path('eliminar_mascotas_adopcion/<int:publicacion_id>/', views.eliminar_mascotas_adopcion, name='eliminar_mascotas_adopcion'),
    path('administrador/reportes/', views.listar_reportes, name='listar_reportes'),
    path('administrador/reportes/<int:reporte_id>/', views.ver_reporte, name='ver_reporte'),
    path('administrador/reportes/<int:reporte_id>/resolver/', views.resolver_reporte, name='resolver_reporte'),
    path('reportar-publicacion/', views.reportar_publicacion, name='reportar_publicacion'),
    path('soporte/', views.soporte, name='soporte'),
    path('suspender_cuenta', views.suspender_cuenta, name='suspender_cuenta'),
    path('notificaciones/', views.notificaciones, name='notificaciones'),

    # Vista principal de configuración de cuenta (incluye sección soportes)
    path('configuracion/', views.configuracion_cuenta, name='configuracion_cuenta'),
    
    # Rutas para gestión de tickets de soporte
    path('soportes/tickets/', views.lista_tickets, name='lista_tickets'),
    path('soportes/tickets/crear/', views.crear_ticket, name='crear_ticket'),
    path('soportes/tickets/<int:ticket_id>/', views.detalle_ticket, name='detalle_ticket'),
    path('soportes/tickets/<int:ticket_id>/cerrar/', views.cerrar_ticket, name='cerrar_ticket'),
    
    # Rutas para preguntas frecuentes
    path('soportes/faq/', views.preguntas_frecuentes, name='preguntas_frecuentes'),
    path('soportes/faq/buscar/', views.buscar_pregunta, name='buscar_pregunta'),

    # URLs para comentarios
    path('agregar-comentario/', views.agregar_comentario, name='agregar_comentario'),
    path('comentarios/<int:publicacion_id>/', views.obtener_comentarios, name='obtener_comentarios'),
    path('eliminar-comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('obtener-notificaciones/',views.obtener_notificaciones, name='obtener_notificaciones'),
   

]

    
      
    