from fpdf import FPDF
from datetime import datetime
import mediapipe as mp
import cv2
import MySQLdb
import os
import requests


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
        nombre_local_imagen = "archivos/img/" + nombre_local_imagen

    # agregamos la extension
    if not nombre_local_imagen.__contains__(".jpg"):
        nombre_local_imagen = nombre_local_imagen + ".jpg"

    # descargamos
    imagen = requests.get(url_imagen, stream=True).content
    cwd = os.getcwd()
    print(cwd)
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


def obtener_nombre_archivos(path):
    return tuple(os.listdir(path))


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
                    # Si puede calcular la tangente
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


def getRelacionesURL(nombre_archivo):
    # obtenemos las relaciones de la imagen
    relaciones = getRelaciones(nombre_archivo)

    # retornamos la lista
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


def existe_dir():
    # verificamos si existe la carpeta
    if not os.path.exists("pdf"):
        os.makedirs("pdf")


def gen_pdf(resultados, url):
    x = 50
    y = 10
    now = datetime.now()

    existe_dir()

    # definimos el tamaño y las unidades de medicion
    pdf = FPDF(orientation='P', unit='mm', format='Letter')
    # agregamos una pagina
    pdf.add_page()

    # agregamos una imagen dada por el url
    pdf.image(url, 50, 10, 100, 100)
    pdf.set_font('helvetica', size=12)

    pdf.text(x, y+105, txt="Se ha identificado a:")

    txt = " "+resultados[1]+" "+resultados[2]+" "+resultados[3]
    txt = txt.upper()
    pdf.text(x, y+110, txt=txt)
    # definimos el tipo de letra, estilo y tamaño
    txt = "Alias: " + resultados[4] + "   Fecha de nacimiento: "+resultados[5]
    pdf.set_font('helvetica', size=10)
    pdf.text(x, y+115, txt=txt)
    # sub info
    txt = "Ocupación: " + resultados[6]
    pdf.text(x, y+120, txt=txt)
    # descripcion y otra cosa
    txt = "Dirección: "+resultados[7]
    pdf.text(x, y+125, txt=txt)

    txt_guardar = str(now.day) + str(now.month) + str(now.year)
    txt_guardar = resultados[1]+resultados[2]+resultados[3]+txt_guardar

    pos = len(url)
    for i in reversed(url):
        if i == "/":
            break
        pos -= 1
    url = url[pos:]
    pdf.output("pdf/"+txt_guardar+url+".pdf", 'F')

    return txt_guardar


def gen_pdf(resultados, url, error):
    x = 50
    y = 10
    now = datetime.now()

    existe_dir()

    # definimos el tamaño y las unidades de medicion
    pdf = FPDF(orientation='P', unit='mm', format='Letter')
    # agregamos una pagina
    pdf.add_page()

    # agregamos una imagen dada por el url
    pdf.image(url, 50, 10, 100, 100)
    pdf.set_font('helvetica', size=12)

    pdf.text(x, y+105, txt="Se ha identificado a:")

    txt = " "+resultados[1]+" "+resultados[2]+" "+resultados[3]
    txt = txt.upper()
    pdf.text(x, y+110, txt=txt)
    # definimos el tipo de letra, estilo y tamaño
    txt = "Alias: " + resultados[4] + "   Fecha de nacimiento: "+resultados[5]
    pdf.set_font('helvetica', size=10)
    pdf.text(x, y+115, txt=txt)
    # sub info
    txt = "Ocupación: " + resultados[6]
    pdf.text(x, y+120, txt=txt)
    # descripcion y otra cosa
    txt = "Dirección: "+resultados[7]
    pdf.text(x, y+125, txt=txt)
    # error
    pdf.set_font('helvetica', size=12)
    pdf.text(x, y+130, txt="Certeza calculada: " +
             str(round(100 - error, 2)) + "%")

    txt_guardar = str(now.day) + str(now.month) + str(now.year)
    txt_guardar = resultados[1]+resultados[2]+resultados[3]+txt_guardar

    pos = len(url)
    # quitar la ruta donde se encuentra
    for i in reversed(url):
        if i == "/":
            break
        pos -= 1
    url = url[pos:]
    # quitar el .jpg de la ruta
    url = url[:-4]

    pdf.output("pdf/"+txt_guardar+".pdf", 'F')

    return txt_guardar


host = "localhost"
user = "root"
port = "3306"
passwd = "1234"
dbName = "datosrf"
tablaIntegrantes = "integrantes"
tablaDatos = "datos_rf"
tablaValores = "valores"
tablaValoresSP = "valoresSP"


