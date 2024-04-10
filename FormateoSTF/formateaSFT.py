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

def count_rows(df, column, logger, nombre_archivo):
    num = len(df[column])
    logger.info(f"El archivo '{nombre_archivo}' con columna {column} tiene {num} filas.")

def formateaSFT(logger, nombre_archivo, nombre_archivo_nuevo):
    try:
        # Leer fichero
        logger.info('Leyendo fichero ' + nombre_archivo)
        df = pd.read_csv(nombre_archivo)

        # Contabilizar el numero de filas
        count_rows(df, 'human', logger, nombre_archivo)
        count_rows(df, 'bot', logger, nombre_archivo)

        # Agregar un texto delante de la columna 'human' y b delante de la columna 'bot'
        # human: how are you \n bot: I am fine
        df['text'] = df.apply(lambda row: 'human: ' + str(row['human']) + '\n bot: ' + str(row['bot']), axis=1)

        # Eliminar las columnas human y bot
        df = df.drop('human', axis=1)
        df = df.drop('bot', axis=1)

        # Guardar el DataFrame actualizado en el archivo CSV destino
        df.to_csv(nombre_archivo_nuevo, index=False)

        # Contabilizar el numero de filas
        num_filas = len(df)
        logger.info(f"El archivo '{nombre_archivo_nuevo}' tiene {num_filas} filas.")

    except Exception as e:
        logger.info(f"Error: {e}")


def execute(name):
    # Configuración del logger
    dir = 'G:/DatasetsRecetas/'
    filename = dir + name + '.log'
    nombre_archivo = dir + 'RecetasGratisIn.csv'
    nombre_archivo_nuevo = dir + 'RecetasGratisSFT.csv'

    logging.basicConfig(filename=filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Crear un logger
    logger = logging.getLogger()

    # Lee fichero y formatea SFT
    logger.info("Starting script %s" % name)
    formateaSFT(logger, nombre_archivo, nombre_archivo_nuevo)

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    execute("formateaSFT")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
