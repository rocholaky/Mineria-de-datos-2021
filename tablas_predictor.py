from exploracionSG import *
from exploracionJO import *
from h3nc import *

clases = get_clases()

activos = get_activos_diarios_nacional()

asintomaticos = get_asintomaticos_diarios_nacional()

nombres_tablas = ["clases", "activos", "Vacunas", "PCR", "asintomaticos"]

print("nombres de tablas: " + str(nombres_tablas))