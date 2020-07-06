import datetime
import threading
import time

from nltk.corpus import stopwords
from src.python.deteccion_de_plagio import obtener_oracion_mas_parecida_del_dataset, limpiar, obtener_oracion_mas_parecida_de_internet
from src.python.logging_example import *
from src.python.procesamiento_de_archivos import obtener_archivos, guardar_resultado_en_word
from src.python.nombre_del_alumno import obtener_nombre_y_apellido_del_alumno
from nltk import sent_tokenize, word_tokenize

from src.python.tema_del_texto import obtener_tema_del_texto


def es_titulo(oracion):
    sw = stopwords.words('spanish')
    oracion_en_palabras = [palabra for palabra in word_tokenize(oracion) if not palabra in sw]
    oracion_sin_stopwords = ''
    for palabra in oracion_en_palabras:
        oracion_sin_stopwords += " " + palabra
    return oracion_sin_stopwords.strip().istitle()

def obtener_nombre_alumno(archivo):
    global nombre_alumno
    nombre_alumno = obtener_nombre_y_apellido_del_alumno(archivo)
    if nombre_alumno:
        log.info("Alumno que realizo el ensayo: " + nombre_alumno[0])
    else:
        log.warning("No se encontro el nombre del alumno")

# Obtener Plagio de otros tps
# falta ver que tp pasó primero, que porcentaje poner como limite, que las consignas no sean plagio
def obtener_plagio_de_otros_tps(archivo_test, archivos_entrenamiento, texto_archivo_test_limpio):
    log.info("Obteniendo plagio de otros tps...")
    hilos_plagio_de_otros_tps = list()

    for oracion in texto_archivo_test_limpio:
        hilo_plagio_de_otros_tps = threading.Thread(target=obtener_oracion_mas_parecida_del_dataset, args=(oracion, archivo_test, archivos_entrenamiento,))
        hilos_plagio_de_otros_tps.append(hilo_plagio_de_otros_tps)
        hilo_plagio_de_otros_tps.start()

    for index, thread in enumerate(hilos_plagio_de_otros_tps):
        thread.join()

    global plagio_de_otros_tps
    plagio_de_otros_tps = [(oracion, posible_plagio, porcentaje, archivo) for
                           (oracion, posible_plagio, porcentaje, archivo) in porcentajes_de_aparicion_otros_tps if
                           (porcentaje > 0.7) and not es_titulo(oracion)]
    log.info(f"{len(plagio_de_otros_tps)} plagios de otros tps encontrados")

def obtener_plagio_de_internet(texto_archivo_test_limpio):
    log.info("Obteniendo plagio de paginas de internet...")
    hilos_plagio_de_internet = list()

    for oracion in texto_archivo_test_limpio:
        hilo_plagio_de_internet = threading.Thread(target=obtener_oracion_mas_parecida_de_internet, args=(oracion,))
        hilos_plagio_de_internet.append(hilo_plagio_de_internet)
        hilo_plagio_de_internet.start()

    for index, thread in enumerate(hilos_plagio_de_internet):
        thread.join()

    global plagio_de_internet
    plagio_de_internet = [(oracion, posible_plagio, porcentaje, archivo) for
                          (oracion, posible_plagio, porcentaje, archivo) in porcentajes_de_aparicion_internet if
                          (porcentaje > 0.7) and not es_titulo(oracion)]
    log.info(f"{len(plagio_de_internet)} plagios de paginas de internet encontrados")

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
        texto_archivo_test_limpio = limpiar(archivo_test.texto)

        tiempo_inicial = time.time()

        threads = list()

        hilo_tema = threading.Thread(target=obtener_tema_del_texto, args=(texto_archivo_test_limpio, archivos_entrenamiento,))
        threads.append(hilo_tema)
        hilo_tema.start()

        '''
        hilo_nombre_alumno = threading.Thread(target=obtener_nombre_alumno, args=(archivo_test,))
        threads.append(hilo_nombre_alumno)
        hilo_nombre_alumno.start()

        hilo_plagio_de_otros_tps = threading.Thread(target=obtener_plagio_de_otros_tps, args=(archivo_test, archivos_entrenamiento, texto_archivo_test_limpio,))
        threads.append(hilo_plagio_de_otros_tps)
        hilo_plagio_de_otros_tps.start()

        hilo_plagio_de_internet = threading.Thread(target=obtener_plagio_de_internet, args=(texto_archivo_test_limpio,))
        threads.append(hilo_plagio_de_internet)
        hilo_plagio_de_internet.start()
        '''

        for index, thread in enumerate(threads):
            thread.join()

        '''
        plagio = plagio_de_otros_tps.copy()
        for (oracion, posible_plagio, porcentaje, url) in plagio_de_internet:
            if not any(oracion == otra_oracion for (otra_oracion, _, _, _) in plagio):
                plagio += [(oracion, posible_plagio, porcentaje, url)]

        tiempo_final = time.time()
        tiempo_que_tardo = datetime.timedelta(seconds=tiempo_final-tiempo_inicial)
        log.info(f"Total de {len(plagio)} plagios encontrados en {tiempo_que_tardo} hs")

        guardar_resultado_en_word(nombre_archivo, nombre_alumno, plagio, tiempo_que_tardo)
        '''

    else:
        log.error("No se encontro ningun archivo para verificar plagio")
        log.error("Cerrando detector de plagio...")

if __name__ == '__main__':
    main()