from django.db import models

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

