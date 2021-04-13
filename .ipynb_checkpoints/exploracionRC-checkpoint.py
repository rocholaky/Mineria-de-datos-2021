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


def plot_fallecimientos():
    # obtenemos el dataframe de fallecimientos:
    fallecimiento_etario = utils.dataRetrieval.get_fallecimiento_etario()
    # volvemos la columna de fechas el indice
    ts = fallecimiento_etario.set_index(fallecimiento_etario.columns[0])
    # volvemos este valor datetime
    ts.index = pd.to_datetime(ts.index)

    # generamos los plots
    fig, ax = plt.subplots()
    # en el ax ponemos el plot generado con pandas
    ax = ts.plot(ax=ax)

    # Ponemos valores solamente de los meses para que sea legible
    # Definimos que la separación sea por mes
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    # cada mes se define por 4 semanas
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(1),
                                                    interval=1))
    # ladeamos los valores en 45 grados
    plt.xticks(rotation=45)
    # definimos que los valores que salgan con el formato 2021-01
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    # generamos los valores de los labels
    ax.set_title("Muertes por rango etario en función del tiempo")
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Muertes')
    # definimos que tendremos grilla
    ax.grid(True)
    # mostramos el gráfico
    plt.show()


# +
# obtenemos los contagios nacionales:
contagios_nacionales = utils.dataRetrieval.get_total_nacional()

# obtenemos contagios por región:
contagios_comuna = utils.dataRetrieval.get_Casos_Totales_comunas_incr()
# sacamos la columna "Tasa":
contagios_comuna = contagios_comuna.drop('Tasa', axis=1)
# sacamos el código de la columna y obtener casos sumados:
connected_regions = contagios_comuna.drop(["Codigo comuna", "Codigo region"], axis=1).groupby("Region").sum()
# obtenemos la población por region en formato de DataFrame
# donde los indices son Región y la columna es la cantidad de población:
# esto permite hacer divisiones por indice.
R_population = connected_regions["Poblacion"]
# sacamos la población y trasponemos la matriz
connected_regions = connected_regions.drop("Poblacion", axis=1).transpose()

# obtenemos las fechas sin los titulos 'Region', 'Codigo region', 'Comuna', 'Codigo comuna', 'Poblacion'
Dates = list(contagios_comuna)[5:]

# obtenemos densidad de contagiados
connected_regions = connected_regions/R_population
#connected_regions = connected_regions.astype(float)
plot_timeSeries(connected_regions, "Densidad Contagiados proporcional a la población", "Cantidad de Contagios por Región Acumulado")


# +
# Procedemos a obtener los contagios por Región no incrementales:
# generamos dataframe
Contagios_por_dia = pd.DataFrame()
# llenamos dataframe con fechas
for date in Dates:
        try:
            # try to do this
            # obtenemos el data Frame de los casos totales por region en la fecha date
            df_date = utils.dataRetrieval.get_Casos_totales_x_region(date)
            # obtenemos las columnas
            colum_value = list(df_date.columns.values)

            #debido a la poca rigurosidad del dataset es necesario ponernos en distintos casos.
            if " Casos nuevos" in colum_value:
                key_contagiados = " Casos nuevos"
            elif "Casos  nuevos" in colum_value:
                key_contagiados = "Casos  nuevos"
            elif "Casos  nuevos  totales" in colum_value:
                key_contagiados= "Casos  nuevos  totales"
            elif 'Casos nuevos totales' in colum_value:
                key_contagiados = "Casos nuevos totales"
            else:
                key_contagiados = "Casos nuevos"

            # obtenemos los contagiados sin el último valor
            column_contagiados = df_date[key_contagiados].values[:-1]
            # existen casos donde hay más valores pero estos no nos interesan por lo que tomamos
            # solamente los 16 primeros que son las regiones
            if len(column_contagiados>16):
                # obtenemos las regiones
                column_contagiados = column_contagiados[:16]
            # lo agregamos como columna al data frame
            Contagios_por_dia[date] = column_contagiados
        except:
            # if error do this
            pass

#agregamos los indices de las regiones
Contagios_por_dia.index = df_date["Region"].values[:16]
# dividimos por la población para obtener la densidad poblacional en porcentage
densidad_contagios_x_dia = Contagios_por_dia.div(R_population, axis=0).transpose()*100
# Trasponemos los datos.
Contagios_por_dia = Contagios_por_dia.transpose()

plot_timeSeries(densidad_contagios_x_dia, "Porcentage de la población contagiada", "Contagios por día")
plot_timeSeries(Contagios_por_dia, "Cantidad contagios", "Contagios por día")
plot_fallecimientos()



# +
###### vacunaciones ##########################################
# obtenemos los datos de las vacunas
vac_x_comuna = utils.dataRetrieval.get_vacunacion()
# eliminamos los valores totales:
vac_x_comuna.drop(vac_x_comuna[vac_x_comuna["Region"] == "Total"].index, inplace=True)
# dividimos en primera y segunda dosis:
vac_x_comuna_d1 = vac_x_comuna[vac_x_comuna["Dosis"] == 'Primera']
# eliminamos la columna dosis al ya tenerlas separadas por dosis
del vac_x_comuna_d1["Dosis"]
# obtenemos los valores de las dosis 2:
vac_x_comuna_d2 = vac_x_comuna[vac_x_comuna["Dosis"] == 'Segunda']
# eliminamos la columna dosis
del vac_x_comuna_d2["Dosis"]
# seteamos los índices para que sean las regiones:
vac_x_comuna_d1.set_index("Region", inplace=True)
vac_x_comuna_d2.set_index("Region", inplace=True)
# dividimos por la población de la región para así poder obtener la densidad poblacional.
vac_x_comuna_d1 = vac_x_comuna_d1.div(R_population, axis=0)
vac_x_comuna_d2 = vac_x_comuna_d2.div(R_population, axis=0)
# trasponemos ambas para que queden como time series
vac_x_comuna_d1 = vac_x_comuna_d1.transpose()
vac_x_comuna_d2 = vac_x_comuna_d2.transpose()

# ploteamos:
plot_timeSeries(vac_x_comuna_d1, "Cantidad Vacunas", "Vacunas primera dosis en función del tiempo")
plot_timeSeries(vac_x_comuna_d2, "Cantidad Vacunas", "Vacunas segunda dosis en función del tiempo")


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
