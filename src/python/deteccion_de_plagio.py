import re
import requests
import unicodedata
from nltk import sent_tokenize
from nltk import word_tokenize
from googlesearch import search
from bs4 import BeautifulSoup
from src.python.metodos_de_similitud import obtener_similitud

def limpiar(archivo):
    archivo_limpio = re.sub(r'\n+', '\n', archivo.strip()) # reemplazo multiples enter por uno solo
    archivo_limpio = re.sub('\n', '. ', archivo_limpio.strip())
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
            if palabras_oracion[0].islower() or palabras_oracion[0].isnumeric():
                oraciones_mas_limpias[j] += " " + oraciones_limpias[i]
            else:
                j += 1
                oraciones_mas_limpias.append(oraciones_limpias[i])
        i += 1

    return oraciones_mas_limpias

def obtener_oracion_mas_parecida_del_dataset(oracion, archivo_test_txt, archivos_entrenamiento_txt):
    mayor_porcentaje = 0.0
    oracion_mas_parecida = ''
    archivo_donde_se_encontro = ''
    for archivo in archivos_entrenamiento_txt:
        if (archivo != None and obtener_similitud(archivo_test_txt.texto, archivo.texto) < 0.9):
            for oracion_a_comparar in limpiar(archivo.texto):
                similitud = obtener_similitud(oracion.lower(), oracion_a_comparar.lower())
                if similitud > mayor_porcentaje:
                    mayor_porcentaje = similitud
                    oracion_mas_parecida = oracion_a_comparar
                    archivo_donde_se_encontro = archivo.nombre

    #return re.sub('[^A-Za-z0-9áéíóúñ:/ ]+', ' ', oracion), re.sub('[^A-Za-z0-9áéíóúñ:/ ]+', ' ', oracion_mas_parecida), mayor_porcentaje, archivo_donde_se_encontro
    return oracion, oracion_mas_parecida, mayor_porcentaje, archivo_donde_se_encontro


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

def obtener_oracion_mas_parecida_de_internet(oracion):
    mayor_porcentaje = 0.0
    oracion_mas_parecida = ''
    url_donde_se_encontro = ''
    for url in search(re.sub('[^A-Za-z0-9áéíóúñ:/ ]+', ' ', oracion.lower()), tld="com.ar", num=2, stop=2):
        print('Buscando: ' + oracion + '\n En URL: ' + url + '\n')
        texto = obtener_html_como_texto(url)
        if texto != '':
            for oracion_a_comparar in sent_tokenize(texto.strip()):
                similitud = obtener_similitud(oracion.lower(), oracion_a_comparar.lower())
                if (similitud > mayor_porcentaje):
                    mayor_porcentaje = similitud
                    oracion_mas_parecida = oracion_a_comparar
                    url_donde_se_encontro = url

    return (re.sub('[^A-Za-z0-9áéíóúñ:/ ]+', ' ', oracion), re.sub('[^A-Za-z0-9áéíóúñ:/ ]+', ' ', oracion_mas_parecida),
            mayor_porcentaje, url_donde_se_encontro)