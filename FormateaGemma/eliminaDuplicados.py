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

together.api_key = "04c4c8b5d4fc108e63683099f16e32fb338e9e05916ef3511e7910f60653a1ae" # Replace with your Together API Key

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


def execute(name):
    # Configuración del logger
    logging.basicConfig(filename='./EliminaDuplicados.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Crear un logger
    logger = logging.getLogger()

    # Lee fichero y elimina duplicados
    logger.info("Starting script %s" % name)
    nombre_archivo = '../TestTogetherIA/RecetasGratis.csv'
    eliminar_duplicados(nombre_archivo)

    # Carga el archivo CSV en un DataFrame
    df = pd.read_csv(nombre_archivo)

    # Contabilizar el numero de filas
    num_filas = len(df)
    logger.info(f"El archivo '{nombre_archivo}' tiene {num_filas} filas.")

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    execute("Test Together IA")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