def conectarDB():

    db = MySQLdb.connect(
        host=host,    # your host, usually localhost
        user=user,
        passwd=passwd,  # your password
        db=dbName)        # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()

    return cur


def obtenerNoAnalizados(cur):
    cur.execute("SELECT * FROM "+tablaDatos+" WHERE estado = 0")

    return cur.fetchall()


def analizarNuevasFotos(cur):
    # obtenemos la tabla de los datos no analizados
    tablaNoAnalizados = obtenerNoAnalizados(cur)

    # aqui se guardaran los resultados
    listaID = []
    listaAnalisis = []
    error = []
    error_pagina = []

    valor_temp = 0

    for image in tablaNoAnalizados:
        nombre = "temp"
        # image[0] nos da el id de la foto
        # image[1] nos da el id_integrante
        # image[2] nos da el nombre de la foto
        # image[3] nos da el estado de la foto
        url = str(image[2])

        if not verificar_pagina(url):
            error_pagina.append(url)
            continue

        # descargamos la imagen
        url = descargar_imagen(url, nombre)

        # verificamos que se haya descargado la imagen
        if not existe(url):
            error.append(url)
            continue

        # obtenemos las relaciones de la imagen
        relaciones = getRelacionesURL(url)

        # eliminarmos la imagen
        eliminarArchivo(url)

        # obtenemos el id del dato
        id_dato = image[0]

        # obtenemos el id de la persona
        id_integrante = image[1]

        # guardamos en la lista
        listaID.append(id_dato)
        listaAnalisis.append((id_integrante, relaciones))

        valor_temp += 1

    if len(error) != 0:
        print("Error al descargar las siguientes imagenes:")
        for e in error:
            print(e)

    return (tuple(listaID), tuple(listaAnalisis))


def modificarEstado(cur, tuplaID):
    # inicializamos la modificacion
    cadena = "UPDATE "+tablaDatos+" SET estado = 1 where id = "
    # recorremos la lista
    for dato in tuplaID:
        # obtenemos el id y agregamos
        cadena = cadena + str(dato) + " OR id = "

    # quitamos el ultimo or id y agregamos el semicolon
    cadena = cadena[0:len(cadena)-len(" OR id = ")] + ";"
    # ejecutamos la modificacion
    cur.execute(cadena)
    # guardamos los cambios
    cur.connection.commit()


def promediarRelaciones(tuplaAnalisis):
    # inicializamos el diccionario de promedios
    # la key sera el id y su valor sera el valor
    dictPromedios = {}
    ids = []
    # recorremos la lista
    for id in tuplaAnalisis:
        # obtenemos el id
        ids.append(id[0])
    # obtenemos los id que no se repiten
    listaIDs = set(ids)
    # recorremos la lista de ids
    for id in listaIDs:
        listaTempValores = []
        for listaID_Valor in tuplaAnalisis:
            if listaID_Valor[0] == id:
                listaTempValores.append(listaID_Valor[1])
        # obtenemos el promedio
        promedio = sum(listaTempValores)/len(listaTempValores)
        # agregamos el promedio a la lista
        dictPromedios[id] = promedio
    return dictPromedios


def verificarRepetido(cur, dictID_Promedios):
    # inicializamos la cadena
    cadena = "SELECT * FROM "+tablaValores+" WHERE id_integrante = "
    # recorremos la tupla
    for id in dictID_Promedios.keys():
        # obtenemos el id
        cadena = cadena + str(id) + " OR id_integrante = "
    # quitamos la ultima parte
    cadena = cadena[0:len(cadena)-len(" OR id_integrante = ")] + ";"
    # ejecutamos la cadena
    cur.execute(cadena)
    # guardamos los cambios
    cur.connection.commit()
    # obtenemos los resultados
    resultados = cur.fetchall()
    # inicializamos la lista
    dictID_Promedios_BD = {}
    # recorremos los resultados
    for resultado in resultados:
        # agregamos el id
        dictID_Promedios_BD[resultado[0]] = resultado[1]
    # retornamos la lista
    return dictID_Promedios_BD


# falta promediar los promedios
def redefinirValores(dictID_Promedios, dictID_Promedios_BD):
    # Nuevo para el update
    ductUpdate = {}
    # recorremos el diccionario
    for id in dictID_Promedios_BD.keys():
        # obtenemos el valor
        valor = dictID_Promedios[id]
        # obtenemos el valor de la base de datos
        valorBD = dictID_Promedios_BD[id]
        # obtenemos el promedio
        promedio = (valor + float(valorBD))/2
        # agregamos el id y el promedio
        ductUpdate[id] = promedio
        dictID_Promedios.pop(id)
    # retornamos el diccionario
    return (ductUpdate, dictID_Promedios)


