# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import seaborn as sns
# fución que plotea series de tiempo, es necesario que la
# serie de tiempo esté tenga indices de las fechas.
def plot_timeSeries(ts, ylabel, title, fig_size=(7, 6)):
    # volvemos este valor datetime
    ts.index = pd.to_datetime(ts.index)
    # generamos los plots
    fig, ax = plt.subplots(figsize=fig_size)
    # seteamos los colores:
    ax.set_prop_cycle('color', plt.cm.Spectral(np.linspace(0, 1, len(ts.columns))))
    # en el ax ponemos el plot generado con pandas
    ax = ts.plot(ax=ax)
    # seteamos el color en gris
    ax.set_facecolor('#808080')

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
    ax.set_title(title)
    ax.set_xlabel('Fecha')
    ax.set_ylabel(ylabel)
    # definimos que tendremos grilla
    ax.grid(True)
    # mostramos el gráfico
    plt.show()


# fución que plotea series de tiempo en barplot, es necesario que la
# serie de tiempo esté tenga indices de las fechas.
def barplot_timeSeries(ts, ylabel, title,fig_size=(7, 6), tick=True, stacked = False):
    # generamos los plots
    fig, ax = plt.subplots(figsize=fig_size)
    # seteamos los colores:
    ax.set_prop_cycle('color', plt.cm.Spectral(np.linspace(0, 1, len(ts.columns))))
    # en el ax ponemos el plot generado con pandas
    ax = ts.plot(kind="bar",  ax=ax, stacked=stacked)
    # seteamos el color en gris
    ax.set_facecolor('#808080')

    if tick:
        # Ponemos valores solamente de los meses para que sea legible
        # Definimos que la separación sea por mes
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        # cada mes se define por 4 semanas
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=(1),
                                                         interval=1))
        # definimos que los valores que salgan con el formato 2021-01
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    else:
        ax.xaxis.set_major_formatter(ticker.FixedFormatter(ts.index))
    # ladeamos los valores en 45 grados
    plt.xticks(rotation=45)
    # generamos los valores de los labels
    ax.set_title(title)
    ax.set_xlabel('Fecha')
    ax.set_ylabel(ylabel)
    # definimos que tendremos grilla
    ax.grid(True)
    # mostramos el gráfico
    plt.show()

#Graficar calidad del aire
def plot_df(df, title, ylabel, xlabel = 'Fecha',  size = (20,9), legend = True):
    '''Grafica serie de tiempo de la calidad del aire'''
    fig, ax = plt.subplots(figsize=size)
    ax.set_prop_cycle('color', plt.cm.Spectral(np.linspace(0, 1, len(df.columns))))
        # en el ax ponemos el plot generado con pandas
    ax = df.plot(ax=ax)
    ax.set_facecolor('#808080')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    
    if legend:
        legend  = plt.legend(bbox_to_anchor=(1.01, 0.97), loc='upper left')
        legend.get_frame().set_facecolor('#808080')
        
    plt.tight_layout()
    plt.show()
    plt.close()
    return

def box_plot_df(df, title, xlabel, ylabel,size = (20,10)):
    '''Grafica boxplot serie de tiempo de la calidad del aire'''
    fig, ax = plt.subplots(figsize=size)
    fig.suptitle(title, fontsize=14, fontweight='bold')
    ax = df.boxplot()
    # ladeamos los valores en 45 grados
    plt.xticks(rotation=90)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    plt.close()
    return

def corr_plot_df(df, title):
    # covarianza
    corr = df.corr()
    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.title(title)
    plt.show()
    plt.close()
    return
