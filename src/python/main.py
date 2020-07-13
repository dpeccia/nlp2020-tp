import datetime
import os
import threading
import time
import yaml
from src.python.funciones_principales import obtener_nombre_alumno, obtener_plagio_de_otros_tps, obtener_plagio_de_internet
from src.python.helper import *
from src.python.procesamiento_de_archivos import obtener_archivos, guardar_resultado, limpiar, \
    limpiar_archivos_entrenamiento, excluida, correctamente_citada
from src.python.tema_del_texto import obtener_tema_del_texto


def main():
    log.info("Iniciando detector de plagio ...")
    tiempo_inicial = time.time()

    with open("../../config.yml", "r") as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)

    archivos_entrenamiento = obtener_archivos(config["path_archivos_entrenamiento"])
    if not archivos_entrenamiento:
        log.warning("No se encontraron archivos en la carpeta entrenamiento, solo se buscara plagio de Internet")

    archivos_test = obtener_archivos(config["path_archivo_test"])
    if archivos_test:
        archivo_test = archivos_test[0]
        nombre_archivo = archivo_test.nombre + archivo_test.extension
        log.info("Analizando plagio en: " + nombre_archivo)
        texto_archivo_test_limpio = limpiar(archivo_test.texto)

        texto_archivo_test_sin_oraciones_excluidas = [oracion for oracion in texto_archivo_test_limpio if not excluida(oracion)]

        sw = stopwords.words('spanish')

        hilos_limpieza_archivos = list()

        for archivo in archivos_entrenamiento:
            if archivo is not None:
                hilo_limpieza_archivos = threading.Thread(target=limpiar_archivos_entrenamiento, args=(archivo,))
                hilos_limpieza_archivos.append(hilo_limpieza_archivos)
                hilo_limpieza_archivos.start()

        hilos_principales = list()
        
        hilo_nombre_alumno = threading.Thread(target=obtener_nombre_alumno, args=(texto_archivo_test_limpio, sw,))
        hilos_principales.append(hilo_nombre_alumno)
        hilo_nombre_alumno.start()

        hilo_plagio_de_internet = threading.Thread(target=obtener_plagio_de_internet,
                                                   args=(texto_archivo_test_sin_oraciones_excluidas, sw, int(config["cantidad_de_links"]), bool(config["buscar_en_pdfs"]),))
        hilos_principales.append(hilo_plagio_de_internet)
        hilo_plagio_de_internet.start()

        for index, thread in enumerate(hilos_limpieza_archivos):
            thread.join()
        '''
        hilo_tema = threading.Thread(target=obtener_tema_del_texto,
                                     args=(texto_archivo_test_limpio, sw, int(config["cantidad_de_topicos"]),))
        hilos_principales.append(hilo_tema)
        hilo_tema.start()
'''
        hilo_plagio_de_otros_tps = threading.Thread(target=obtener_plagio_de_otros_tps,
                                                    args=(texto_archivo_test_sin_oraciones_excluidas, sw, ))
        hilos_principales.append(hilo_plagio_de_otros_tps)
        hilo_plagio_de_otros_tps.start()

        for index, thread in enumerate(hilos_principales):
            thread.join()

        log.info("Obteniendo resultados finales ...")

        plagio = plagio_de_otros_tps.copy()
        for (oracion, posible_plagio, porcentaje, url, ubicacion) in plagio_de_internet:
            if not any(oracion == otra_oracion for (otra_oracion, _, _, _, _) in plagio):
                if not correctamente_citada(url, texto_archivo_test_limpio):
                    plagio += [(oracion, posible_plagio, porcentaje, url, ubicacion)]

        tiempo_final = time.time()
        tiempo_que_tardo_str = str(datetime.timedelta(seconds=tiempo_final-tiempo_inicial)).split(":")
        if tiempo_que_tardo_str[1] == "00":
            tiempo_que_tardo = f"{tiempo_que_tardo_str[2].split('.')[0]} segundos"
        else:
            tiempo_que_tardo = f"{tiempo_que_tardo_str[1]} minutos, {tiempo_que_tardo_str[2].split('.')[0]} segundos"
        log.info(f"Total de {len(plagio)} plagios encontrados en {tiempo_que_tardo}")

        porcentaje_de_plagio = int((len(plagio) * 100) / len(texto_archivo_test_limpio))
        guardar_resultado(nombre_archivo, nombre_alumno, topico_con_mas_score, plagio, tiempo_que_tardo, porcentaje_de_plagio, config["path_resultado"], config["path_archivos_entrenamiento"])
        log.info("El detector de plagio finalizo correctamente!")
        log.info(f"Porcentaje de plagio: {porcentaje_de_plagio} %")
        log.info(f'Resultado guardado en: {os.path.abspath(config["path_resultado"])}\\Plagio {str(str(nombre_archivo).split(".")[0])}.docx')
    else:
        log.error("No se encontro ningun archivo para verificar plagio")
        log.error("Cerrando detector de plagio...")


if __name__ == '__main__':
    main()
