import descargaImagen as di
import calculoFacial as cf

pathOrlando = ["imagen_0001.jpg", "imagen_0002.jpg",
               "imagen_0003.jpg", "imagen_0004.jpg"]

pathMarce = ["imagen_0005.jpg", "imagen_0006.jpg",
             "imagen_0007.jpg", "imagen_0008.jpg"]

pathAlex = ["imagen_0009.jpg", "imagen_0010.jpg",
            "imagen_0011.jpg", "imagen_0012.jpg", "imagen_0013.jpg", "imagen_0014.jpg", "imagen_0015.jpg"]
pathPruebas = ["imagen_0016.jpg", "imagen_0017.jpg", "imagen_0018.jpg"]
pathPaths = [pathOrlando, pathMarce, pathAlex]

cf.encontrar(cf.getPromedios_local(
    pathPaths, pathOrlando, pathMarce, pathAlex), pathPruebas)
