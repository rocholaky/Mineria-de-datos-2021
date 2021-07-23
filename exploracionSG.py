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
####### Caldiad del aire ############################
def calidad_del_aire(mp, anio, intervalo = '2W-SAT'):
    '''Extrae y filtra datos de calidad de aire en MP hasta 2020'''
    MP = utils.dataRetrieval.get_MP(str(mp),str(anio))
    indices = MP['Nombre de estacion']
    MP = MP.drop(['Nombre de estacion', 'Talagante'], axis=1) #No habia suficiente información
    MP.index = indices
    MP = MP.transpose()
    MP = MP.drop(['Codigo region','Region' ,'Comuna','Codigo comuna','UTM_Este','UTM_Norte'], axis=1)
    MP = MP.transpose()
    MP.index = pd.to_datetime(list(MP.index.values))
    MP = MP.astype(float)
    MP = MP.resample( intervalo, closed='left', label='left' ).sum()
    MP.transpose()
    return MP

def calidad_del_aire_nuevo_formato(mp, anio =2021, intervalo = '2W-SAT'):
    '''Extrae y filtra datos de calidad de aire en MP desde esl 2021'''
    MP = utils.dataRetrieval.get_MP(str(mp),str(anio))
    indices = MP['Nombre de estacion']
    MP = MP.drop(['Nombre de estacion','Talagante'], axis=1) #Talagante no tenia información en 2021
    MP.index = indices
    MP.index = pd.to_datetime(list(MP.index.values))
    MP = MP.astype(float)
    MP = MP.resample(intervalo, closed='left', label='left' ).sum()
    return MP


# -

#MP 10 2019-2020-2021
# MP = pd.concat([calidad_del_aire(10, 2019),calidad_del_aire(10, 2020)], axis=0)
# MP = pd.concat([MP,calidad_del_aire_nuevo_formato(10,2021)], axis=0)
# estacion_sin_lectura = MP.columns[MP.isna().any()].tolist()
# MP = MP.drop(estacion_sin_lectura, axis = 1)
# plot_df(MP, 'Cantidad de MP10 por estacion en funcion del tiempo', 'Cantidad de MP10')
# box_plot_df(MP)

# #MP 2.5 2019-2020-2021
# MP = pd.concat([calidad_del_aire(2.5, 2019),calidad_del_aire(2.5, 2020)], axis=0)
# MP = pd.concat([MP,calidad_del_aire_nuevo_formato(2.5,2021)], axis=0)
# estacion_sin_lectura = MP.columns[MP.isna().any()].tolist()
# MP = MP.drop(estacion_sin_lectura, axis = 1)
# plot_df(MP, 'Cantidad de MP 2.5 por estacion en funcion del tiempo', 'Cantidad de MP 2.5')
# box_plot_df(MP)

# ###### Data Product 36 - Residencias Sanitarias:#################################
# rs_x_reg = utils.dataRetrieval.get_residencias()
# # eliminamos los cupos totales y residencias:
# rs_x_reg.drop(rs_x_reg[rs_x_reg["Categoria"] == "cupos totales"].index, inplace=True)
# rs_x_reg.drop(rs_x_reg[rs_x_reg["Categoria"] == "residencias"].index, inplace=True)
# #eliminamos la columna categoria
# del rs_x_reg["Categoria"]
# #seteamos los indices para que sean las regiones
# rs_x_reg.set_index("Region", inplace=True)
# #transponemos el dataframe
# rs_x_reg=rs_x_reg.transpose()
# #plot_timeSeries(rs_x_reg, "Numero de personas en residencias sanitarias", "Numero de personas en residencias en función del tiempo")
# plot_df(rs_x_reg, "Numero de personas en residencias en función del tiempo", "Numero de personas en residencias sanitarias")
# box_plot_df(rs_x_reg)
# ####Densidad de residencias sanitarias (rel poblacion regional) -> contagios

# ######### Nacimientos #################################
# nac_x_reg1 = utils.dataRetrieval.get_nacimientos2020()
# nac_x_reg2 = utils.dataRetrieval.get_nacimientos2021()
# #print(nacimientos_x_region1)
# nac_x_reg1 = nac_x_reg1.drop(["Codigo comuna","Codigo region"], axis=1).groupby("Region").sum().transpose()
# nac_x_reg2 = nac_x_reg2.drop(["Codigo comuna","Codigo region"], axis=1).groupby("Region").sum().transpose()
# nac_x_reg = pd.concat([nac_x_reg1,nac_x_reg2], axis=0)
# # # volvemos los indices a datetime
# nac_x_reg.index = pd.to_datetime(list(nac_x_reg.index.values))
# #Agrupamos por mes
# nac_x_reg=nac_x_reg.resample('M').sum()
# #Sacamos el último mes, porque aun no estan completos los datos
# nac_x_reg = nac_x_reg.head(-1)
# #Ploteaos la serie de tiempo
# #plot_timeSeries(nac_x_reg, "Nacidos por region ", "Nacidos por region en funcion del tiempo", (20,9))
# plot_df(nac_x_reg, "Nacidos por region en funcion del tiempo", "Nacidos por region" , legend = False)
# box_plot_df(nac_x_reg)

def get_product76_segunda_dosis_nacional():
    values = pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto76/vacunacion.csv")
    return values
Vacunas = get_product76_segunda_dosis_nacional()
Vacunas = Vacunas.head(3).transpose().drop("Region")
new_header = Vacunas.iloc[0] #grab the first row for the header
Vacunas = Vacunas[1:] #take the data less the header row
Vacunas.columns = new_header #set the header row as the df header
Vacunas.rename(columns=Vacunas.iloc[0])
Vacunas.index = pd.to_datetime(Vacunas.index)
# print(Vacunas)

def get_product49_pcr_nacional():
    values = pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto49/Positividad_Diaria_Media_T.csv")
    return values
PCR = get_product49_pcr_nacional()
PCR = PCR[["Fecha", "pcr"]]
PCR = PCR.set_index(PCR["Fecha"]).drop(["Fecha"],1)
PCR.index = pd.to_datetime(PCR.index)
# print(PCR)