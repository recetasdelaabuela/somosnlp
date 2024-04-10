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
import unicodedata
import re

# Configuración de la codificación
sys.stdout.reconfigure(encoding='utf-8')

# Función para limpiar texto
def limpiar_texto(texto):
    # Comprobar si el texto es una cadena de texto
    if isinstance(texto, str):
        # Eliminar caracteres no ASCII
        #texto_limpio = re.sub(r'[^\x00-\x7F]+', ' ', texto)
        # Normalizar caracteres a su forma NFC
        #texto_limpio = unicodedata.normalize('NFC', texto_limpio)
        # Normalizar caracteres a su forma NFC
        texto_normalizado = unicodedata.normalize('NFC', texto)

        # Sustituir valores extraños por su representación UTF-8 correspondiente
        texto_sustituido = texto_normalizado.encode('utf-8', 'ignore').decode('utf-8')

    elif pd.isna(texto):
        print('Es un nan')
        texto_sustituido = ''
    else:
        # Si no es una cadena de texto, devolver el valor original
        print(str(texto))
        texto_sustituido = ''
    return texto_sustituido

def formateaUTF8(nombre_archivo):
    try:
        # Leer fichero
        print('Leyendo fichero ' + nombre_archivo)
        df = pd.read_csv(nombre_archivo, encoding='utf-8')
        #df = pd.read_csv(nombre_archivo, encoding='ISO-8859-1')

        # Limpiar texto en las columnas "input" y "output"
        df['input'] = df['input'].apply(limpiar_texto)
        df['output'] = df['output'].apply(limpiar_texto)

        # Contabilizar el numero de filas
        num_filas = len(df)
        print(f"El archivo '{nombre_archivo}' tiene {num_filas} filas.")
        print(str(df.iloc[0]))

        # Guardar el DataFrame actualizado en el mismo archivo CSV
        df.to_csv(nombre_archivo, index=False, encoding='utf-8')

    except FileNotFoundError:
        print("El archivo no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")


def execute(name):
    # Configuración del logger
    logging.basicConfig(filename='./FormateaUTF8.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Crear un logger
    logger = logging.getLogger()

    # Lee fichero y formatea
    logger.info("Starting script %s" % name)
    nombre_archivo = './comebien_it.csv'
    formateaUTF8(nombre_archivo)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    execute("Formatea UTF-8")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
