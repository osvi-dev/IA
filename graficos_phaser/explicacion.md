# Graficando los Datos del Juego Phaser

Este documento explica el proceso de análisis y visualización de datos del juego desarrollado en Phaser. Utilizaremos `pandas` para manipular los datos y `matplotlib` para graficarlos en 2D y 3D.

## Importación de Librerías

Primero, importamos las librerías necesarias para manejar y visualizar los datos:

```python
import pandas as pd
import matplotlib.pyplot as plt
```

## Carga y Exploración del Dataset

Cargamos el dataset desde un archivo CSV y realizamos una inspección básica de su contenido.

```python
# Leemos el dataset
df = pd.read_csv('dataset.csv')
df
```

Para obtener una visión más detallada de los datos, utilizamos `describe()`:

```python
# Vemos la información más detallada del dataset
df.describe()
```

También verificamos si existen datos faltantes:

```python
# Verificar si hay datos faltantes
df.isnull().sum()
```

Si no hay datos faltantes, podemos proceder con la visualización.

## Gráfica 2D: Desplazamiento vs. Velocidad de la Bala

Realizamos un gráfico de dispersión (scatter plot) en 2D para visualizar la relación entre el desplazamiento y la velocidad de la bala, usando `Estatus Salto` como variable de color.

```python
# Gráfico en 2D
plt.figure(figsize=(10, 6))
plt.scatter(df['Desplazamiento Bala'], df['Velocidad Bala'], c=df['Estatus Salto'], cmap='managua')
plt.xlabel('Desplazamiento Bala')
plt.ylabel('Velocidad Bala')
plt.title('Desplazamiento vs Velocidad de la Bala')
plt.colorbar(label='Estatus Salto')
plt.show()
```

## Gráfica 3D: Análisis Completo de los Datos

Para obtener una visión más detallada, realizamos una gráfica en 3D donde se incluye la variable `Estatus Salto` como eje Z.

```python
# Gráfico en 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

scatter = ax.scatter(df['Desplazamiento Bala'],
                     df['Velocidad Bala'],
                     df['Estatus Salto'],
                     c=df['Estatus Salto'],
                     cmap='turbo')

ax.set_xlabel('Desplazamiento Bala')
ax.set_ylabel('Velocidad Bala')
ax.set_zlabel('Estatus del Salto')
ax.set_title('Análisis 3D de Datos del Juego')

plt.colorbar(scatter, label='Estatus Salto')
plt.show()
```


