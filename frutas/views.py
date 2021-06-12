from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the  index.")


def usuarios_inicio(request):
    return HttpResponse("Hello, world. You're at the usuarios_inicio index.")


def estadisticas_inicio(request):
    return HttpResponse("Hello, world. You're at the estadisticas_inicio index.")


def frutas_inicio(request):
    return HttpResponse("Hello, world. You're at the frutas_inicio index.")