# -*- coding: utf-8 -*-
import utils.dataRetrieval
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.dates as mdates
from datetime import datetime
from utils.util_plot import plot_timeSeries
import datetime
import seaborn as sns

NORTE = ['Arica y Parinacota', 'Tarapacá', 'Antofagasta', 'Atacama',
                'Coquimbo', 'Valparaíso']

CENTRO = ['Metropolitana', 'O’Higgins', 'Maule', 'Ñuble']

SUR = ['Biobío', 'Araucanía', 'Los Ríos', 'Los Lagos', 'Aysén', 'Magallanes']

nombres_regiones = NORTE + CENTRO + SUR

REGION_INDEX = {}
val = 0
for x in nombres_regiones:
    REGION_INDEX[x] = val
    val += 1

REGION_TO_POS = {
    'Tarapacá': 0,
    'Antofagasta': 0,
    'Atacama': 0,
    'Coquimbo': 0,
    'Valparaíso': 0,
    'O’Higgins': 1,
    'Maule': 1,
    'Biobío': 2,
    'Araucanía': 2,
    'Los Lagos': 2,
    'Aysén': 2,
    'Magallanes': 2,
    'Metropolitana': 1,
    'Los Ríos': 2,
    'Arica y Parinacota': 0,
    'Ñuble': 1
}


REGION_TO_NUMBER = {
    'Tarapacá': 1,
    'Antofagasta': 2,
    'Atacama': 3,
    'Coquimbo': 4,
    'Valparaíso': 5,
    'O’Higgins': 6,
    'Maule': 7,
    'Biobío': 8,
    'Araucanía': 9,
    'Los Lagos': 10,
    'Aysén': 11,
    'Magallanes': 12,
    'Metropolitana': 13,
    'Los Ríos': 14,
    'Arica y Parinacota': 15,
    'Ñuble': 16
}

NUMBER_TO_REGION = {
    1: 'Tarapacá',
    2: 'Antofagasta',
    3: 'Atacama',
    4: 'Coquimbo',
    5: 'Valparaíso',
    6: 'O’Higgins',
    7: 'Maule',
    8: 'Biobío',
    9: 'Araucanía',
    10: 'Los Lagos',
    11: 'Aysén',
    12: 'Magallanes',
    13: 'Metropolitana',
    14: 'Los Ríos',
    15: 'Arica y Parinacota',
    16: 'Ñuble'
}


