import requests
import os


def verificar_pagina(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False


def descargar_imagen(url_imagen, nombre_local_imagen):
    # agregamos para que se vaya a la carpeta de img
    if not nombre_local_imagen.__contains__("img/"):
        nombre_local_imagen = "img/" + nombre_local_imagen

    # agregamos la extension
    if not nombre_local_imagen.__contains__(".jpg"):
        nombre_local_imagen = nombre_local_imagen + ".jpg"

    # descargamos
    imagen = requests.get(url_imagen, stream=True).content

    with open(nombre_local_imagen, "wb") as handler:
        handler.write(imagen)

    # regresamos el nombre
    return nombre_local_imagen


def eliminarArchivo(url):
    os.remove(url)


def existe(path):
    isFile = os.path.isfile(path)
    if isFile:
        return True
    else:
        return False


def obtener_nombre_archivos(path):
    return tuple(os.listdir(path))
