from django.db import models

# Create your models here.

class Usuario(models.Model):
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
