import threading

import gensim
from gensim.models import LdaModel
from nltk.corpus import stopwords
import spacy
from src.python.deteccion_de_plagio import limpiar
from src.python.helper import log, topico_con_mas_score, textos_preparados_entrenamiento, archivos_entrenamiento_limpios
from gensim import corpora


def preparar_texto_para_lda(archivo, nlp, sw):
    archivo_mas_limpio = []
    for oracion in archivo:
        sustantivos = obtener_sustantivos_lematizados(nlp, oracion)
        oracion_mas_limpia = [palabra for palabra in sustantivos if not palabra in sw and not str(palabra).isnumeric()]
        archivo_mas_limpio = archivo_mas_limpio + [palabra for palabra in oracion_mas_limpia if str(palabra) != '']
    return archivo_mas_limpio


def obtener_sustantivos_lematizados(nlp, texts):
    texts_out = [token.lemma_ for token in nlp(texts.lower()) if token.pos_ in ['NOUN'] and len(token.text) > 2]
    return texts_out

def preparar_archivo_entrenamiento_para_lda(archivo, nlp, sw):
    archivo_preparado = preparar_texto_para_lda(archivo, nlp, sw)
    textos_preparados_entrenamiento.append(archivo_preparado)

def obtener_tema_del_texto(archivo_test, sw, cantidad_de_topicos):
    log.info("TOPICOS | Obteniendo topicos del texto ...")
    log.debug("TOPICOS | Preparando archivos para modelo LDA ...")
    nlp = spacy.load('es_core_news_sm')

    hilos_preparar_archivos_para_lda = list()
    for archivo in archivos_entrenamiento_limpios:
        hilo_preparar_archivo_para_lda = threading.Thread(target=preparar_archivo_entrenamiento_para_lda,
                                                          args=(archivo.texto, nlp, sw,))
        hilos_preparar_archivos_para_lda.append(hilo_preparar_archivo_para_lda)
        hilo_preparar_archivo_para_lda.start()

    texto_preparado_test = preparar_texto_para_lda(archivo_test, nlp, sw)

    for index, thread in enumerate(hilos_preparar_archivos_para_lda):
        thread.join()

    log.debug("TOPICOS | Archivos de entrenamiento preparados")
    log.debug("TOPICOS | Corriendo algoritmo LDA para archivos de entrenamiento ...")
    diccionario = corpora.Dictionary(textos_preparados_entrenamiento)
    corpus = [diccionario.doc2bow(texto) for texto in textos_preparados_entrenamiento]
    modelo_lda = gensim.models.LdaMulticore(corpus, num_topics=10, id2word=diccionario, passes=2)

    log.debug("TOPICOS | Algoritmo LDA para archivos de entrenamiento finalizado")
    log.debug("TOPICOS | Corriendo algoritmo LDA para archivos de test ...")
    indice, score = sorted(modelo_lda[diccionario.doc2bow(texto_preparado_test)], key=lambda tup: -1 * tup[1])[0]
    topico_con_mas_score.extend(
        [palabra.split("*")[1].replace("\"", "") for palabra in modelo_lda.print_topic(indice, cantidad_de_topicos).split(" + ")])

    log.info(f"TOPICOS | Topicos del texto: {topico_con_mas_score}")
