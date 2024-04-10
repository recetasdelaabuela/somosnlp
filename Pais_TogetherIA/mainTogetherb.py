# This is a sample Python script.
# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import csv
import together
import time
import pandas as pd
#import math
#import requests
#import io
import sys
import logging

# Configuración de la codificación
sys.stdout.reconfigure(encoding='utf-8')

together.api_key = "xxx" # Replace with your Together API Key

def eliminar_duplicados(nombre_archivo):
    try:
        # Leer fichero
        print('Leyendo fichero ' + nombre_archivo)
        df = pd.read_csv(nombre_archivo)

        # Contabilizar el numero de filas
        num_filas = len(df)
        print(f"El archivo '{nombre_archivo}' tiene {num_filas} filas.")

        # Leer el contenido del archivo CSV y eliminar duplicados en la columna "URL"
        df = df.drop_duplicates(subset=["URL"])

        # Guardar el DataFrame actualizado en el mismo archivo CSV
        df.to_csv(nombre_archivo, index=False)

    except FileNotFoundError:
        print("El archivo no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def determinar_pais(texto):
    try:
        if not isinstance(texto, str):
            return ""
        if (texto == ""):
            return ""
        texto = texto.lower()
    except Exception as e:
        print(f"determinar_pais error: {e} en {texto}")

    # Lista de palabras clave para países hispanoamericanos comunes
    paises = {
        "España": ["españa", "spain", "español", "española", "españoles", "españolas"],
        "Mexico": ["mexico", "méxico", "méjico", "méjico", "tex-mex", "azteca", "mexicano", "mexicana", "mexicanos", "mexicanas", "mejicano", "mejicana", "mejicanos", "mejicanas"],
        "Guatemala": ["guatemala", "guatemalteco", "guatemalteca", "quiché", "guatemaltecos", "guatemaltecas"],
        "El salvador": ["el salvador", "salvadoreño", "salvadoreña", "cuscatleco", "cuscatleco", "salvadoreños", "salvadoreñas"],
        "Honduras": ["honduras", "hondureño", "hondureña", "catracho", "catracha", "hondureños", "hondureñas"],
        "Nicaragua": ["nicaragua", "nicaragüense", "nicaragüenses", "pinolero", "pinolera"],
        "Costa rica": ["costa rica", "costarricense", "costarricenses"],
        "Panama": ["panamá", "panameño", "panameña", "canalero", "canalera", "panameños", "panameñas"],
        "Colombia": ["colombia", "colombiano", "colombiana", "cafetero", "cafetera", "colombianos", "colombianas"],
        "Ecuador": ["ecuador", "ecuatoriano", "ecuatoriana", "ecuatorianos", "ecuatorianas"],
        "Peru": ["peru", "perú", "peruano", "peruana", "inca", "incaico", "incaica", "peruanos", "peruanas"],
        "Bolivia": ["bolivia", "boliviano", "boliviana", "bolivianos", "bolivianas"],
        "Chile": ["chile", "chileno", "chilena", "mapuche", "chilenos", "chilenas"],
        "Argentina": ["argentina", "argentino", "argentina",  "gaucho", "gaucha", "argentinos", "argentinas"],
        "Uruguay": ["uruguay", "uruguayo", "uruguaya", "charrúa", "uruguayos", "uruguayas"],
        "Paraguay": ["paraguay", "paraguayo", "paraguaya", "guaraní", "paraguayos", "paraguayas"],
        "Venezuela": ["venezuela", "venezolano", "venezolana", "bolivariano", "bolivariana", "venezolanos", "venezolanas"],
        "Puerto rico": ["puerto rico", "puertorriqueño", "puertorriqueña", "boricua", "puertorriqueños", "puertorriqueñas"],
        "Guinea ecuatorial": ["guinea ecuatorial", "ecuatoguineano", "ecuatoguineana", "ecuatoguineanos", "ecuatoguineanas"],
        "República dominicana": ["republica dominicana", "república dominicana", "dominicano", "dominicana", "quisqueyano", "quisqueyana", "dominicanos", "dominicanas"],
        "Cuba": ["cuba", "cubano", "cubana", "isleño", "isleña", "cubanos", "cubanas"],
        "Haiti": ["haiti", "haití", "haitiano", "haitiana", "haitianos", "haitianas"],
    }

    # Buscar coincidencias entre las palabras clave y el texto
    for pais, palabras_clave in paises.items():
        for palabra in palabras_clave:
            if palabra in texto:
                return pais

    # Si no se encontraron coincidencias
    return ""


def determine_country_withWords(contexto):
    return determinar_pais(contexto)

def determine_country_withIA(contexto, logger):
    #question = "Tell me in spanish and in one single word which is the most probable origin country from the recipe? "
    question = ". Classify the previous recipe into one of the following list of countries: "
    paises = """España, México, Guatemala, El Salvador, Honduras, Nicaragua, Costa Rica, Panamá, Colombia, Ecuador, 
    Perú, Bolivia, Chile, Argentina, Uruguay, Paraguay, Venezuela, Puerto Rico, República_Dominicana, Cuba, Haití, Guinea_Ecuatorial"""
    #myprompt = "[INST] " + str(question) + str(contexto) + "[/INST]"
    #mypromtp = contexto + " Question: " + question + " Answer: "
    #mypromtp = question + paises + " Recipe: " + contexto + " Answer? "
    myprompt = "[INST] " + str(contexto) + str(question) + str(paises) +  "[/INST]"

    endpoint = 'https://api.together.xyz/inference'
    #payload = {
    #    #"model": "togethercomputer/RedPajama-INCITE-7B-Chat",
    #    'model': "mistralai/Mixtral-8x7B-Instruct-v0.1",
    #    "prompt": myprompt,
    #    "max_tokens": 1,
    #    "temperature": 0.1,
    #    "top_p": 1,
    #    "top_k": 30,
    #    "repetition_penalty": 1
    #}
    #headers = {
    #    "accept": "application/json",
    #    "content-type": "application/json",
    #    "Authorization": "Bearer 04c4c8b5d4fc108e63683099f16e32fb338e9e05916ef3511e7910f60653a1ae",
    #    "User-Agent": "<ComeBien>"
    #}

    #response = requests.post(endpoint, json=payload, headers=headers)
    #print(response)
    #generatedText = response['output']['choices'][0]['text']

    try:
        generatedText = ''
        output = together.Complete.create(
            prompt=myprompt,
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            max_tokens=30, temperature=0.1, top_p=1, top_k=30, repetition_penalty=1,
            #max_tokens=30, temperature=0.8,
        )
        # parse the completion then print the whole output
        generatedText = output['output']['choices'][0]['text']
    except Exception as e:
        logger.info(f"Together error: {e}, {contexto}")
        logger.info('Continuando en 10s')
        time.sleep(10)

    pais = determine_country_withWords(generatedText)
    return pais

def execute(name):
    # Ubicacion ficheros
    dir = 'G:/DatasetsRecetas/'
    filename_logger = dir + 'RecetasGratis.log'
    nombre_archivo = dir + 'RecetasGratis.csv'
    nombre_archivo_nuevo = dir + 'RecetasGratisNuevo.csv'

    # Configuración del logger
    logging.basicConfig(filename=filename_logger, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Crear un logger
    logger = logging.getLogger()

    # Lee fichero y elimina duplicados
    logger.info("Starting script %s" % name)
    eliminar_duplicados(nombre_archivo)

    # Carga el archivo CSV en un DataFrame
    df = pd.read_csv(nombre_archivo)

    # Contabilizar el numero de filas
    num_filas = len(df)
    logger.info(f"El archivo '{nombre_archivo}' tiene {num_filas} filas.")

    try:
        # Itera sobre cada receta e imprímela en pantalla
        num_country_gentilicio = 0
        num_country_nombre = 0
        num_country_ia = 0
        num_country = 0
        num_country_intl = 0
        num_country_notfound = 0
        # Iterar sobre el objet pandas, extraer columna 'Contexto' y 'Nombre' y modificar la columna 'Pais' según determinacion pais
        for indice, fila in df.iterrows():
            pais_encontrado = False
            contexto = fila['Contexto']
            pais = fila['Pais']
            num_country = num_country + 1

            if (pais == "") or (not isinstance(pais, str)):
                country_gentilicio = determine_country_withWords(contexto)
                if country_gentilicio != "":
                    num_country_gentilicio = num_country_gentilicio + 1
                    pais_encontrado = True
                    pais = country_gentilicio
                    logger.info(str(num_country) + " - X Pais " + str(country_gentilicio) + " en " + str(contexto))
                else:
                    # Filtrar el DataFrame por el valor del contexto
                    try:
                        #nombre = df.loc[df['Contexto'] == contexto, 'Nombre'].iloc[0]
                        nombre = fila['Nombre']
                    except Exception as e:
                        logger.info(f"{num_country} - Receta nombre error: {e}, {contexto}")
                    country_nombre = determine_country_withWords(nombre)
                    if country_nombre != "":
                        num_country_nombre = num_country_nombre + 1
                        pais_encontrado = True
                        pais = country_nombre
                        logger.info(str(num_country) + " - N Pais " + str(country_nombre) + " en " + str(nombre))
                    else:
                        country_ia = determine_country_withIA(contexto, logger)
                        tiempo_espera = 1
                        time.sleep(tiempo_espera)
                        if country_ia != "":
                            pais_encontrado = True
                            pais = country_ia
                            num_country_ia = num_country_ia + 1
                            logger.info(str(num_country) + " - IA C Pais " + str(country_ia) + " con nombre " + str(nombre))
                        else:
                            country_ia = determine_country_withIA(nombre, logger)
                            time.sleep(tiempo_espera)
                            if country_ia != "":
                                pais_encontrado = True
                                pais = country_ia
                                num_country_ia = num_country_ia + 1
                                logger.info(str(num_country) + " - IA N Pais " + str(country_ia) + " en nombre " + str(nombre))
                            else:
                                # Asigna pais internacional por defecto cuando no ha encontrado ninguno
                                pais_encontrado = True
                                num_country_notfound = num_country_notfound + 1
                                country_intl = 'Internacional'
                                pais = country_intl
                                logger.info(str(num_country) + " - IA No Pais " + str(country_intl) + " ni contexto ni nombre " + str(nombre))
            else:
                if (pais == 'Internacional'):
                    num_country_intl = num_country_intl + 1

            if pais_encontrado:
                # Modificar el valor de la columna 'Pais' en la fila actual
                df.at[indice, 'Pais'] = pais

            # Guardar cada x recetas el DataFrame en un nuevo archivo CSV
            if num_country % 1000 == 0 :
                df.to_csv(nombre_archivo_nuevo, index=False)

        logger.info("Números de países encontrados mediante palabras clave: "+str(num_country_gentilicio))
        logger.info("Números de países encontrados mediante nombre receta: "+str(num_country_nombre))
        logger.info("Números de países encontrados mediante IA Together: " + str(num_country_ia))
        logger.info("Números de países Internacional: " + str(num_country_intl))
        logger.info("Números de países no encontrados: " + str(num_country_notfound))

        # Guardar el DataFrame en un nuevo archivo CSV
        df.to_csv(nombre_archivo_nuevo, index=False)

    except Exception as e:
        logger.info(f"{num_country} - Error {e} en {contexto}")


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    execute("Test Together IA")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
