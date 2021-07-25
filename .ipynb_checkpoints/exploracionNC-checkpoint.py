import utils.dataRetrieval
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from utils.util_plot import plot_timeSeries, barplot_timeSeries
import matplotlib


activos = pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna.csv", delimiter=',')
activos = activos[activos["Comuna"] == "Total"]
activos  = activos.set_index("Region")
poblacion = activos["Poblacion"]
activos = activos.loc[:, "2020-04-13":]
proporcionalActivos = activos.div(poblacion, axis = 0).transpose()*100000
activos = activos.transpose()


plot_timeSeries(proporcionalActivos, "Evolución de casos activos proporcionales por región", "Casos activos por 100.000 habitantes")
plot_timeSeries(activos, "Evolución de casos activos por región", "Casos activos totales")




asintomaticos = pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto27/CasosNuevosSinSintomas_T.csv", delimiter= ',')
asintomaticos = asintomaticos.loc[: , :"Magallanes"]

plot_timeSeries(asintomaticos, "Evolución de asintomáticos por región", "Casos asintomáticos totales", fig_size=(20,6))