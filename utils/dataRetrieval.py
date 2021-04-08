import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Funcion que permite la obtención de los casos totales incrementales de la pandemia:
date = '2020-03-30'


# Obtención de casos totales en una región dada una fecha:
def get_Casos_Totales_Region_on_date(date):
    values = pd.read_csv(
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto4/" + date + "-CasosConfirmados-totalRegional.csv",
        index_col='Region')
    return values


# Obtención del fallecimiento etario por fecha:
def get_fallecimiento_etario():
    values = pd.read_csv(
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario_T.csv",
        delimiter=',')
    return values


# Función que entrega los CSV con los datos totales por comuna incrementales
def get_Casos_Totales_comunas_incr():
    values = pd.read_csv(
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19.csv")
    return values


# Cuidado que no está cualquier día:
# función entrega los CSV con las los casos totales por coomuna.
def get_Casos_Totales_comunas(date):
    values = pd.read_csv(
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto2/" + date + "-CasosConfirmados.csv")
    return values


# Obtención de casos totales por región:
def get_Casos_totales_x_region(date):
    values = pd.read_csv(
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto4/" + date + "-CasosConfirmados-totalRegional.csv")
    return values


# Obtención de totales nacionales:
def get_total_nacional():
    values = pd.read_csv(
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv")
    return values


# obtención de incidencia:
def get_incidencia():
    values = pd.read_csv(
        "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto6/bulk/data.csv")
    return values


# obtencion de vacunas:
def get_vacunacion():
    values = pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto76/vacunacion.csv")
    return values