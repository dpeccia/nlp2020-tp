import time

import requests
from googlesearch import search
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

from src.python.metodos_de_similitud import obtener_similitud
from src.python.helper import porcentajes_de_aparicion_internet, porcentajes_de_aparicion_otros_tps, preparar_oracion, \
    log, archivos_entrenamiento_limpios, mutex
from src.python.procesamiento_de_archivos import limpiar


def obtener_oracion_mas_parecida_del_dataset(oracion, oracion_preparada, archivo_test_txt, archivos_entrenamiento, sw):
    mayor_porcentaje = 0.0
    oracion_mas_parecida = ''
    archivo_donde_se_encontro = ''

    for archivo in archivos_entrenamiento:
        if archivo is not None:
            if obtener_similitud(".".join(archivo_test_txt), ".".join(archivo.texto)) < 0.9:
                for oracion_a_comparar in archivo.texto:
                    oracion_a_comparar_preparada = preparar_oracion(oracion_a_comparar, sw)
                    if oracion_a_comparar_preparada is None:
                        continue
                    similitud = obtener_similitud(oracion_preparada, oracion_a_comparar_preparada)
                    if similitud > mayor_porcentaje:
                        mayor_porcentaje = similitud
                        oracion_mas_parecida = oracion_a_comparar
                        archivo_donde_se_encontro = archivo.nombre
    porcentajes_de_aparicion_otros_tps.append((oracion, oracion_mas_parecida, mayor_porcentaje, archivo_donde_se_encontro))

def obtener_html_como_texto(url):
    try:
        html = requests.get(url).text
    except requests.exceptions.ConnectionError:
        return ''
    soup = BeautifulSoup(html)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def obtener_oracion_mas_parecida_de_internet(oracion, oracion_preparada, sw):
    mayor_porcentaje = 0.0
    oracion_mas_parecida = ''
    url_donde_se_encontro = ''

    mutex.acquire()
    urls = search(oracion_preparada, tld="com.ar", num=2, stop=2, pause=2)
    time.sleep(0.002)
    mutex.release()

    for url in urls:
        if str(url).endswith(".pdf") or str(url).endswith(".pdf/"):
            continue
        else:
            #log.debug('PLAGIO_DE_INTERNET | Buscando: ' + oracion + '\n En URL: ' + url)
            texto = obtener_html_como_texto(url)
            if texto != '':
                for oracion_a_comparar in limpiar(texto):
                    oracion_a_comparar_preparada = preparar_oracion(oracion_a_comparar, sw)
                    if oracion_a_comparar_preparada is None:
                        continue
                    similitud = obtener_similitud(oracion_preparada, oracion_a_comparar_preparada)
                    if similitud > 0.8:
                        mayor_porcentaje = similitud
                        oracion_mas_parecida = oracion_a_comparar
                        url_donde_se_encontro = url
                        break
                    elif similitud > mayor_porcentaje:
                        mayor_porcentaje = similitud
                        oracion_mas_parecida = oracion_a_comparar
                        url_donde_se_encontro = url
        if mayor_porcentaje > 0.8:
            break
    porcentajes_de_aparicion_internet.append((oracion, oracion_mas_parecida, mayor_porcentaje, url_donde_se_encontro))