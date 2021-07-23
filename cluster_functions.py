import exploracionJO
from sklearn.cluster import KMeans, AgglomerativeClustering
import matplotlib.pyplot as plt
from utils.dataRetrieval import get_Casos_Totales_comunas, get_total_nacional,\
get_Casos_Totales_comunas_incr
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram
from matplotlib.pyplot import figure
import numpy as np
import pandas as pd
from datetime import datetime
# definimos las fechas donde queremos realizar el proceso de cluster:
fecha_inicio = '2021-03-01'
fecha_final = '2021-06-01'


def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)


def getMovilidadDeComunasDeRegion(start = fecha_inicio, end = fecha_final):
    data_por_region = exploracionJO.get_movilidad_data_frames_por_comuna()
    df = []
    for region in range(1, 17):
        df2 = data_por_region[region - 1]
        df2.index = pd.to_datetime(list(df2.index.values))
        df2 = df2[(df2.index >= start) & (df2.index <= end)].transpose()
        df2.index = [value.lower() for value in list(df2.index)]
        
        meanTable = pd.DataFrame(df2.mean(axis = 1))
        stdTable = pd.DataFrame(df2.std(axis = 1))
        meanTable.rename(columns = {0 : 'mean_movilidad'}, inplace = True)
        stdTable.rename(columns = {0 : 'std_movilidad'}, inplace = True)

        df.append(meanTable.join(stdTable))
    df = pd.concat(df)
    return df

def get_datos_nacionales():
    # obtenemos los contagios nacionales:
    contagios_nacionales = get_total_nacional()

    # obtenemos contagios por región:
    contagios_comuna = get_Casos_Totales_comunas_incr()
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
    return R_population, Dates

def get_densidad_contagios(Dates):
    start = fecha_inicio
    end = fecha_final
    # Procedemos a obtener los contagios por Región no incrementales:
    # generamos dataframe
    Contagios_por_dia = pd.DataFrame()
    # llenamos dataframe con fechas
    for date in Dates:
            # try to do this
            # obtenemos el data Frame de los casos totales por region en la fecha date
            df_date = get_Casos_Totales_comunas(date)
            # obtenemos las columnas
            colum_value = list(df_date.columns.values)

            # debido a la poca rigurosidad del dataset es necesario ponernos en distintos casos.
            if "Casos Confirmados" in colum_value:
                key_contagiados = "Casos Confirmados"
            # obtenemos los contagiados sin el último valor
            column_contagiados = df_date[key_contagiados].div(df_date["Poblacion"], axis=0)
            Contagios_por_dia[date] = column_contagiados
    Contagios_por_dia = Contagios_por_dia.transpose()
    Contagios_por_dia.index = pd.to_datetime(Contagios_por_dia.index)
    Contagios_por_dia = Contagios_por_dia[(Contagios_por_dia.index >= start) & (Contagios_por_dia.index <= end)].transpose()
    Contagios_por_dia.set_index(df_date["Comuna"], inplace=True)
    meanTable = pd.DataFrame(Contagios_por_dia.mean(axis = 1))
    stdTable = pd.DataFrame(Contagios_por_dia.std(axis = 1))
    meanTable.rename(columns = {0 : 'mean_contagios'}, inplace = True)
    stdTable.rename(columns = {0 : 'std_contagios'}, inplace = True)
    Contagios_final = meanTable.join(stdTable)
    Contagios_final.index = [value.lower() for value in list(Contagios_final.index)]
    return Contagios_final

