# Create your models here.
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.hashers import make_password , check_password
from .validators import *
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key= True)
    nombre_completo = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    telefono = models.PositiveIntegerField()
    correo = models.EmailField(max_length=254)
    contraseña = models.CharField(max_length=254)
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.contraseña)
    
    def save(self, *args, **kwargs):
        if not self.contraseña.startswith('pbkdf2_'):
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)
    ROLES = (
        (1, "Admin"),
        (2, "Usuario"),
        (3, "Empleado")
    )
    rol = models.IntegerField(choices=ROLES, default=2)

    foto_perfil = models.ImageField(
        upload_to='perfiles/',
        null=True,
        blank=True,
        default=None
    )
    
    def clean(self):
        # Validar dominio del correo
        if not re.match(r'^[\w\.-]+@(gmail\.com|hotmail\.com|outlook\.com)$', self.correo):
            raise ValidationError({'correo': 'Solo se permiten correos de gmail.com, hotmail.com o outlook.com.'})
        
        self.contraseña = self.contraseña.strip()

        # Validar contraseña con letras y números
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d).+$', self.contraseña):
            raise ValidationError({'contraseña': 'Debe contener letras y números.'})

    def save(self, *args, **kwargs):
        if not self.contraseña.startswith('pbkdf2_'):
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)
        
    @property
    def es_administrador(self):
        return self.rol == 1

    def __str__(self):
        return f"{self.nombre_completo} - {self.correo}"    
    
class Producto(models.Model):
    id_producto = models.AutoField(primary_key= True)
    nombre_producto = models.CharField(max_length=250)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    cantidad = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
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
    veces_comprado = models.PositiveIntegerField(default=0, verbose_name="Veces comprado")
    ultima_compra = models.DateTimeField(null=True, blank=True, verbose_name="Última compra")

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
    tipo_publicacion = models.CharField(
        max_length=10, 
        choices=TIPO_PUBLICACION,
        null=False,
        blank=False
    )
    
    nombre_mascota = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$',
                message="El nombre solo puede contener letras y espacios"
            )
        ],
        null=True,
        blank=True
    )
    
    edad = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Edad en años"
    )
    
    raza = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$',
                message="La raza solo puede contener letras y espacios"
            )
        ],
        null=True,
        blank=True
    )
    
    SEXO_CHOICES = [
        ('Macho', 'Macho'),
        ('Hembra', 'Hembra'),
    ]
    sexo = models.CharField(
        max_length=10,
        choices=SEXO_CHOICES,
        null=True,
        blank=True
    )
    
    contacto = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\d{7,15}$',
                message="El contacto debe contener entre 7 y 15 dígitos"
            )
        ],
        null=True,
        blank=True
    )

    def clean(self):
        if self.tipo_publicacion not in dict(self.TIPO_PUBLICACION).keys():
            raise ValidationError("Tipo de publicación no válido")

    def __str__(self):
        return f"Publicación de {self.usuario.nombre_completo} - {self.fecha_publicacion.strftime('%d/%m/%Y')}"

class FotoMascota(models.Model):
    publicacion = models.ForeignKey(PublicacionMascota, on_delete=models.CASCADE, related_name='fotos')
    imagen = models.ImageField(
        upload_to='fotos_mascotas/',
        validators=[validar_extension_imagen]
    )
    
    def __str__(self):
        return f"Foto de publicación {self.publicacion.id}"
    
class Reporte(models.Model):
    TIPO_REPORTE = [
        ('inapropiado', 'Contenido inapropiado'),
        ('estafa', 'Posible estafa'),
        ('spam', 'Spam'),
        ('otros', 'Otros'),
    ]
    
    publicacion = models.ForeignKey(
        'PublicacionMascota', 
        on_delete=models.CASCADE,
        related_name='reportes'
    )
    tipo_reporte = models.CharField(max_length=20, choices=TIPO_REPORTE)
    usuario_reportero = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='reportes_hechos'
    )
    motivo = models.TextField(blank=True, null=True)
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    revisado = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha_reporte']
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'
    
    def __str__(self):
        return f"Reporte #{self.id} - {self.get_tipo_reporte_display()} - {self.publicacion.tipo_publicacion}"