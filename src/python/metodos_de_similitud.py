import math
import re
from collections import Counter

def obtener_similitud_del_coseno(vector1, vector2):
    interseccion = set(vector1.keys()) & set(vector2.keys())
    numerador = sum([vector1[x] * vector2[x] for x in interseccion])

    sum1 = sum([vector1[x] ** 2 for x in vector1.keys()])
    sum2 = sum([vector2[x] ** 2 for x in vector2.keys()])
    denominador = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominador:
        return 0.0
    else:
        return float(numerador) / denominador

def string_a_vector(texto):
    palabras = re.compile(r'\w+').findall(texto)
    return Counter(palabras)

def obtener_similitud(texto1, texto2):
    vector1 = string_a_vector(texto1)
    vector2 = string_a_vector(texto2)
    return obtener_similitud_del_coseno(vector1, vector2)