def get_data(fecha_inicio, fecha_final):
	activos = pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna.csv",
                      delimiter=',')

	activos = activos.dropna(subset=['Codigo comuna'])
	activos['Codigo comuna'] = activos['Codigo comuna'].apply(int).apply(str)
	indices = activos[['Codigo comuna', 'Region', 'Comuna']] 
	Poblacion = activos["Poblacion"]
	activos = activos.drop(['Codigo comuna', "Codigo region", "Region","Comuna","Poblacion"], axis=1)
	activos = activos.div(Poblacion, axis= 0)
	activos = activos.transpose()
	activos.index = pd.to_datetime(list(activos.index.values))
	activos = activos.loc['2020-12-01':'2021-03-01']
	activos = activos.transpose()
	d = {'mean_act': activos.mean(axis=1), 'std_act': activos.std(axis=1)}
	activosMedidas = pd.DataFrame(data=d).join(indices)
	activosMedidas = activosMedidas.set_index('Comuna')
	activosMedidas.index = [value.lower() for value in list(activosMedidas.index)]
	activosMedidas.drop(columns=["Codigo comuna", "Region"], inplace=True)

	fallecidos = pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto38/CasosFallecidosPorComuna.csv", delimiter= ',')

	fallecidos = fallecidos.dropna(subset=['Codigo comuna'])
	fallecidos['Codigo comuna'] = fallecidos['Codigo comuna'].apply(int).apply(str)
	indices1 = fallecidos[['Codigo comuna', 'Region', 'Comuna']] 
	Poblacion = fallecidos["Poblacion"]
	fallecidos2 = fallecidos
	fallecidos = fallecidos.drop(['Codigo comuna', "Codigo region", "Region","Comuna","Poblacion"], axis=1)
	fallecidos = fallecidos.div(Poblacion, axis=0)
	fallecidos = fallecidos.transpose()
	fallecidos.index = pd.to_datetime(list(fallecidos.index.values))
	fallecidos = fallecidos.loc[fecha_inicio:fecha_final]
	fallecidos = fallecidos.transpose()
	d1 = {'mean_fallecidos': fallecidos.mean(axis=1), 'std_fallecidos': fallecidos.std(axis=1)}
	fallecidosMedidas = pd.DataFrame(data=d1).join(indices1)
	fallecidosMedidas = fallecidosMedidas.set_index('Comuna')
	fallecidosMedidas.index = [value.lower() for value in list(fallecidosMedidas.index)]
	fallecidosMedidas.drop(columns=["Codigo comuna", "Region"], inplace=True)

	movilidadMedidas = getMovilidadDeComunasDeRegion(fecha_inicio, fecha_final)
	contagiosMedidas = get_densidad_contagios(dates)
	X = activosMedidas.join(fallecidosMedidas).join(movilidadMedidas).join(contagiosMedidas)
	X = X.dropna()

	k_res = []
	possible_k = range(1, 16)
	for k in possible_k:
	  k_means_alg = KMeans(n_clusters=k, random_state=100)
	  k_means_alg.fit(X)
	  k_res.append(k_means_alg.inertia_)

	plt.plot(possible_k, k_res, "r*")
	plt.xlabel("Possibles clusters")
	plt.xticks(possible_k)
	plt.ylabel("SSE")
	plt.title("N de clusters mediante técnica del codo")

	return X


def get_cluster(X, n_clusters, model):
	clusters = [list() for _ in range(n_clusters)]
	for i in range(len(kmeans.labels_)):
	    comuna = X.index[i]
	    cluster = model.labels_[i]
	    clusters[cluster].append(comuna)
	
	for cluster in clusters:
		cluster.sort()
	return clusters



def reduce_data(X, n_components):
	reduced_data = PCA(n_components, random_state=100).fit_transform(X)
	return reduced_data

def show_clusters_kmeans(X, n_clusters):
	X = reduce_data(X, n_clusters)
	kmeans = KMeans(n_clusters=n_clusters, random_state=100)
	kmeans.fit(X)
	plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_)
	plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], s=200, facecolors='none', edgecolors='r')
	plt.title("kmeans values in 2D")
	plt.show()



def aglomerative(X, threshold):
	model = AgglomerativeClustering(distance_threshold=threshold, n_clusters=None, linkage="ward")\
                        .fit(X)
	figure(figsize=(10, 8), dpi=80)
	plt.title('Hierarchical Clustering Dendrogram')
	plot_dendrogram(model, truncate_mode='level', p=3)
	plt.xlabel("Number of points in node (or index of point if no parenthesis).")
	return model