def get_transporte_aereo():
    """Entrega 6 dataframes, los primeros 3 corresponden a norte-centro-sur y son orígenes, los otros 3 corresponden a norte-centro-sur y son destinos.

    """
    viajes = utils.dataRetrieval.get_transporte_aereo()

    # Columnas despreciables
    columnas_inutiles = [
        "Cod_region_destino",
        "Destino",
        "Origen",
        "Cod_region_origen",
        "Fin_semana",
        "Operaciones",
        "Semana"
    ]

    # Agrupar datos por fecha y región, eliminar columnas inútiles
    viajes_origen = viajes.drop(columnas_inutiles + [
        "Region_destino"
    ], axis = 1).groupby([
        "Inicio_semana",
        "Region_origen"
    ]).sum()

    viajes_destino = viajes.drop(columnas_inutiles + [
        "Region_origen"
    ], axis = 1).groupby([
        "Inicio_semana",
        "Region_destino"
    ]).sum()


    # Contendrán los datos de cada destino/rogien
    new_data_norte_origen = []
    new_data_centro_origen = []
    new_data_sur_origen = []
    new_data_norte_destino = []
    new_data_centro_destino = []
    new_data_sur_destino = []


    # Obtener nuevas tablas
    # Deja las fechas en primera columna y las regiones en las columnas restantes
    # [i, j] es región j en fecha i. Para origenes.
    last = ["2020-0-0", "2020-0-0", "2020-0-0"]
    for index, row in viajes_origen.iterrows():
        fecha = row.name[0]

        if (REGION_INDEX[row.name[1]] < 6):
            if (row.name[0] != last[0]):
                new_data_norte_origen += [[0]*(len(NORTE) + 1)]
                new_data_norte_origen[-1][0] = row.name[0]
                last[0] = row.name[0]
            new_data_norte_origen[-1][1 + REGION_INDEX[row.name[1]]] += row.Pasajeros
        elif (REGION_INDEX[row.name[1]] < 10):
            if (row.name[0] != last[1]):
                new_data_centro_origen += [[0]*(len(CENTRO) + 1)]
                new_data_centro_origen[-1][0] = row.name[0]
                last[1] = row.name[0]
            new_data_centro_origen[-1][1 + REGION_INDEX[row.name[1]] - 6] += row.Pasajeros
        else:
            if (row.name[0] != last[2]):
                new_data_sur_origen += [[0]*(len(SUR) + 1)]
                new_data_sur_origen[-1][0] = row.name[0]
                last[2] = row.name[0]
            new_data_sur_origen[-1][1 + REGION_INDEX[row.name[1]] - 10] += row.Pasajeros


    # Obtener nuevas tablas
    # Deja las fechas en primera columna y las regiones en las columnas restantes
    # [i, j] es región j en fecha i. Para destinos.
    last = ["2020-0-0", "2020-0-0", "2020-0-0"]
    for index, row in viajes_destino.iterrows():
        if (REGION_INDEX[row.name[1]] < 6):
            if (row.name[0] != last[0]):
                new_data_norte_destino += [[0]*(len(NORTE) + 1)]
                new_data_norte_destino[-1][0] = row.name[0]
                last[0] = row.name[0]
            new_data_norte_destino[-1][1 + REGION_INDEX[row.name[1]]] += row.Pasajeros
        elif (REGION_INDEX[row.name[1]] < 10):
            if (row.name[0] != last[1]):
                new_data_centro_destino += [[0]*(len(CENTRO) + 1)]
                new_data_centro_destino[-1][0] = row.name[0]
                last[1] = row.name[0]
            new_data_centro_destino[-1][1 + REGION_INDEX[row.name[1]] - 6] += row.Pasajeros
        else:
            if (row.name[0] != last[2]):
                new_data_sur_destino += [[0]*(len(SUR) + 1)]
                new_data_sur_destino[-1][0] = row.name[0]
                last[2] = row.name[0]
            new_data_sur_destino[-1][1 + REGION_INDEX[row.name[1]] - 10] += row.Pasajeros
    
    # Convertir a DataFrame
    data_norte_origen = pd.DataFrame(new_data_norte_origen, columns = ['Inicio'] + NORTE)
    data_norte_origen = data_norte_origen.set_index('Inicio')
    data_norte_origen.index = pd.to_datetime(data_norte_origen.index)
    data_norte_origen = data_norte_origen.resample('W').sum()
    
    data_centro_origen = pd.DataFrame(new_data_centro_origen, columns = ['Inicio'] + CENTRO)
    data_centro_origen = data_centro_origen.set_index('Inicio')
    data_centro_origen.index = pd.to_datetime(data_centro_origen.index)
    data_centro_origen = data_centro_origen.resample('W').sum()

    data_sur_origen = pd.DataFrame(new_data_sur_origen, columns = ['Inicio'] + SUR)
    data_sur_origen = data_sur_origen.set_index('Inicio')
    data_sur_origen.index = pd.to_datetime(data_sur_origen.index)
    data_sur_origen = data_sur_origen.resample('W').sum()

    data_norte_destino = pd.DataFrame(new_data_norte_destino, columns = ['Inicio'] + NORTE)
    data_norte_destino = data_norte_destino.set_index('Inicio')
    data_norte_destino.index = pd.to_datetime(data_norte_destino.index)
    data_norte_destino = data_norte_destino.resample('W').sum()

    data_centro_destino = pd.DataFrame(new_data_centro_destino, columns = ['Inicio'] + CENTRO)
    data_centro_destino = data_centro_destino.set_index('Inicio')
    data_centro_destino.index = pd.to_datetime(data_centro_destino.index)
    data_centro_destino = data_centro_destino.resample('W').sum()

    data_sur_destino = pd.DataFrame(new_data_sur_destino, columns = ['Inicio'] + SUR)
    data_sur_destino = data_sur_destino.set_index('Inicio')
    data_sur_destino.index = pd.to_datetime(data_sur_destino.index)
    data_sur_destino = data_sur_destino.resample('W').sum()

    # Retornar lo pedido
    return [
        data_norte_origen, 
        data_centro_origen,
        data_sur_origen,
        data_norte_destino,
        data_centro_destino,
        data_sur_destino
    ]

