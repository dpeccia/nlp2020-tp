import os
from tika import parser
from docx import Document
from docx.shared import Inches
import time

class ArchivoTxt:
    def __init__(self, nombre, extension, texto):
        self.nombre = nombre
        self.extension = extension
        self.texto = texto

def obtener_archivos(nombre_directorio):
    archivos = os.listdir(nombre_directorio)
    return [convertir_archivo_a_txt(nombre_directorio, archivo) for archivo in archivos]

def convertir_documento_a_txt(archivo, nombre_directorio):
    raw = parser.from_file(nombre_directorio + archivo)
    return raw['content']

def convertir_archivo_a_txt(nombre_directorio, archivo):
    archivo_nombre, archivo_extension = os.path.splitext(archivo)
    if archivo_extension != ".pptx":
        archivo_txt = convertir_documento_a_txt(archivo, nombre_directorio)
        return ArchivoTxt(archivo_nombre, archivo_extension, archivo_txt)

def guardar_resultado_en_word(nombre_archivo, nombre_alumno, plagio, tiempo_que_tardo):
    document = Document()

    document.add_heading(f'Análisis de plagio sobre: {nombre_archivo}', 0)

    p = document.add_paragraph('Nombre del alumno que realizo el TP: ')
    p.add_run(nombre_alumno[0]).italic = True

    document.add_heading('Análisis de plagio', level=1)
    document.add_paragraph(f'Total de {len(plagio)} encontrados en {tiempo_que_tardo}')

    table = document.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Oración plagiada'
    hdr_cells[1].text = 'Oración original'
    hdr_cells[2].text = 'Lugar donde se encontró'
    for oracion, plagio, porcentaje, url in plagio:
        row_cells = table.add_row().cells
        row_cells[0].text = oracion
        row_cells[1].text = plagio
        row_cells[2].text = url

    document.add_page_break()

    nombre_archivo_plagio = '../../Resultado/Plagio ' + str(str(nombre_archivo).split(".")[0]) + '.docx'

    document.save(nombre_archivo_plagio)
