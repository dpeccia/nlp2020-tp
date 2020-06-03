from nltk.corpus import stopwords

from src.python.deteccion_de_plagio import obtener_oracion_mas_parecida_del_dataset, limpiar
from src.python.logging_example import *
from src.python.procesamiento_de_archivos import obtener_archivos
from src.python.nombre_del_alumno import obtener_nombre_y_apellido_del_alumno
from nltk import sent_tokenize, word_tokenize
import re

def es_titulo(oracion):
    sw = stopwords.words('spanish')
    oracion_en_palabras = [palabra for palabra in word_tokenize(oracion) if not palabra in sw]
    oracion_sin_stopwords = ''
    for palabra in oracion_en_palabras:
        oracion_sin_stopwords += " " + palabra
    return oracion_sin_stopwords.strip().istitle()

def main():
    log.info("Iniciando detector de plagio ...")

    archivos_entrenamiento = obtener_archivos("../../Entrenamiento/")
    if not archivos_entrenamiento:
        log.warning("No se encontraron archivos en la carpeta entrenamiento, solo se buscara plagio de Internet")

    archivos_test = obtener_archivos("../../Test/")
    if archivos_test:
        # set([os.path.splitext(archivo)[1] for archivo in archivos_entrenamiento]) # obtengo las extensiones de los archivos
        archivo_test = archivos_test[0]
        nombre_archivo = archivo_test.nombre + archivo_test.extension
        log.info("Analizando plagio en: " + nombre_archivo)
        nombre_alumno = obtener_nombre_y_apellido_del_alumno(archivo_test)
        if nombre_alumno:
            log.info("Alumno que realizo el ensayo: " + nombre_alumno[0])
        else:
            log.warning("No se encontro el nombre del alumno")

        # Obtener Plagio de otros tps
        # falta ver que tp pasó primero, que porcentaje poner como limite, que las consignas no sean plagio
        texto_archivo_test_limpio = limpiar(archivo_test.texto)
        porcentajes_de_aparicion = [obtener_oracion_mas_parecida_del_dataset(oracion, archivo_test, archivos_entrenamiento) for oracion in texto_archivo_test_limpio]
        plagio_de_otros_tps = [(oracion, posible_plagio, porcentaje, archivo) for (oracion, posible_plagio, porcentaje, archivo) in porcentajes_de_aparicion if (porcentaje > 0.7) and not es_titulo(oracion)]

        for (a, b, c, d) in plagio_de_otros_tps:
            print(f"{a} ; {b} ; {c} ; {d}")

        # Obtener plagio de paginas de internet

        # porcentajes_de_aparicion = [obtener_oracion_mas_parecida_de_internet(oracion) for oracion in sent_tokenize(archivo_test_txt.texto.strip())]
        # plagio_de_internet = [(oracion,posible_plagio,porcentaje,archivo) for (oracion,posible_plagio,porcentaje,archivo) in porcentajes_de_aparicion if porcentaje>0.7]
    else:
        log.error("No se encontro ningun archivo para verificar plagio")
        log.error("Cerrando detector de plagio...")

if __name__ == '__main__':
    main()