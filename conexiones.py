# pip install MySQL
import MySQLdb
from calculoFacial import getRelacionesURLprueba, getRelaciones


host = "localhost"
user = "root"
port = "3306"
passwd = "1234"
dbName = "datosrf"
tablaIntegrantes = "integrantes"
tablaDatos = "datos_rf"
tablaValores = "valores"


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

    for image in tablaNoAnalizados:
        # image[0] nos da el id de la foto
        # image[1] nos da el id_integrante
        # image[2] nos da el nombre de la foto
        # image[3] nos da el estado de la foto
        nombre = str(image[2])
        # obtenemos las relaciones de la imagen
        relaciones = getRelacionesURLprueba("", nombre)
        # obtenemos el id
        id_dato = image[0]

        # obtenemos el id de la persona
        id_integrante = image[1]

        # guardamos en la lista
        listaID.append(id_dato)
        listaAnalisis.append((id_integrante, relaciones))

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
        promedio = (valor + valorBD)/2
        # agregamos el id y el promedio
        ductUpdate[id] = promedio
        dictID_Promedios.pop(id)
    # retornamos el diccionario
    return (ductUpdate, dictID_Promedios)


def insertarValores(cur, dictID_Promedios):
    # inicializamos la cadena
    # necesita un update
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
    cadena = "UPDATE"+tablaValores+" SET valor = "
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
        print("sin valores para analizar")
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
        # pass
    modificarEstado(cur, tuplaID)

    return getTablaValores(cur)


def buscarImagen(valores, url):
    valorImg = getRelaciones(url)
    print(valorImg)
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
    print(resultados)


valores = analizarBasesdeDatos()
print(valores)
url = "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/buscar/h1.jpg"

buscarImagen(valores, url)
url = "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/buscar/h3.jpg"

buscarImagen(valores, url)
url = "C:/Users/Orlando/Desktop/git/NuevoProyecto/img/buscar/h2.jpg"

buscarImagen(valores, url)
