import time

import gensim
from gensim.models import LdaModel, CoherenceModel
from nltk.corpus import stopwords
import spacy

from src.python.deteccion_de_plagio import limpiar
from src.python.logging_example import log
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import corpora

def prepare_text_for_lda(archivo):
    nlp = spacy.load('es_core_news_sm')
    sw = stopwords.words('spanish')
    archivo_mas_limpio = []
    for oracion in archivo:
        sustantivos = nouns(nlp, oracion)
        oracion_mas_limpia = [palabra for palabra in sustantivos if not palabra in sw and not str(palabra).isnumeric()]
        oracion_lematizada = [lemmatize(palabra) for palabra in oracion_mas_limpia]
        archivo_mas_limpio = archivo_mas_limpio + [palabra for palabra in oracion_lematizada if str(palabra) != '']
    return archivo_mas_limpio

def nouns(nlp, texts):
    texts_out = [token.text for token in nlp(texts.lower()) if token.pos_ in ['NOUN'] and len(token.text) > 2]
    return texts_out

def lemmatize(word):
    return WordNetLemmatizer().lemmatize(word)

def display_topics(model):
  for topic_idx, topic in enumerate(model.print_topics()):
    print ("Topic %d:" % topic_idx)

def obtener_tema_del_texto(archivo, archivos_entrenamiento):
    textos_entrenamiento = [limpiar(archivo.texto) for archivo in archivos_entrenamiento if archivo != None]
    textos_preparados_entrenamiento = [prepare_text_for_lda(archivo) for archivo in textos_entrenamiento]
    texto_preparado_test = prepare_text_for_lda(archivo) # unseen_document

    dictionary = corpora.Dictionary(textos_preparados_entrenamiento)
    corpus = [dictionary.doc2bow(texto) for texto in textos_preparados_entrenamiento]
    lda_model = gensim.models.LdaMulticore(corpus, num_topics=10, id2word=dictionary, passes=2, workers=2)
    #for idx, topic in lda_model.print_topics(-1):
     #   print('Topic: {} \nWords: {}'.format(idx, topic))

    for index, score in sorted(lda_model[dictionary.doc2bow(texto_preparado_test)], key=lambda tup: -1 * tup[1]):
        print("Score: {}\t Topic: {}".format(score, lda_model.print_topic(index, 5)))
