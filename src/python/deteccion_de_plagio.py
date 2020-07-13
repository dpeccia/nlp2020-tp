import time
import requests
from googlesearch import search
from bs4 import BeautifulSoup
from nltk import word_tokenize
from metodos_de_similitud import obtener_similitud
from helper import porcentajes_de_aparicion_internet, porcentajes_de_aparicion_otros_tps, preparar_oracion, mutex
from procesamiento_de_archivos import limpiar


def obtener_oracion_mas_parecida_del_dataset(oracion, oracion_preparada, archivo_test_txt, archivos_entrenamiento, sw):
    mayor_porcentaje = 0.0
    oracion_mas_parecida = ''
    archivo_donde_se_encontro = ''
    archivo_donde_se_encontro_txt = ''
    ubicacion_dentro_de_la_lista = 0

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
                        archivo_donde_se_encontro = archivo.nombre + archivo.extension
                        ubicacion_dentro_de_la_lista = int(archivo.texto.index(oracion_a_comparar))
                        archivo_donde_se_encontro_txt = archivo.texto
    ubicacion_principio = sum(map(len, map(word_tokenize, archivo_donde_se_encontro_txt[:ubicacion_dentro_de_la_lista])))
    ubicacion_fin = ubicacion_principio + len(word_tokenize(oracion_mas_parecida))
    ubicacion_donde_se_encontro = f"({ubicacion_principio}, {ubicacion_fin})"
    porcentajes_de_aparicion_otros_tps.append((oracion, oracion_mas_parecida, mayor_porcentaje, archivo_donde_se_encontro, ubicacion_donde_se_encontro))


def obtener_html_como_texto(url):
    try:
        html = requests.get(url).text
    except requests.exceptions.ConnectionError:
        return ''
    soup = BeautifulSoup(html, features='lxml')
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


def obtener_oracion_mas_parecida_de_internet(oracion, oracion_preparada, sw, cantidad_de_links, buscar_en_pdfs):
    mayor_porcentaje = 0.0
    oracion_mas_parecida = ''
    url_donde_se_encontro = ''
    archivo_donde_se_encontro = ''
    ubicacion_dentro_de_la_lista = 0

    mutex.acquire()
    for url in search(oracion_preparada, tld="com.ar", num=cantidad_de_links, stop=cantidad_de_links, pause=2):
        time.sleep(0.002)
        mutex.release()
        if (not buscar_en_pdfs) and url.endswith(".pdf") or str(url).endswith(".pdf/"):
            mutex.acquire()
            continue
        else:
            texto = obtener_html_como_texto(url)
            if texto != '':
                archivo = limpiar(texto)
                for oracion_a_comparar in archivo:
                    oracion_a_comparar_preparada = preparar_oracion(oracion_a_comparar, sw)
                    if oracion_a_comparar_preparada is None:
                        continue
                    similitud = obtener_similitud(oracion_preparada, oracion_a_comparar_preparada)
                    if similitud > 0.8:
                        mayor_porcentaje = similitud
                        oracion_mas_parecida = oracion_a_comparar
                        url_donde_se_encontro = url
                        archivo_donde_se_encontro = archivo
                        ubicacion_dentro_de_la_lista = int(archivo.index(oracion_a_comparar))
                        break
                    elif similitud > mayor_porcentaje:
                        mayor_porcentaje = similitud
                        oracion_mas_parecida = oracion_a_comparar
                        url_donde_se_encontro = url
                        archivo_donde_se_encontro = archivo
                        ubicacion_dentro_de_la_lista = int(archivo.index(oracion_a_comparar))
        if mayor_porcentaje > 0.8:
            break
        mutex.acquire()
    time.sleep(0.002)
    mutex.release()
    ubicacion_principio = sum(map(len, map(word_tokenize, archivo_donde_se_encontro[:ubicacion_dentro_de_la_lista])))
    ubicacion_fin = ubicacion_principio + len(word_tokenize(oracion_mas_parecida))
    ubicacion_donde_se_encontro = f"({ubicacion_principio}, {ubicacion_fin})"
    porcentajes_de_aparicion_internet.append((oracion, oracion_mas_parecida, mayor_porcentaje, url_donde_se_encontro, ubicacion_donde_se_encontro))
