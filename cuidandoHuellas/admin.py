from django.contrib import admin

# Register your models here.

from . models import *


@admin.register(Usuario)
class usuarioAdmin(admin.ModelAdmin):
     list_display = ['id_usuario','nombre_completo', 'ciudad', 'telefono', 'correo', 'rol']
     list_editable = ['rol']

@admin.register(Producto)
class productoAdmin(admin.ModelAdmin):
     list_display = ['id_producto', 'nombre_producto', 'precio', 'foto_producto']
     
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'total']
    
    def total(self, obj):
        return f"${obj.total()}"
    
    total.short_description = 'Total'

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ['id', 'carrito', 'producto', 'cantidad', 'get_subtotal']
    
    def get_subtotal(self, obj):
        return f"${obj.subtotal()}"
    
    get_subtotal.short_description = 'Subtotal'

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'fecha', 'total']
    list_filter = ['fecha']
    date_hierarchy = 'fecha'

@admin.register(DetalleFactura)
class DetalleFacturaAdmin(admin.ModelAdmin):
    list_display = ['id', 'factura', 'producto', 'cantidad', 'subtotal']
    list_filter = ['factura']