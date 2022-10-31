import cv2
import mediapipe as mp
import administrador_archivos as aa
import os

mp_face_mesh = mp.solutions.face_mesh

# relacion de una sola foto


def getRelaciones(img):
    # Lista donde se guardaran las coordenadas
    lista_coordenadas = []
    # Lista donde se guardaran las relaciones
    lista_relaciones = []
    # punto de referencia
    COOR_NARIZ = 19

    # inicia para imagenes staticas
    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            min_detection_confidence=0.5) as face_mesh:
        # Lee la imagen
        image = cv2.imread(img)
        # obtiene las dimensiones de la imagen
        height, width, depth = image.shape
        # Convierte la imagen a RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Procesa la imagen
        results = face_mesh.process(image_rgb)

        # Si encuentra una cara
        if results.multi_face_landmarks is not None:
            # Recorre los puntos de la cara
            for face_landmarks in results.multi_face_landmarks:
                # Recorre los puntos de la cara
                for index in range(len(face_landmarks.landmark)):
                    # Guarda las coordenadas de cada punto
                    x = int(face_landmarks.landmark[index].x * width)
                    y = int(face_landmarks.landmark[index].y * height)
                    z = int(face_landmarks.landmark[index].z * depth)
                    # Guarda las coordenadas en una lista
                    lista_coordenadas.append([x, y, z])

            # recorre la lista de coordenadas
            for i in range(len(lista_coordenadas)):
                # Calcula la distancia entre el punto de referencia y el punto actual
                if i != COOR_NARIZ:
                    x = abs(lista_coordenadas[i][0] -
                            lista_coordenadas[COOR_NARIZ][0])
                    y = abs(lista_coordenadas[i][1] -
                            lista_coordenadas[COOR_NARIZ][1])
                    z = abs(lista_coordenadas[i][2] -
                            lista_coordenadas[COOR_NARIZ][2])
                    # Si puede calcular la tangente de lo controrario guarda y o z
                    if x == 0:
                        pass
                    else:
                        tangxy = y / x
                        tangxz = z / x
                    # Guarda las relaciones en una lista
                        lista_relaciones.append(tangxy + tangxz)

            # Retorna la suma de las relaciones
            sumalist = sum(lista_relaciones)

    return sumalist

# relacion promediada de varias fotos


def getPromedios_local(pathPaths, pathOrlando, pathMarce, pathAlex):
    resultados_temp = []
    promedios = []
    # recorre los paths de paths de imagenes
    for path in pathPaths:
        # recorre las imagenes de cada path
        for img in path:
            # obtiene las relaciones de cada imagen
            resultados_temp.append(getRelaciones(img))
        # obtiene el promedio de las relaciones de cada path

        if path == pathOrlando:
            # guarda el promedio y el nombre de la persona
            # numero sumas de relaciones entre las fotos ingresadas
            promedios.append(
                [sum(resultados_temp) / len(resultados_temp), "Orlando"])
        elif path == pathMarce:
            promedios.append(
                [sum(resultados_temp) / len(resultados_temp), "Marce"])
        elif path == pathAlex:
            promedios.append(
                [sum(resultados_temp) / len(resultados_temp), "Alex"])

        # limpia la lista temporal
        resultados_temp = []
    # retorna la lista de promedios
    return promedios


def encontrar(promedios, pathPruebas):
    # por cada imagen a buscar coincidencia
    for img in pathPruebas:

        # variable para el error
        error = 101
        # error por cada recorrido
        error_actual = 101
        # posicion en la lista de imagenes
        pos = -1
        # obtiene las relaciones de la imagen a buscar
        prueba = getRelaciones(img)
        # recorre la lista de promedios
        for i in promedios:
            # calcula el error
            error = abs(prueba - i[0])/prueba * 100
            # si el error es menor al error actual
            if error < error_actual:
                # guarda el error actual
                error_actual = error
                # guarda la posicion
                pos = pathPruebas.index(img)

        # imprime el resultado al finalizar el recorrido
        print("La imagen", img, "se identifica a",
              promedios[pos][1], "con un error de", error_actual, "%")


def getRelacionesURL(url, nombre_descarga):
    # definimos la url del host donde estarán las imagenes
    url_primera_parte = ""
    # agregamos
    # por ejemplo la url solo es el nombre de la persona juan.jpg
    # entonces la url completa es http://localhost:5000/juan.jpg
    url_total = url_primera_parte + url
    # verificamos que el nombre de la descarga este en el path correcto
    # si no esta lo agregamos
    if nombre_descarga.__contains__("img/"):
        # descargamos la imagen
        aa.descargar_imagen(url_total, nombre_descarga)
    else:
        # descargamos la imagen
        aa.descargar_imagen(url_total, "img/" + nombre_descarga)
        nombre_descarga = "img/" + nombre_descarga

    # obtenemos las relaciones de la imagen
    relaciones = getRelaciones(nombre_descarga)
    # eliminarmos la imagen
    aa.eliminarArchivo(nombre_descarga)
    # retornamos el nombre de la imagen
    return relaciones


def getRelacionesURLprueba(url, nombre_descarga):
    # agregamos
    # por ejemplo la url solo es el nombre de la persona juan.jpg
    # entonces la url completa es http://localhost:5000/juan.jpg
    url_total = url
    # verificamos que el nombre de la descarga este en el path correcto
    # si no esta lo agregamos
    if nombre_descarga.__contains__("img/"):
        # descargamos la imagen
        #aa.descargar_imagen(url_total, nombre_descarga)
        pass
    else:
        # descargamos la imagen
        #aa.descargar_imagen(url_total, "img/" + nombre_descarga)
        nombre_descarga = "img/" + nombre_descarga

    # obtenemos las relaciones de la imagen
    relaciones = getRelaciones(nombre_descarga)
    # imprimo solo para dar un visual de lo que usamos
    print(nombre_descarga)
    # eliminarmos la imagen
    # aa.eliminarArchivo(nombre_descarga)
    # retornamos el nombre de la imagen
    return relaciones
