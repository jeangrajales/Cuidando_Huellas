from django.shortcuts import render

# Create your views here.


def pagina_principal(request):
    return render(request,'pagina_principal.html')


def mascotas_perdidas(request):
    return render(request,'mascotas_perdidas.html')

def productos(request):
    pass

def adopciones(request):
    return render(request,'adopciones.html')