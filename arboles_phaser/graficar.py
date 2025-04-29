import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz
import os

juego_normal = pd.read_csv('arboles_pasher/prueba1.csv')
X_juego_uno = juego_normal.iloc[:, :2]
y_juego_uno = juego_normal.iloc[:, 2]

clf = DecisionTreeClassifier()
clf.fit(X_juego_uno, y_juego_uno)

# Generar el gráfico
dot_data = export_graphviz(
    clf,
    out_file=None,
    feature_names=X_juego_uno.columns,
    class_names=['no salto', 'salto'],
    filled=True,
    rounded=True
)

graph = graphviz.Source(dot_data)

# Intentar visualizar o guardar
try:
    graph.view()
except graphviz.backend.execute.ExecutableNotFound:
    print("Graphviz no está en el PATH. Guardando como PDF...")
    graph.render('arboles_pasher/juego1', format='pdf', cleanup=True)