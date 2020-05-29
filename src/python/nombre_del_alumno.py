import re
import spacy
import itertools
from nltk import line_tokenize
from nltk.corpus import stopwords

def obtener_nombre_y_apellido_del_alumno(archivo_test_txt):
    nombre_alumno = ''
    nlp = spacy.load('es_core_news_sm')  # modelo para detectar Entidades (nombres)

    texto_dividido_en_lineas = [re.sub('[^A-Za-z0-9áéíóúñ ]+', ' ', linea) for linea in line_tokenize(archivo_test_txt.texto.strip())]
    lineas_pasadas_por_el_modelo = [[(a.text, a.label_) for a in nlp(linea).ents] for linea in texto_dividido_en_lineas]
    lista_flatenizada = list(itertools.chain.from_iterable(lineas_pasadas_por_el_modelo))  # flatten

    entidades_reconocidas_como_personas = [texto for (texto, categoria) in lista_flatenizada if categoria == 'PER']

    sw = stopwords.words('spanish')
    entidades_reconocidas_como_personas = [entidad for entidad in entidades_reconocidas_como_personas if
                                           not entidad.lower().strip() in sw]

    # print([pos_tag(word_tokenize(entidad)) for entidad in entidades_reconocidas_como_personas])

    for entidad in entidades_reconocidas_como_personas:
        if entidad in archivo_test_txt.nombre:
            nombre_alumno = entidad

    if (nombre_alumno != ''):
        return nombre_alumno
    else:  # Fijarse cual de las entidades reconocidas como personas esta en un contexto como Nombre:, Integrantes:, etc
        return entidades_reconocidas_como_personas
        # print([nltk.Text(word_tokenize(archivo_test_txt.texto)).concordance(entidad) for entidad in entidades_reconocidas_como_personas])