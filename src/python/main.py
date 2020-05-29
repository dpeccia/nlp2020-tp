import os
from src.python.logging_example import *
from src.python.nombre_del_alumno import obtener_nombre_y_apellido_del_alumno
from src.python.procesamiento_de_archivos import convertir_archivo_a_txt

def main():
    log.debug("A quirky message only developers care about")
    log.info("Curious users might want to know this")
    log.warning("Something is wrong and any user should be informed")
    log.error("Serious stuff, this is red for a reason")
    log.critical("OH NO everything is on fire")
    archivos_entrenamiento = os.listdir("../../Entrenamiento/")
    archivo_test = os.listdir("../../Test/")
    # set([os.path.splitext(archivo)[1] for archivo in archivos_entrenamiento]) # obtengo las extensiones de los archivos
    archivos_entrenamiento_txt = [convertir_archivo_a_txt("../../Entrenamiento/" + archivo) for archivo in archivos_entrenamiento]
    archivo_test_txt = [convertir_archivo_a_txt("../../Test/" + archivo) for archivo in archivo_test][0]

    nombre_archivo = archivo_test_txt.nombre  # la extension hace falta?

    nombre_alumno = obtener_nombre_y_apellido_del_alumno(archivo_test_txt)
    print(nombre_alumno)

    # Obtener Plagio de otros tps
    # falta ver que tp pasó primero, que porcentaje poner como limite, que las consignas no sean plagio

    # porcentajes_de_aparicion = [obtener_oracion_mas_parecida_del_dataset(oracion, archivo_test_txt, archivos_entrenamiento_txt) for oracion in sent_tokenize(archivo_test_txt.texto.strip())]
    # plagio_de_otros_tps = [(oracion, posible_plagio, porcentaje, archivo) for (oracion, posible_plagio, porcentaje, archivo) in porcentajes_de_aparicion if porcentaje > 0.7]

    # Obtener plagio de paginas de internet

    # porcentajes_de_aparicion = [obtener_oracion_mas_parecida_de_internet(oracion) for oracion in sent_tokenize(archivo_test_txt.texto.strip())]
    # plagio_de_internet = [(oracion,posible_plagio,porcentaje,archivo) for (oracion,posible_plagio,porcentaje,archivo) in porcentajes_de_aparicion if porcentaje>0.7]

if __name__ == '__main__':
    main()