def insertarValores(cur, dictID_Promedios):
    # inicializamos la cadena
    cadena = "INSERT INTO "+tablaValores+" (id_integrante, valor) VALUES "
    # recorremos la tupla
    for id in dictID_Promedios.keys():
        # obtenemos el id
        cadena = cadena + "(" + str(id) + ", " + \
            str(dictID_Promedios[id]) + "), "

    # quitamos la ultima coma
    cadena = cadena[0:len(cadena)-2] + ";"
    # ejecutamos la cadena
    cur.execute(cadena)
    # guardamos los cambios
    cur.connection.commit()


def updateValores(cur, dictUpdate):
    # inicializamos la cadena
    cadena = "UPDATE "+tablaValores+" SET valor = "
    # recorremos la tupla
    for id in dictUpdate.keys():
        # obtenemos el id
        cadena = cadena + str(dictUpdate[id]) + \
            " WHERE id_integrante = " + str(id) + ";"
        # ejecutamos la cadena
        cur.execute(cadena)
        # guardamos los cambios
        cur.connection.commit()

# Este analisis es desde la base de datos de pandilleros, donde se conoce
# los datos y el id_del_integrante


def getTablaValores(cur):
    cadena = "select * from " + tablaValores
    cur.execute(cadena)
    cur.connection.commit()
    resultados = cur.fetchall()
    cur.close()
    return resultados


def analizarBasesdeDatos():
    # conectamos a la db
    cur = conectarDB()

    # Analizamos las fotos nuevas que han sido agregadas
    # a la base de datos
    tuplaTotal = analizarNuevasFotos(cur)

    # obtenemos la tupla de los id (id de la foto) de las no analizadas
    tuplaID = tuplaTotal[0]

    # obtenemos el id de los integrantes y su valor
    tuplaAnalisis = tuplaTotal[1]

    # si no hay valores para analizar, acabamos
    if (len(tuplaAnalisis) == 0):
        return getTablaValores(cur)

    # obtenemos el promedio de las relaciones
    dictID_Promedios = promediarRelaciones(tuplaAnalisis)

    # obtenemos los valores de la base de datos
    dictID_Promedios_BD = verificarRepetido(cur, dictID_Promedios)

    # si en la base de datos hay valores, estos se tendran que redefinir
    # promediando una vez mas
    if (len(dictID_Promedios_BD) != 0):
        dictUpdate = redefinirValores(
            dictID_Promedios, dictID_Promedios_BD)
        dictID_Promedios = dictUpdate[1]
        dictUpdate = dictUpdate[0]

        # falta hace update
        if (len(dictID_Promedios) != 0):
            insertarValores(cur, dictID_Promedios)
        updateValores(cur, dictUpdate)

    # si no hay valores anteriores a la base de datos, agregamos
    else:
        insertarValores(cur, dictID_Promedios)

    modificarEstado(cur, tuplaID)

    return getTablaValores(cur)


def buscarImagen(valores, url):

    if not verificar_pagina(url):
        print("No se pudo conectar a la pagina")
        return

    nombre = "temp"

    url = descargar_imagen(url, nombre)

    if not existe(url):
        return

    valorImg = getRelaciones(url)

    # variable para el error
    error = 101
    # error por cada recorrido
    error_actual = 101
    # posicion en la lista de imagenes
    pos = -1
    # calcula el error

    for valor in valores:
        error = abs(valorImg - float(valor[1]))/valorImg * 100
        # si el error es menor al error actual
        if error < error_actual:
            # guarda el error actual
            error_actual = error
            # guarda la posicion
            pos = valor[0]

    cur = conectarDB()
    cadena = "select * from " + tablaIntegrantes + \
        " where id_integrante = " + str(pos)

    cur.execute(cadena)
    cur.connection.commit()
    resultados = cur.fetchall()

    # cerramos db
    cur.close()

    gen_pdf(resultados[0], url, error)

    eliminarArchivo(url)


if __name__ == "__main__":
    valores = analizarBasesdeDatos()

    url = "https://raw.githubusercontent.com/ouarIT/img/main/img16.jpg"
    buscarImagen(valores, url)

    url = "https://raw.githubusercontent.com/ouarIT/img/main/img17.jpg"
    buscarImagen(valores, url)

    url = "https://raw.githubusercontent.com/ouarIT/img/main/img18.jpg"
    buscarImagen(valores, url)
