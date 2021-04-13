# -*- coding: utf-8 -*-
import utils.dataRetrieval
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from utils.util_plot import plot_timeSeries
import datetime
import seaborn as sns

# +
###### Data Product 36 - Residencias Sanitarias:#################################
residencias_x_region = utils.dataRetrieval.get_residencias()
# eliminamos los cupos totales y residencias:
residencias_x_region.drop(residencias_x_region[residencias_x_region["Categoria"] == "cupos totales"].index, inplace=True)
residencias_x_region.drop(residencias_x_region[residencias_x_region["Categoria"] == "residencias"].index, inplace=True)
#eliminamos la columna categoria
del residencias_x_region["Categoria"]
#seteamos los indices para que sean las regiones
residencias_x_region.set_index("Region", inplace=True)
#transponemos el dataframe
residencias_x_region=residencias_x_region.transpose()
plot_timeSeries(residencias_x_region, "Numero de personas en residencias sanitarias", "Numero de personas en residencias en función del tiempo")

####Densidad de residencias sanitarias (rel poblacion regional) -> contagios
# -

######### Nacimientos #################################
nacimientos_x_region1 = utils.dataRetrieval.get_nacimientos2020()
nacimientos_x_region2 = utils.dataRetrieval.get_nacimientos2021()
#print(nacimientos_x_region1)
nacimientos_x_region1 = nacimientos_x_region1.drop(["Codigo comuna","Codigo region"], axis=1).groupby("Region").sum()
nacimientos_x_region2 = nacimientos_x_region2.drop(["Codigo comuna","Codigo region"], axis=1).groupby("Region").sum()
nacimientos_x_region1 = nacimientos_x_region1.transpose()
nacimientos_x_region2 = nacimientos_x_region2.transpose()
nacimientos_x_region = pd.concat([nacimientos_x_region1,nacimientos_x_region2], axis=0)
# # volvemos los indices a datetime
nacimientos_x_region.index = pd.to_datetime(list(nacimientos_x_region.index.values))
#Agrupamos por mes
nacimientos_x_region=nacimientos_x_region.resample('M').sum()
#Sacamos el último mes, porque aun no estan completos los datos
nacimientos_x_region = nacimientos_x_region.head(-1)
#Ploteaos la serie de tiempo
plot_timeSeries(nacimientos_x_region, "Nacidos por region ", "Nacidos por region en funcion del tiempo")


# +
####### Caldiad del aire ############################
def filtrar(mp, anio):
    MP = utils.dataRetrieval.get_MP(str(mp),str(anio))
    indices = MP['Nombre de estacion']
    MP = MP.drop('Nombre de estacion', axis=1)
    MP.index = indices
    MP = MP.transpose()
    MP = MP.drop(['Codigo region','Region' ,'Comuna','Codigo comuna','UTM_Este','UTM_Norte'], axis=1)
    MP = MP.transpose()
    MP.index = pd.to_datetime(list(MP.index.values))
    MP = MP.astype(float)
    MP = MP.resample( '2W-SAT', closed='left', label='left' ).sum()
    MP.transpose()
    return MP

anios = [2019,2020,2021]

# -

#MP 10 2019-2020-2021
mp = 10
MP = pd.concat([filtrar(10, anios[0]),filtrar(10, anios[1])], axis=0)
MP_10_2021 = utils.dataRetrieval.get_MP(str(mp),str(anios[2]))
print(MP_10_2021)
indices = MP_10_2021['Nombre de estacion']
MP_10_2021 = MP_10_2021.drop('Nombre de estacion', axis=1)
MP_10_2021.index = indices
MP_10_2021.index = pd.to_datetime(list(MP_10_2021.index.values))
MP_10_2021 = MP_10_2021.astype(float)
MP_10_2021 = MP_10_2021.resample( '2W-SAT', closed='left', label='left' ).sum()
MP = pd.concat([MP,MP_10_2021], axis=0)
MP.describe()

#Datos faltantes talagante, y otras
MP_10_2021 = utils.dataRetrieval.get_MP(str(mp),str(anios[2]))
MP_10_2021['Talagante']

#Graficar calidad del aire
fig, ax = plt.subplots(figsize=(14,14))
ax.set_prop_cycle('color', plt.cm.Spectral(np.linspace(0, 1, len(MP.columns))))
    # en el ax ponemos el plot generado con pandas
ax = MP.plot(ax=ax)
ax.set_facecolor('#808080')
ax.set_title('Cantidad de MP10 en el aire en funcion del tiempo')
ax.set_xlabel('Fecha')
ax.set_ylabel('Cantidad de MP10 en el aire')
ax.grid(True)

# +
#MP 2.5 2019-2020-2021
mp = 2.5
MP2 = pd.concat([filtrar(mp, anios[0]),filtrar(mp, anios[1])], axis=0)
MP_25_2021 = utils.dataRetrieval.get_MP(str(mp),str(anios[2]))
indices = MP_25_2021['Nombre de estacion']
MP_25_2021 = MP_25_2021.drop('Nombre de estacion', axis=1)
MP_25_2021.index = indices
MP_25_2021.index = pd.to_datetime(list(MP_25_2021.index.values))
MP_25_2021 = MP_25_2021.astype(float)
MP_25_2021 = MP_25_2021.resample( '2W-SAT', closed='left', label='left' ).sum()
MP2 = pd.concat([MP2,MP_25_2021], axis=0)

#Graficar calidad del aire
fig, ax = plt.subplots(figsize=(14,14))
ax.set_prop_cycle('color', plt.cm.Spectral(np.linspace(0, 1, len(MP2.columns))))
    # en el ax ponemos el plot generado con pandas
ax = MP.plot(ax=ax)
ax.set_facecolor('#808080')
ax.set_title('Cantidad de MP10 en el aire en funcion del tiempo')
ax.set_xlabel('Fecha')
ax.set_ylabel('Cantidad de MP10 en el aire')
ax.grid(True)

MP2.describe()
