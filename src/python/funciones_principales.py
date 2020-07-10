import threading

from nltk.corpus import stopwords
from src.python.deteccion_de_plagio import obtener_oracion_mas_parecida_del_dataset, \
    obtener_oracion_mas_parecida_de_internet
from src.python.helper import nombre_alumno, log, plagio_de_otros_tps, porcentajes_de_aparicion_otros_tps, \
    plagio_de_internet, porcentajes_de_aparicion_internet, preparar_oracion, archivos_entrenamiento_limpios
from src.python.nombre_del_alumno import obtener_nombre_y_apellido_del_alumno


def obtener_nombre_alumno(archivo, sw):
    log.info("NOMBRE_ALUMNO | Obteniendo nombre del alumno ...")
    nombre_alumno.extend(obtener_nombre_y_apellido_del_alumno(archivo, sw))
    if nombre_alumno:
        log.info("NOMBRE_ALUMNO | Alumno que realizo el ensayo: " + nombre_alumno[0])
    else:
        log.warning("NOMBRE_ALUMNO | No se encontro el nombre del alumno")

# Obtener Plagio de otros tps
# falta ver que tp pasó primero, que porcentaje poner como limite, que las consignas no sean plagio
def obtener_plagio_de_otros_tps(texto_archivo_test_limpio, sw):
    log.info("PLAGIO_DE_TPS | Obteniendo plagio de otros tps...")
    hilos_plagio_de_otros_tps = list()

    for oracion in texto_archivo_test_limpio:
        oracion_preparada = preparar_oracion(oracion, sw)
        if oracion_preparada is None:
            continue

        archivos_entrenamiento = archivos_entrenamiento_limpios
        hilo_plagio_de_otros_tps = threading.Thread(target=obtener_oracion_mas_parecida_del_dataset,
                                                    args=(oracion, oracion_preparada, texto_archivo_test_limpio, archivos_entrenamiento, sw,))
        hilos_plagio_de_otros_tps.append(hilo_plagio_de_otros_tps)
        hilo_plagio_de_otros_tps.start()

    for index, thread in enumerate(hilos_plagio_de_otros_tps):
        thread.join()

    plagio_de_otros_tps.extend([(oracion, posible_plagio, porcentaje, archivo) for
                           (oracion, posible_plagio, porcentaje, archivo) in porcentajes_de_aparicion_otros_tps if
                           (porcentaje > 0.7)])
    log.info(f"PLAGIO_DE_TPS | {len(plagio_de_otros_tps)} plagios de otros tps encontrados")


def obtener_plagio_de_internet(texto_archivo_test_limpio, sw):
    log.info("PLAGIO_DE_INTERNET | Obteniendo plagio de paginas de internet...")
    hilos_plagio_de_internet = list()

    for oracion in texto_archivo_test_limpio:
        oracion_preparada = preparar_oracion(oracion, sw)
        if oracion_preparada is None:
            continue
        hilo_plagio_de_internet = threading.Thread(target=obtener_oracion_mas_parecida_de_internet, args=(oracion, oracion_preparada, sw,))
        hilos_plagio_de_internet.append(hilo_plagio_de_internet)
        hilo_plagio_de_internet.start()

    for index, thread in enumerate(hilos_plagio_de_internet):
        thread.join()

    plagio_de_internet.extend([(oracion, posible_plagio, porcentaje, archivo) for
                          (oracion, posible_plagio, porcentaje, archivo) in porcentajes_de_aparicion_internet if
                          (porcentaje > 0.7)])
    log.info(f"PLAGIO_DE_INTERNET | {len(plagio_de_internet)} plagios de paginas de internet encontrados")
