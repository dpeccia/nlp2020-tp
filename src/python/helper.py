import logging
from colorlog import ColoredFormatter
from nltk import word_tokenize, re
from nltk.corpus import stopwords

LOG_LEVEL = logging.DEBUG
LOGFORMAT = "  %(log_color)s%(asctime)-8s%(reset)s %(log_color)s| %(log_color)s%(levelname)s%(reset)s %(log_color)s| %(log_color)s%(message)s%(reset)s"
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log = logging.getLogger('pythonConfig')
log.setLevel(LOG_LEVEL)
log.addHandler(stream)

global archivos_entrenamiento_limpios
archivos_entrenamiento_limpios = []

global porcentajes_de_aparicion_otros_tps
porcentajes_de_aparicion_otros_tps = []

global porcentajes_de_aparicion_internet
porcentajes_de_aparicion_internet = []

global topico_con_mas_score
topico_con_mas_score = []

global nombre_alumno
nombre_alumno = []

global plagio_de_otros_tps
plagio_de_otros_tps = []

global plagio_de_internet
plagio_de_internet = []

global textos_preparados_entrenamiento
textos_preparados_entrenamiento = []

def preparar_oracion(oracion, sw):
    if str(oracion).endswith('?'):
        return None
    oracion_mas_preparada = re.sub('á', 'a', oracion.strip())
    oracion_mas_preparada = re.sub('é', 'e', oracion_mas_preparada.strip())
    oracion_mas_preparada = re.sub('í', 'i', oracion_mas_preparada.strip())
    oracion_mas_preparada = re.sub('ó', 'o', oracion_mas_preparada.strip())
    oracion_mas_preparada = re.sub('ú', 'u', oracion_mas_preparada.strip())
    oracion_mas_preparada = re.sub(r'[^a-zA-Z0-9\s]', '', oracion_mas_preparada.strip())
    oracion_mas_preparada = re.sub(r'[ ][ ]+', ' ', oracion_mas_preparada.strip())
    oracion_en_palabras = [palabra for palabra in word_tokenize(oracion_mas_preparada) if not palabra in sw]
    if len(oracion_en_palabras) <= 3:
        return None
    oracion_mas_preparada = " ".join(oracion_en_palabras)
    if oracion_mas_preparada.strip().istitle():
        return None
    else:
        return oracion_mas_preparada.lower()
