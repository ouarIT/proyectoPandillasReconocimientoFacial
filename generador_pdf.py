from fpdf import FPDF
from datetime import datetime
import os


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

    pdf.output("pdf/"+txt_guardar+url+".pdf", 'F')

    return txt_guardar
