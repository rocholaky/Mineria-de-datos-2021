import pandas as pd
import numpy as np

def get_clases():
    data = pd.read_csv('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales.csv')
    data = data.set_index('Fecha').T
    data['class'] = np.where(data['Casos nuevos con sintomas'] < data['Casos nuevos con sintomas'].shift(-1), 1, 0)
    data = data['class']
    data.drop(data.tail(1).index, inplace=True)
    data = pd.DataFrame(data)
    data.index = pd.to_datetime(data.index)
    return data