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


def get_product76_vacuna_dosis_nacional():
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