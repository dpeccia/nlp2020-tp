import re
import nltk
import spacy
import itertools
from nltk import line_tokenize, pos_tag
from nltk import word_tokenize
from nltk.corpus import stopwords

from src.python.deteccion_de_plagio import limpiar


def obtener_nombre_y_apellido_del_alumno(texto_dividido_en_oraciones, sw):
    nlp = spacy.load('es_core_news_sm')  # modelo para detectar Entidades (nombres)

    lineas_pasadas_por_el_modelo = [[(a.text, a.label_) for a in nlp(oracion).ents] for oracion in texto_dividido_en_oraciones]
    lista_flatenizada = list(itertools.chain.from_iterable(lineas_pasadas_por_el_modelo))  # flatten

    entidades_reconocidas_como_personas = [texto for (texto, categoria) in lista_flatenizada if categoria == 'PER']

    entidades_reconocidas_como_personas = [entidad for entidad in entidades_reconocidas_como_personas if not entidad.lower().strip() in sw]
    #print([entidad.split(' ', 1)[0] for entidad in entidades_reconocidas_como_personas])

    posibles_nombres_alumno = []
    # Fijarse cual de las entidades reconocidas como personas esta en un contexto como Nombre:, Integrantes:, etc
    for entidad in entidades_reconocidas_como_personas:
        contextos = nltk.Text(word_tokenize(". ".join(texto_dividido_en_oraciones))).concordance_list(entidad.split(' ', 1)[0])
        for contexto in contextos:
            #print(contexto.line)
            if list(map(str.lower, contexto.left)).__contains__('alumno') or \
               list(map(str.lower, contexto.left)).__contains__('alumna') or \
               list(map(str.lower, contexto.left)).__contains__('integrante') or \
               list(map(str.lower, contexto.left)).__contains__('apellido') or \
               list(map(str.lower, contexto.left)).__contains__('nombre'):
                posibles_nombres_alumno += [entidad]
    if posibles_nombres_alumno:
        return posibles_nombres_alumno
    else:
        return entidades_reconocidas_como_personas
