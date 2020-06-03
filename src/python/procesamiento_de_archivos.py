import os
from tika import parser

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