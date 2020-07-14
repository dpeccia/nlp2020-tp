# Detector de Plagio

#### Trabajo Práctico Individual realizado para la materia _Procesamiento del Lenguaje Natural_ en la UTN FRBA - 1er cuatrimestre 2020

Consiste en detectar el nivel de plagio de un Trabajo Práctico _T_, presentado por un alumno _X_, incluyendo la posibilidad de detectar parafraseos que no hayan sido debidamente citados

Esta detección no se limita a los trabajos prácticos de otros años, presentados por otros alumnos sino que además tiene en cuenta la web, libros, papers, proceedings y cualquier otra fuente de información de la cual se pudiera estar cometiendo plagio

Además de detectar el plagio, se indica claramente, en qué líneas o palabras (ubicación relativa) se encontró, a quien o quienes se está plagiando y se da la posibilidad de ver o revisar ambos textos (pudiendo ser referencias a links, trabajos de otros alumnos, libros, etc)

Código realizado en Python3. Documento que acompaña al código: [TP Plagio - Diego Peccia.pdf](/TP%20Plagio%20-%20Diego%20Peccia.pdf)

Video del algoritmo funcionando [acá](https://drive.google.com/file/d/1-1UNlB-egbrgAvQCuFdceIJaF6b-B__-/view?usp=sharing)

## Como ejecutarlo

Para ejecutar el programa debemos tener previamente instalado Python3. Yo opté por usar un ambiente de Miniconda:

#### Paso 1: Librerías 
Si es la primera vez que se va a ejecutar el algoritmo, deberemos ejecutar en el _Anaconda Powershell Prompt_, con el ambiente previamente activado, el archivo **_librerias.bat_** ubicado en la carpeta del repositorio

#### Paso 2: Configuración
Seteamos configuracion en **_config.yml_**:
* _path_archivos_entrenamiento_: ubicación de los archivos o trabajos prácticos anteriores (dataset) donde se desee consultar el plagio
* _path_archivo_test_: ubicación del archivo del que querremos detectar el plagio
* _path_resultado_: ubicación donde querremos almacenar el archivo resultado del algoritmo de detección de plagio
* _cantidad_de_topicos_: cantidad de palabras clave, tema, o tópicos del texto de test que querremos que el algoritmo nos diga para luego poder identificar el tema más fácilmente
* _cantidad_de_links_: cantidad de links de google donde querremos que el detector busque si hay plagio (por oración)
* _buscar_en_pdfs_: True o False. Si queremos que, en caso de que uno de los links donde se busca plagio sea un pdf que haya que descargar, se busque plagio ahí también o no

#### Paso 3: Archivos a analizar
Poner en la ubicación que seteamos en el _path_archivos_entrenamiento_ todos los trabajos prácticos anteriores y el archivo a analizar en la ubicación que seteamos en el _path_archivo_test_ en alguno de los siguientes formatos: _.txt, .doc, .docx, .pdf, .ppt, .pptx_

#### Paso 4: Exclusiones
Opcionalmente podemos agregar en el archivo **_Texto excluido de plagio.txt_** texto que no nos gustaría que se analizara el plagio. Está más que nada pensado para consignas de trabajos prácticos. En caso de que no deseemos excluir nada, dejamos el archivo vacío

#### Paso 5: Ejecución
Finalmente para ejecutar el algoritmo, ponemos en el _Anaconda PowerShell Prompt_, con el ambiente previamente activado, posicionados en el directorio _~repositorio/src/python/_ : `python main.py`

Podremos ir viendo las etapas por las que va pasando el algoritmo en los logs de la consola

## Resultado

El resultado se guardará en un archivo en la ubicación que seteamos en el _path_resultado_ con el nombre de **_Plagio <nombre_del_tp>.pdf_** en el que se podrá ver:
* Nombre del archivo de texto procesado
* Tópico o Tema del texto procesado
* Nombre y apellido del alumno que realizó el TP
* Cantidad de Plagios encontrados y cuanto tiempo se tardó
* Porcentaje de plagio del texto en general
* Listado de frases (y su ubicación dentro del texto) que podrían ser plagios de otros TPs previamente subidos o bien copiados de internet en una tabla con las siguientes columnas: Oración plagiada (oración del archivo de texto procesado), oración original (oración del lugar donde se plagió), lugar donde se encontró (con un hipervínculo al archivo o página de internet donde se encontró), ubicación dentro del archivo en el que se encontró

Ejemplo de resultado del detector de plagio: [/Resultado/Plagio Trabajo Práctico de Ejemplo.pdf](/Resultado/Plagio%20Trabajo%20Pr%C3%A1ctico%20de%20Ejemplo.pdf)
