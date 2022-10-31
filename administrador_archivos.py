import requests
import os


def descargaImagen(url_imagen, nombre_local_imagen):
    imagen = requests.get(url_imagen, stream=True).content

    with open(nombre_local_imagen, "wb") as handler:
        handler.write(imagen)


def eliminarArchivo(url):
    os.remove(url)
