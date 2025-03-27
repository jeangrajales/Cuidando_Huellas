from django.shortcuts import render

# Create your views here.


def iniciar_sesion(request):
    return render(request,'iniciar_sesion.html')

def registrarse(request):
    return render(request,'registrarse.html')

def pagina_principal(request):
    return render(request,'pagina_principal.html')

def nuestros_servicios(request):
    return render(request, 'nuestros_servicios.html')


def mascotas_perdidas(request):
    return render(request,'mascotas_perdidas.html')

def productos(request):
    pass

def adopciones(request):
    return render(request,'adopciones.html')