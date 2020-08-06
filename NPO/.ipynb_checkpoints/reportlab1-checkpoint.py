# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Reportlab
# [examples](https://recursospython.com/guias-y-manuales/crear-documentos-pdf-en-python-con-reportlab/)

# Las dimensiones de una hoja están expresadas en puntos (points), no en píxeles, equivaliendo un punto a 1/72 pulgadas. Una hoja A4 está constituida por 595.2 puntos de ancho (width) y 841.8 puntos de alto (height). origen de las coordenadas (esto es, la posición (0, 0)) se encuentra en el extremo inferior izquierdo. Al crear una instancia de canvas.Canvas podemos especificar una dimensión alternativa para cada una de las hojas vía el parámetro pagesize, pasando una tupla cuyo primer elemento representa el ancho en puntos y el segundo, el alto. 

# c.showPage() antes de guardar el documento. Este método le indica a ReportLab que ya hemos terminado de trabajar en la hoja actual y queremos pasar a la siguiente. Aunque todavía no hemos trabajado con una segunda hoja (y no aparecerá en el documento en tanto no se haya dibujado nada) es una buena práctica recordar hacerlo antes de invocar c.save(). Para insertar imagenes en un documento PDF ReportLab hace uso de la librería Pillow, que se instala sencillamente vía pip install Pillow.El método drawImage() toma como argumento la ruta de una imagen (soporta múltiples formatos tales como PNG, JPEG y GIF) y la posición (x, y) en la que se quiere insertar. Podemos achicar o agrandar la imagen indicando sus dimensiones vía los argumentos width y height.

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter, landscape, portrait
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, Flowable, SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib import randomtext
from reportlab import platypus

print(letter,A4)


def pntopd (file, figs, x, y, w, he, ori, size):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4, letter, landscape, portrait
    w, h = size
    c = canvas.Canvas(file, pagesize=ori(size))
    for png in figs:
        c.drawImage(png, x, h - y, width=w, height=he)
        c.showPage()
    c.save()
    


from datetime import date
from pathlib import Path
ruta = "C:/SQLite"
today = date.today()
dat_dir = Path(ruta)
tit = today.strftime("%y%m%d") + '_ParameterAudit'
pdf_file = tit + ".pdf"
pdf_path = dat_dir / pdf_file
pnglist = ['C0.png', 'C4387.png', 'C9712.png', 'C9685.png', 'C4364.png']
pntopd(pdf_file, pnglist, 50, 550, 500, 500, portrait, letter)

w, h = letter
c = canvas.Canvas("hola-mundo.pdf", pagesize=portrait(letter))
# c.drawString(50, h - 50, "¡Hola, mundo!")
c.drawImage("C0.png", 50, h - 550, width=500, height=500)
c.showPage()
c.drawImage("C4387.png", 50, h - 550, width=500, height=500)
c.showPage()
c.drawImage("C9712.png", 50, h - 550, width=500, height=500)
c.showPage()
c.drawImage("C9685.png", 50, h - 550, width=500, height=500)
c.showPage()
c.drawImage("C4364.png", 50, h - 550, width=500, height=500)
c.showPage()
c.save()

lWidth, lHeight = letter
if orientation == 'landscape':
    canvas.setPageSize((lHeight, lWidth))
else:
    canvas.setPageSize((lWidth, lHeight))

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
w, h = A4
c = canvas.Canvas("figuras.pdf", pagesize=A4)
c.drawString(30, h - 50, "Línea")
x = 120
y = h - 45
c.line(x, y, x + 100, y)
c.drawString(30, h - 100, "Rectángulo")
c.rect(x, h - 120, 100, 50)
c.drawString(30, h - 170, "Círculo")
c.circle(170, h - 165, 20)
c.drawString(30, h - 240, "Elipse")
c.ellipse(x, y - 170, x + 100, y - 220)
c.showPage()
c.save()


