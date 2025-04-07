from django import forms
from .models import *

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