def get_movilidad_data_frames_por_comuna():
    """Entrega una lista de 17 DataFrames, el primero está vacío y los siguientes corresponden a la información por región indexada desde 1 a 16.
    
    """

    # Sacamos el dataset
    movilidad = utils.dataRetrieval.get_movilidad_por_comuna()

    ## Estructuras de datos para la generación de las tablas

    # Indica de qué region es una comuna 
    # (string:string)
    comuna_es_de_region = {}

    # Indica qué comunas tiene cada región, empezamos cada región con una lista vacía
    # (string:lista<string>)
    comunas_en_regiones = {}
    for x in nombres_regiones:
        comunas_en_regiones[x] = []

    
    # Estas no importan en el futuro
    nombres_comunas_aux = movilidad[0].nom_comuna.unique()

    comuna_encontrada = [0] * len(nombres_comunas_aux)


    # Nombre de las comunas
    nombres_comunas = []
    for x in nombres_comunas_aux:
        nombres_comunas += [x]
    nombres_comunas.sort()

    # guarda indices asociados a comunas
    INDEX_COMUNA = {}
    for i in range(0, len(nombres_comunas)):
        INDEX_COMUNA[nombres_comunas[i]] = i

    columnas_inutiles_comunas = [
        'comuna',
        'fecha_termino',
        'semana'
    ]

    comunas = movilidad[0].drop(columnas_inutiles_comunas, axis = 1)

    aux = comunas.groupby(['fecha_inicio', 'nom_comuna']).sum()


    # Lista de datos por región.
    comunas_data_por_region = [
        [], [], [], [],
        [], [], [], [],
        [], [], [], [],
        [], [], [], [],
        []
    ]

    # Guarda la posición en la que está una comuna en la lista de su región respectiva.
    comunas_indice_de_region = {}

    for index, row in aux.iterrows():
        if (comuna_encontrada[INDEX_COMUNA[row.name[1]]] == 0):
            region = NUMBER_TO_REGION[row.region]
            comuna = row.name[1]
            comuna_idx = INDEX_COMUNA[comuna]
            comuna_encontrada[comuna_idx] = 1
            comuna_es_de_region[comuna] = region
            comunas_en_regiones[region] += [comuna]
            comunas_indice_de_region[comuna] = len(comunas_en_regiones[region]) - 1
    

    # Guardar los datos de movilidad, [i, j] es fecha i, comuna j
    last = ["2020-0-0"] * 16

    for index, row in aux.iterrows():
        region = NUMBER_TO_REGION[row.region]
        comuna = row.name[1]
        region_id = int(round(row.region))
        if (row.region - region_id > 0.5):
            region_id += 1
        if (last[region_id - 1] != row.name[0]):
            comunas_data_por_region[region_id] += [[0]*(len(comunas_en_regiones[region]) + 1)]
            comunas_data_por_region[region_id][-1][0] = row.name[0]
            last[region_id - 1] = row.name[0]
        indice = comunas_indice_de_region[comuna]
        comunas_data_por_region[region_id][-1][1 + indice] = row.var_salidas
    data_frames_por_region = []
    for i in range(16):
        data_frames_por_region += [pd.DataFrame(comunas_data_por_region[i + 1], columns = ['Inicio'] + comunas_en_regiones[NUMBER_TO_REGION[i + 1]])]
        data_frames_por_region[-1] = data_frames_por_region[-1].set_index('Inicio')
        #print(NUMBER_TO_REGION[i + 1] + ": ---------------------------------------")
        #print(data_frames_por_region[-1])

    return data_frames_por_region

