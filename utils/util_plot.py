import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# fución que plotea series de tiempo, es necesario que la
# serie de tiempo esté tenga indices de las fechas.
def plot_timeSeries(ts, ylabel, title,fig_size=(7, 6)):
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