# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 19:44:54 2024

@author: Usuario
"""

import pandas as pd
import numpy as np
import datetime as dt

# Función para cargar y concatenar los datos de varios archivos CSV
def cargar_datos(archivos):
    dataframes = [pd.read_csv(archivo, sep=';') for archivo in archivos]
    return pd.concat(dataframes)

# Función para filtrar y reestructurar el DataFrame
def procesar_datos(emisiones):
    columnas_principales = ['ESTACION', 'MAGNITUD', 'ANO', 'MES']
    columnas_dias = [col for col in emisiones if col.startswith('D')]
    columnas = columnas_principales + columnas_dias
    
    # Filtrar las columnas
    emisiones = emisiones[columnas]
    
    # Reestructurar usando melt
    emisiones = emisiones.melt(id_vars=columnas_principales, var_name='DIA', value_name='VALOR')
    
    # Crear columna de fecha
    emisiones['DIA'] = emisiones['DIA'].str.strip('D')
    emisiones['FECHA'] = pd.to_datetime(emisiones['ANO'].astype(str) + '/' + emisiones['MES'].astype(str) + '/' + emisiones['DIA'], 
                                        format='%Y/%m/%d', errors='coerce')
    
    # Eliminar fechas inválidas
    emisiones = emisiones.dropna(subset=['FECHA'])
    
    # Ordenar por estación, magnitud y fecha
    emisiones = emisiones.sort_values(by=['ESTACION', 'MAGNITUD', 'FECHA'])
    
    return emisiones

# Función para mostrar las estaciones y contaminantes disponibles
def mostrar_informacion(emisiones):
    print('Estaciones disponibles:', emisiones['ESTACION'].unique())
    print('Contaminantes disponibles:', emisiones['MAGNITUD'].unique())

# Función para obtener la evolución de un contaminante en una estación durante un periodo
def evolucion(emisiones, estacion, contaminante, desde, hasta):
    desde = pd.to_datetime(desde)
    hasta = pd.to_datetime(hasta)
    
    return emisiones[(emisiones['ESTACION'] == estacion) & 
                     (emisiones['MAGNITUD'] == contaminante) & 
                     (emisiones['FECHA'] >= desde) & 
                     (emisiones['FECHA'] <= hasta)].sort_values('FECHA')['VALOR']

# Función para obtener un resumen descriptivo por contaminante
def resumen_por_contaminante(emisiones):
    return emisiones.groupby('MAGNITUD')['VALOR'].describe()

# Función para obtener un resumen descriptivo por contaminante y estación
def resumen_por_estacion_y_contaminante(emisiones):
    return emisiones.groupby(['ESTACION', 'MAGNITUD'])['VALOR'].describe()

# Función para obtener el resumen descriptivo de una estación y un contaminante específico
def resumen_individual(emisiones, estacion, contaminante):
    return emisiones[(emisiones['ESTACION'] == estacion) & 
                     (emisiones['MAGNITUD'] == contaminante)]['VALOR'].describe()

# Función para obtener la evolución mensual de un contaminante en un año
def evolucion_mensual(emisiones, contaminante, ano):
    return emisiones[(emisiones['MAGNITUD'] == contaminante) & (emisiones['ANO'] == ano)]\
                    .groupby(['ESTACION', 'MES'])['VALOR'].mean().unstack('MES')

# Función para obtener la evolución mensual de una estación en un año
def evolucion_mensual_estacion(emisiones, estacion, ano):
    return emisiones[(emisiones['ESTACION'] == estacion) & (emisiones['ANO'] == ano)]\
                    .groupby(['MAGNITUD', 'MES'])['VALOR'].mean().unstack('MES')

# Ejecución del flujo principal
if __name__ == '__main__':
    archivos = ['emisiones-2016.csv', 'emisiones-2017.csv', 'emisiones-2018.csv', 'emisiones-2019.csv']
    
    emisiones = cargar_datos(archivos)
    emisiones = procesar_datos(emisiones)
    
    mostrar_informacion(emisiones)
    
    # Ejemplo de uso de las funciones
    print('Evolución:', evolucion(emisiones, 56, 8, '2018/10/25', '2019/02/12'))
    
    print('Resumen por contaminante:', resumen_por_contaminante(emisiones))
    print('Resumen por estación y contaminante:', resumen_por_estacion_y_contaminante(emisiones))
    
    print('Resumen de Dióxido de Nitrógeno en Plaza Elíptica:', resumen_individual(emisiones, 56, 8))
    
    print('Evolución mensual de dióxido de nitrógeno en 2019:', evolucion_mensual(emisiones, 8, 2019))
    print('Evolución mensual de la estación 4 en 2019:', evolucion_mensual_estacion(emisiones, 4, 2019))
