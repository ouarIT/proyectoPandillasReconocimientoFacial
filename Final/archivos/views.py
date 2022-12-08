from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from django.http import FileResponse, HttpRequest
from .conexiones import *
import os

path_archivos = "C:/Users/Orlando/Desktop/git/pagina/Final/archivos/pdf"


def obtener_nombre_archivos(path):
    return tuple(os.listdir(path))


def archivos(request):

    archivos = obtener_nombre_archivos(path_archivos)

    return render(request, "contenedor.html", {"archivos": archivos})


def buscar(request):
    url = request.GET["link"]
    print(url)
    valores = analizarBasesdeDatos()
    buscarImagen(valores, url)

    archivos = obtener_nombre_archivos(path_archivos)

    return render(request, "contenedor.html", {"archivos": archivos})


def mostrar_header(request):
    return render(request, "header.html")


def show_pdf(request, archivo):
    filepath = os.path.join(path_archivos, str(archivo))

    print(filepath)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')


def miembros(request):
    return render(request, "miembros.html")


def registro(request):
    return render(request, "registro.html")
