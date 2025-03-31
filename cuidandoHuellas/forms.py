from django import forms

class formularioContacto(forms.Form):
    nombre = forms.CharField(max_length=100, required= True)
    correo = forms.EmailField(required= True)
    mensaje = forms.CharField(required= True)