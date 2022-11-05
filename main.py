import administrador_archivos as di
import calculoFacial as cf

pathOrlando = ["img/image01.jpg", "img/image02.jpg",
               "img/image03.jpg", "img/image04.jpg"]

pathMarce = ["img/imagen_0005.jpg", "img/imagen_0006.jpg",
             "img/imagen_0007.jpg", "img/imagen_0008.jpg"]

pathAlex = ["img/imagen_0009.jpg", "img/imagen_0010.jpg",
            "img/imagen_0011.jpg", "img/imagen_0012.jpg", "img/imagen_0013.jpg", "img/imagen_0014.jpg", "img/imagen_0015.jpg"]
pathPruebas = ["img/imagen_0016.jpg",
               "img/imagen_0017.jpg", "img/imagen_0018.jpg"]
pathPaths = [pathOrlando, pathMarce, pathAlex]

cf.encontrar(cf.getPromedios_local(
    pathPaths, pathOrlando, pathMarce, pathAlex), pathPruebas)
