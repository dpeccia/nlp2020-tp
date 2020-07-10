import os
import re

import unicodedata
from nltk import word_tokenize, sent_tokenize
from tika import parser
from docx import Document

from src.python.helper import archivos_entrenamiento_limpios


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

def limpiar(archivo):
    archivo_limpio = re.sub(r'\n+', '\n', archivo.strip()) # reemplazo multiples enter por uno solo
    archivo_limpio = re.sub('\n', '. ', archivo_limpio.strip())
    archivo_limpio = re.sub(r'[.][.]+', '.', archivo_limpio.strip())
    archivo_limpio = re.sub(r'[ ][ ]+', ' ', archivo_limpio.strip())
    archivo_limpio = re.sub('á', 'a', archivo_limpio.strip())
    archivo_limpio = re.sub('é', 'e', archivo_limpio.strip())
    archivo_limpio = re.sub('í', 'i', archivo_limpio.strip())
    archivo_limpio = re.sub('ó', 'o', archivo_limpio.strip())
    archivo_limpio = re.sub('ú', 'u', archivo_limpio.strip())
    archivo_limpio = re.sub('”', '"', archivo_limpio.strip())
    archivo_limpio = re.sub('“', '"', archivo_limpio.strip())
    archivo_limpio = re.sub('\u200b', ' ', archivo_limpio.strip())

    archivo_limpio = unicodedata.normalize("NFKD", archivo_limpio.strip())

    oraciones = sent_tokenize(archivo_limpio.strip(), "spanish")
    oraciones_limpias = []
    for oracion in oraciones:
        if oracion.strip() != '.':
            if oracion.strip().endswith('.'):
                oracion_a_agregar = oracion[:-1]
            else:
                oracion_a_agregar = oracion
            oraciones_limpias.append(oracion_a_agregar.strip())

    i=0
    j=0
    # TODO: para arreglar enters que deberian ser espacios para que siga la oracion (pasa en pdfs nomas)
    oraciones_mas_limpias = []
    while i < len(oraciones_limpias):
        if i == 0:
            oraciones_mas_limpias.append(oraciones_limpias[0])
        else:
            palabras_oracion = word_tokenize(oraciones_limpias[i])
            if palabras_oracion[0].islower():
                oraciones_mas_limpias[j] += " " + oraciones_limpias[i]
            else:
                j += 1
                oraciones_mas_limpias.append(oraciones_limpias[i])
        i += 1

    return oraciones_mas_limpias

def limpiar_archivos_entrenamiento(archivo):
    archivo_limpio = limpiar(archivo.texto)
    archivos_entrenamiento_limpios.append(ArchivoTxt(archivo.nombre, archivo.extension, archivo_limpio))

def guardar_resultado(nombre_archivo, nombre_alumno, topico_con_mas_score, plagio, tiempo_que_tardo, porcentaje_de_plagio):
    document = Document()

    document.add_heading(f'Análisis de plagio sobre: {nombre_archivo}', 0)

    p = document.add_paragraph('Tópicos del texto: ')
    p.add_run(" ".join(topico_con_mas_score)).italic = True

    p = document.add_paragraph('Nombre del alumno que realizo el TP: ')
    p.add_run(nombre_alumno[0]).italic = True

    document.add_heading('Análisis de plagio', level=1)
    document.add_paragraph(f'Total de {len(plagio)} encontrados en {tiempo_que_tardo}')
    document.add_paragraph(f'Porcentaje de plagio: {porcentaje_de_plagio}%')

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
