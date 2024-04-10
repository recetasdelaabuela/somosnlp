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
        count_rows(df, 'Nombre', logger, nombre_archivo)
        count_rows(df, 'Pasos', logger, nombre_archivo)

        # Agregar un texto delante de la columna 'human' y b delante de la columna 'bot'
        # human: how are you \n bot: I am fine
        # Id, Nombre, URL, Ingredientes, Pasos, Pais, Duracion, Porciones, Calorias, Categoria, Contexto, Valoracion y Votos, Comensales, Tiempo, Dificultad
        df['text'] = df.apply(lambda row: 'human: ' + str(row['Nombre']) + '\n bot: Ingredientes ' + str(row['Ingredientes']) + ' Pais ' \
        + str(row['Pais']) + ' Duracion ' + str(row['Duracion']) + ' Categoria ' + str(row['Categoria']) \
        + ' Tiempo ' + str(row['Tiempo']) + ' Dificultad ' + str(row['Dificultad']) + ' Preparacion ' + str(row['Pasos']), axis=1)

        # Eliminar todas las columnas excepto 'text'
        col_a_eliminar = df.columns.difference(['text'])
        df.drop(col_a_eliminar, axis=1, inplace=True)

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
    nombre_archivo = dir + 'RecetasGratis.csv'
    nombre_archivo_nuevo = dir + 'RecetasGratisSFTTodo.csv'

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