def get_estados_por_region():
    """Entrega una lista de 17 DataFrames, el primero está vacío y los siguientes corresponden a la información por región indexada desde 1 a 16.
    
    """

    # Sacamos el dataset
    movilidad = utils.dataRetrieval.get_movilidad_por_comuna()

    ## Estructuras de datos para la generación de las tablas

    # Indica de qué region es una comuna 
    # (string:string)
    comuna_es_de_region = {}

    # Indica qué comunas tiene cada región, empezamos cada región con una lista vacía
    # (string:lista<string>)
    comunas_en_regiones = {}
    for x in nombres_regiones:
        comunas_en_regiones[x] = []

    
    # Estas no importan en el futuro
    nombres_comunas_aux = movilidad[0].nom_comuna.unique()

    comuna_encontrada = [0] * len(nombres_comunas_aux)


    # Nombre de las comunas
    nombres_comunas = []
    for x in nombres_comunas_aux:
        nombres_comunas += [x]
    nombres_comunas.sort()

    # guarda indices asociados a comunas
    INDEX_COMUNA = {}
    for i in range(0, len(nombres_comunas)):
        INDEX_COMUNA[nombres_comunas[i]] = i

    columnas_inutiles_comunas = [
        'comuna',
        'fecha_termino',
        'semana'
    ]

    comunas = movilidad[0].drop(columnas_inutiles_comunas, axis = 1)

    aux = comunas.groupby(['fecha_inicio', 'nom_comuna']).sum()

    # Lista de datos por región.
    comunas_data_por_region = [
        [], [], [], [],
        [], [], [], [],
        [], [], [], [],
        [], [], [], [],
        []
    ]

    # Guarda la posición en la que está una comuna en la lista de su región respectiva.
    comunas_indice_de_region = {}

    for index, row in aux.iterrows():
        if (comuna_encontrada[INDEX_COMUNA[row.name[1]]] == 0):
            region = NUMBER_TO_REGION[row.region]
            comuna = row.name[1]
            comuna_idx = INDEX_COMUNA[comuna]
            comuna_encontrada[comuna_idx] = 1
            comuna_es_de_region[comuna] = region
            comunas_en_regiones[region] += [comuna]
            comunas_indice_de_region[comuna] = len(comunas_en_regiones[region]) - 1
    
    # Guardar los datos de fases en comunas, [i, j] es fecha i, comuna j
    last = ["2020-0-0"] * 16

    for index, row in aux.iterrows():
        region = NUMBER_TO_REGION[row.region]
        comuna = row.name[1]
        region_id = round(int(row.region))
        if (row.name[0] != last[region_id - 1]):
            comunas_data_por_region[region_id] += [[0]*(len(comunas_en_regiones[region]) + 1)]
            comunas_data_por_region[region_id][-1][0] = row.name[0]
            last[region_id - 1] = row.name[0]
        indice = comunas_indice_de_region[comuna]
        comunas_data_por_region[region_id][-1][1 + indice] = row.paso
    data_frames_por_region = []
    for i in range(16):
        data_frames_por_region += [pd.DataFrame(comunas_data_por_region[i + 1], columns = ['Inicio'] + comunas_en_regiones[NUMBER_TO_REGION[i + 1]])]
        data_frames_por_region[-1] = data_frames_por_region[-1].set_index('Inicio')
        data_frames_por_region[-1] = data_frames_por_region[-1].groupby(['Inicio']).sum()
        #print(NUMBER_TO_REGION[i + 1] + ": ---------------------------------------")
        #print(data_frames_por_region[-1])

    return data_frames_por_region


#data_frames_por_region = get_movilidad_data_frames_por_comuna()

#plot_df(data_frames_por_region[0], "movilidad en " + NUMBER_TO_REGION[1], "Movilidad", legend = False)


