from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC  # support vector machine classifier
from sklearn.metrics import f1_score, recall_score, precision_score,average_precision_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from exploracionSG import *
from exploracionJO import *
from h3nc import *

clases = get_clases()

activos = get_activos_diarios_nacional()

asintomaticos = get_asintomaticos_diarios_nacional()

nombres_tablas = ["clases", "activos", "Vacunas", "PCR", "asintomaticos"]

print("nombres de tablas: " + str(nombres_tablas))

total = activos.join(Vacunas).join(PCR).join(asintomaticos).join(clases)
total.dropna(inplace=True)

print("total es el DataFrame que contiene todo (menos las clases)")

def run_classifier(clf, X, y, num_tests=100):
    metrics = {'f1-score': [], 'precision': [], 'recall': []}
    
    for _ in range(num_tests):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.30)
        
        
        clf.fit(X_train, y_train)
        predictions = clf.predict(X_test)

        
        metrics['y_pred'] = predictions
        metrics['f1-score'].append(f1_score(y_test, predictions, 
                                                    average='micro')) 
        metrics['recall'].append(recall_score(y_test, predictions, 
                                                    average='micro'))
        metrics['precision'].append(precision_score(y_test, predictions, 
                                                    average='micro'))
    print(classification_report(y_test, predictions))
    return metrics

X = total.drop(['class'], axis=1).values
y = total['class'].values



c0 = ("Decision Tree", DecisionTreeClassifier(max_depth=5))
c1 = ("KNN", KNeighborsClassifier(n_neighbors=10))
c2 = ("Support Vector Machines", SVC())

classifiers = [c0, c1, c2]

results = {}
for name, clf in classifiers:
    metrics = run_classifier(clf, X, y)   # hay que implementarla en el bloque anterior.
    results[name] = metrics
    print("----------------")
    print("Resultados para clasificador: ", name) 
    print("Precision promedio:", np.array(metrics['precision']).mean())
    print("Recall promedio:", np.array(metrics['recall']).mean())
    print("F1-score promedio:", np.array(metrics['f1-score']).mean())
    print("----------------\n\n")  
