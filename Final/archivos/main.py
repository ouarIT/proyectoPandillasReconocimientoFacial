from conexiones import *

if __name__ == "__main__":
    valores = analizarBasesdeDatos()

    url = "https://raw.githubusercontent.com/ouarIT/img/main/img16.jpg"
    buscarImagen(valores, url)

    url = "https://raw.githubusercontent.com/ouarIT/img/main/img17.jpg"
    buscarImagen(valores, url)

    url = "https://raw.githubusercontent.com/ouarIT/img/main/img18.jpg"
    buscarImagen(valores, url)
