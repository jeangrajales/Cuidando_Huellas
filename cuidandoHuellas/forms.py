from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import TicketSoporte, RespuestaTicket, CategoriaTicket

class formularioContacto(forms.Form):
    nombre = forms.CharField(max_length=100, required= True)
    correo = forms.EmailField(required= True)
    mensaje = forms.CharField(required= True)
    
class PublicacionMascotaForm(forms.ModelForm):
    class Meta:
        model = PublicacionMascota
        fields = ['tipo_publicacion', 'nombre_mascota', 'raza', 'edad', 'sexo', 'contacto', 'descripcion']
        widgets = {
            'tipo_publicacion': forms.Select(attrs={'class': 'form-select'}),
            'nombre_mascota': forms.TextInput(attrs={'class': 'form-control'}),
            'raza': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(choices=[('Macho', 'Macho'), ('Hembra', 'Hembra')], attrs={'class': 'form-select'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe el problema de tu mascota aquí...'
            }),
        }

class FotoMascotaForm(forms.ModelForm):
    class Meta:
        model = FotoMascota
        fields = ['imagen']



class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'categoria', 'precio', 'cantidad', 'estado', 'descripcion', 'foto_producto']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['foto_producto'].required = False  # Hacer que el campo no sea obligatorio


class TicketSoporteForm(forms.ModelForm):
    """Formulario para la creación de tickets de soporte"""
    
    class Meta:
        model = TicketSoporte
        fields = ['categoria', 'asunto', 'descripcion', 'archivo_adjunto', 'prioridad']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Describe brevemente tu problema'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Proporciona todos los detalles posibles sobre tu problema'}),
            'archivo_adjunto': forms.FileInput(attrs={'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo categorías activas
        self.fields['categoria'].queryset = CategoriaTicket.objects.filter(activo=True)
        
        # Etiquetas personalizadas
        self.fields['categoria'].label = "¿Qué tipo de problema tienes?"
        self.fields['asunto'].label = "Asunto"
        self.fields['descripcion'].label = "Descripción detallada"
        self.fields['archivo_adjunto'].label = "Adjuntar archivo (opcional)"
        self.fields['prioridad'].label = "¿Qué tan urgente es este problema?"

class RespuestaTicketForm(forms.ModelForm):
    """Formulario para responder a tickets de soporte"""
    
    class Meta:
        model = RespuestaTicket
        fields = ['contenido', 'archivo_adjunto']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribe tu respuesta aquí...'}),
            'archivo_adjunto': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Etiquetas personalizadas
        self.fields['contenido'].label = "Tu respuesta"
        self.fields['archivo_adjunto'].label = "Adjuntar archivo (opcional)"

class FiltroTicketsForm(forms.Form):
    """Formulario para filtrar los tickets de soporte"""
    
    ESTADO_CHOICES = [
        ('', 'Todos los estados'),
        ('pendiente', 'Pendientes'),
        ('proceso', 'En proceso'),
        ('resuelto', 'Resueltos'),
    ]
    
    ORDEN_CHOICES = [
        ('reciente', 'Más recientes primero'),
        ('antiguo', 'Más antiguos primero'),
        ('prioridad', 'Por prioridad'),
    ]
    
    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    
    categoria = forms.ModelChoiceField(
        queryset=CategoriaTicket.objects.filter(activo=True),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    
    orden = forms.ChoiceField(
        choices=ORDEN_CHOICES,
        required=False,
        initial='reciente',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    
    busqueda = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Buscar por número o asunto...'
        })
    )