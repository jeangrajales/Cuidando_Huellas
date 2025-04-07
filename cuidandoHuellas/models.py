from django.db import models
from django.utils import timezone
# Create your models here.

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key= True)
    nombre_completo = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    telefono = models.PositiveIntegerField()
    correo = models.CharField(max_length=254)
    contraseña = models.CharField(max_length=254)
    ROLES = (
        (1, "Admin"),
        (2, "Usuario"),
        (3, "Empleado")
    )
    rol = models.IntegerField(choices=ROLES, default=2)
    
    def __str__(self):
        return f"{self.nombre_completo} - {self.correo}"
    

class Producto(models.Model):
    id_producto = models.AutoField(primary_key= True)
    nombre_producto = models.CharField(max_length=250)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    descripcion = models.TextField()
    CATEGORIAS = (
        (0, ""),
        (1, "Alimentos Mascotas"),
        (2, "Accesorios Mascotas"),
        (3, "Ropa Mascotas")
    )
    ESTADOS = (
        (0, ""),
        (1, "Disponible"),
        (2, "No Disponible")
    )
    foto_producto = models.ImageField(upload_to='foto_producto/') 
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default=0) 
    estado = models.CharField(max_length=20, choices=ESTADOS, default=0)

    def __str__(self):
        return f"{self.id_producto} - {self.nombre_producto} - {self.descripcion} - {self.precio} - {self.foto_producto}"
    
    

class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    
    def total(self):
        return sum(item.subtotal() for item in self.items.all())

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

class Factura(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
class PublicacionMascota(models.Model):
    TIPO_PUBLICACION = (
        ('perdida', 'Mascota Perdida'),
        ('adopcion', 'Mascota en Adopción'),
    )

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='publicaciones')
    descripcion = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    tipo_publicacion = models.CharField(max_length=10, choices=TIPO_PUBLICACION, default='perdida')
    nombre_mascota = models.CharField(max_length=100, null=True, blank=True)
    edad = models.CharField(max_length=50, null=True, blank=True)
    raza = models.CharField(max_length=100, null=True, blank=True)
    sexo = models.CharField(max_length=10, null=True, blank=True)
    contacto = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Publicación de {self.usuario.nombre_completo} - {self.fecha_publicacion.strftime('%d/%m/%Y')}"


class FotoMascota(models.Model):
    publicacion = models.ForeignKey(PublicacionMascota, on_delete=models.CASCADE, related_name='fotos')
    imagen = models.ImageField(upload_to='fotos_mascotas/')
    
    def __str__(self):
        return f"Foto de publicación {self.publicacion.id}"
