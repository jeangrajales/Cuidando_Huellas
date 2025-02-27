from django.shortcuts import render

# Create your views here.


def Hola(request):
    return render(request,'index.html')