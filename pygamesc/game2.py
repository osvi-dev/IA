import pygame
import random
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None
menu = None

# Variables de salto
salto = False
salto_altura = 15  # Velocidad inicial de salto
gravedad = 1.5
en_suelo = True

movimiento_izquierda = False
movimiento_derecha = False
paso_lateral = 60
# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático

# Variables para controlar el algoritmo elegido
usar_red_neuronal = False 
usar_arbol_decision = False
usar_knn = False

# Lista para guardar los datos de velocidad, distancia_x y salto (target)
datos_modelo = []

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('pygamesc/assets/sprites/mono_frame_1.png'),
    pygame.image.load('pygamesc/assets/sprites/mono_frame_2.png'),
    pygame.image.load('pygamesc/assets/sprites/mono_frame_3.png'),
    pygame.image.load('pygamesc/assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('pygamesc/assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('pygamesc/assets/game/fondo2.png')
nave_img = pygame.image.load('pygamesc/assets/game/ufo.png')
nave2_img = pygame.image.load('pygamesc/assets/game/ufo.png')
menu_img = pygame.image.load('pygamesc/assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
X_JUGADOR = 100
X_BALA2 = 105
X_NAVE2 = 65

jugador = pygame.Rect(X_JUGADOR , h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
nave2 = pygame.Rect(X_NAVE2, 30, 64, 64)
bala2 = pygame.Rect(X_BALA2, 100, 16, 16)  # Segunda bala para la nave

menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Variables para la bala
velocidad_bala = -10  # Velocidad de la bala hacia la izquierda
velocidad_bala2 = 5 # Velocidad de la segunda bala hacia abajo

bala_disparada = False
bala_disparada2 = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Definimos la red neuronal con una capa oculta de 10 neuronas
mlp = MLPClassifier(hidden_layer_sizes=(10,), activation='relu', solver='adam', max_iter=1000, random_state=42)
mlp2 = MLPClassifier(hidden_layer_sizes=(10,), activation='relu', solver='adam', max_iter=1000, random_state=42)
mlp3 = MLPClassifier(hidden_layer_sizes=(10,), activation='relu', solver='adam', max_iter=1000, random_state=42)

# Definimos el Decision Tree
clf = DecisionTreeClassifier()
clf2 = DecisionTreeClassifier()
clf3 = DecisionTreeClassifier()

# Definimos los KNN
knn =  KNeighborsClassifier(n_neighbors=5)
knn2 = KNeighborsClassifier(n_neighbors=5)
knn3 = KNeighborsClassifier(n_neighbors=5)

# Variables para el modelo
modelo_entrenado_salto = False
modelo_entrenado_izquierda = False
modelo_entrenado_derecha = False

scaler_salto = StandardScaler()  # Para normalizar los datos
scaler_izquierda = StandardScaler()
scaler_derecha = StandardScaler()

def split_data_x():
    """
    Divide los datos en conjuntos de entrenamiento y prueba.
    
    Returns:
        X_train, X_test, y_train, y_test: Conjuntos de datos divididos
    """
    global datos_modelo
    
    if len(datos_modelo) == 0:
        print("No hay datos para entrenar el modelo. Juega en modo manual primero.")
        return None
    
    X, y = [], []
    for i in range(len(datos_modelo)):
        X.append([abs(datos_modelo[i][0]), datos_modelo[i][1], datos_modelo[i][2], datos_modelo[i][3], datos_modelo[i][4]])  # velocidad_bala, distancia_x, distancia_y, izquierda, derecha
        y.append(datos_modelo[i][5])  # salto_hecho
    
    print("\n\nLas X son: ", X)
    print("\n\nLas Y son: ", y)
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

def split_data_izquierda():
    X, y = [], []
    for i in range(len(datos_modelo)):
        X.append([abs(datos_modelo[i][0]), datos_modelo[i][1], datos_modelo[i][2], datos_modelo[i][4], datos_modelo[i][5]])  # velocidad_bala, distancia_x, distancia_y, derecha, salto_hecho
        y.append(datos_modelo[i][3])  # izquierda
    
    print("\n\nLas X son: ", X)
    print("\n\nLas Y son: ", y)
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

def split_data_derecha():
    X, y = [], []
    for i in range(len(datos_modelo)):
        X.append([abs(datos_modelo[i][0]), datos_modelo[i][1], datos_modelo[i][2], 
                 datos_modelo[i][3], datos_modelo[i][5]])  # velocidad_bala, distancia_x, distancia_y, izquierda, salto_hecho
        y.append(datos_modelo[i][4])  # derecha
    
    print("\n\nLas X son: ", X)
    print("\n\nLas Y son: ", y)
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

def entrenar_red_neuronal():
    """
    Entrena un modelo de red neuronal para predecir si el jugador debe saltar o no.

    Se utilizan los datos de entrenamiento guardados en la variable global
    `datos_modelo`. Separamos los datos en X (características) y y (clases), y
    luego se dividen en conjuntos de entrenamiento y prueba. Luego se entrenan
    los datos de entrenamiento y se evalúa la precisión del modelo en los datos
    de prueba.

    La precisión se imprime en la consola.

    Returns:
        El modelo entrenado
    """
    global modelo_entrenado_salto, mlp, scaler_salto
        
    
    # Entrenamos la red neuronal
    X_train, X_test, y_train, y_test = split_data_x()
    
    # Normalizamos los datos
    X_train = scaler_salto.fit_transform(X_train)
    X_test = scaler_salto.transform(X_test)
    
    mlp.fit(X_train, y_train)
    y_pred = mlp.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'\nPrecisión de la Red Neuronal en test: {accuracy:.4f}')
    
    modelo_entrenado_salto = True
    return mlp


def entrenar_red_neuronal_izquierda():
    global modelo_entrenado_izquierda, mlp2, scaler_izquierda
    
    # Entrenamos la red neuronal
    X_train, X_test, y_train, y_test = split_data_izquierda()
    
    # Normalizamos los datos
    X_train = scaler_izquierda.fit_transform(X_train)
    X_test = scaler_izquierda.transform(X_test)
    
    mlp2.fit(X_train, y_train)
    y_pred = mlp2.predict(X_test)  # Changed from mlp to mlp2

    accuracy = accuracy_score(y_test, y_pred)
    print(f'\nPrecisión de la Red Neuronal en test: {accuracy:.4f}')
    
    modelo_entrenado_izquierda = True
    return mlp2

def entrenar_red_neuronal_derecha():
    global modelo_entrenado_derecha, mlp3, scaler_derecha 
    
    # Entrenamos la red neuronal
    X_train, X_test, y_train, y_test = split_data_derecha()
    
    # Normalizamos los datos
    X_train = scaler_derecha.fit_transform(X_train)
    X_test = scaler_derecha.transform(X_test)
    
    mlp3.fit(X_train, y_train)
    y_pred = mlp3.predict(X_test)  # Changed from mlp to mlp3

    accuracy = accuracy_score(y_test, y_pred)
    print(f'\nPrecisión de la Red Neuronal en test: {accuracy:.4f}')
    
    modelo_entrenado_derecha = True
    return mlp3

def hacer_prediccion_red_neuronal():
    """
    Predice si el jugador debe saltar o no usando el modelo entrenado.
    
    Returns:
        bool: True si el jugador debe saltar, False en caso contrario
    """
    global mlp, modelo_entrenado_salto, scaler_salto, jugador, bala, bala2, velocidad_bala, movimiento_izquierda, movimiento_derecha
    
    if not modelo_entrenado_salto:
        # Si el modelo no está entrenado aún, retornamos False (no saltar)
        return False
    
    # Datos actuales: velocidad de la bala y distancia_x al jugador
    distancia_x = abs(jugador.x - bala.x)
    distancia_y = abs(jugador.y - bala2.y)
    # velocidad_bala, distancia_x, distancia_y, izquierda, derecha, salto_hecho
    datos_actuales = [[abs(velocidad_bala), distancia_x, distancia_y, movimiento_izquierda, movimiento_derecha]]
    
    # Normalizamos los datos con el mismo scaler usado en el entrenamiento
    datos_normalizados = scaler_salto.transform(datos_actuales)
    
    # Hacemos la predicción
    prediccion = mlp.predict(datos_normalizados)
    
    # Retornamos True si la predicción es 1 (saltar), False si es 0 (no saltar)
    return prediccion[0] == 1
def hacer_prediccion_izquierda_red_neuronal():
    global mlp2, modelo_entrenado_izquierda, scaler_izquierda, jugador, bala, bala2, velocidad_bala, velocidad_bala2
    
    if not modelo_entrenado_izquierda:
        return False
    
    # Asegurar que usamos los mismos datos que usamos para entrenar
    distancia_x = abs(jugador.x - bala.x)
    distancia_y = abs(jugador.y - bala2.y)
    # [velocidad_bala, distancia_x, distancia_y, derecha, salto]
    datos_actuales = [[abs(velocidad_bala), distancia_x, distancia_y, movimiento_derecha, salto]]
    
    try:
        # Normalizamos los datos con el mismo scaler usado en el entrenamiento
        datos_normalizados = scaler_izquierda.transform(datos_actuales)
        
        # Hacemos la predicción
        prediccion = mlp2.predict(datos_normalizados)
        return prediccion[0] == 1
    except Exception as e:
        print(f"Error en predicción izquierda: {e}")
        return False

def hacer_prediccion_derecha_red_neuronal():
    global mlp3, modelo_entrenado_derecha, scaler_derecha, jugador, bala, bala2, velocidad_bala, movimiento_izquierda, salto
    
    if not modelo_entrenado_derecha:
        # Si el modelo no está entrenado aún, retornamos False (no moverse a la derecha)
        return False
    
    # Datos actuales: velocidad de la bala y distancia_x al jugador
    distancia_x = abs(jugador.x - bala.x)
    distancia_y = abs(jugador.y - bala2.y)
    # velocidad_bala, distancia_x, distancia_y, izquierda, salto
    datos_actuales = [[abs(velocidad_bala), distancia_x, distancia_y, movimiento_izquierda, salto]]
    
    # Normalizamos los datos con el mismo scaler usado en el entrenamiento
    datos_normalizados = scaler_derecha.transform(datos_actuales)
    
    # Hacemos la predicción
    prediccion = mlp3.predict(datos_normalizados)
    
    return prediccion[0] == 1
 
def entrenar_decision_tree():
    """
    Entrena un modelo de Decision Tree para predecir si el jugador debe saltar o no.

    Se utilizan los datos de entrenamiento guardados en la variable global
    `datos_modelo`. Separamos los datos en X (características) y y (clases), y
    luego se dividen en conjuntos de entrenamiento y prueba. Luego se entrenan
    los datos de entrenamiento y se evalúa la precisión del modelo en los datos
    de prueba.

    La precisión se imprime en la consola.

    Returns:
        El modelo entrenado
    """
    global modelo_entrenado_salto, clf
    
    # Entrenamos el árbol de decisión
    X_train, X_test, y_train, y_test = split_data_x()
    
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'\nPrecisión del Árbol de Decisión en test: {accuracy:.4f}')
    
    modelo_entrenado_salto = True
    return clf   

def entrenar_decision_tree_izquierda():
    global modelo_entrenado_izquierda, clf2
    
    # Entrenamos el árbol de decisión
    X_train, X_test, y_train, y_test = split_data_izquierda()
    
    clf2.fit(X_train, y_train)
    y_pred = clf2.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'\nPrecisión del Árbol de Decisión en test: {accuracy:.4f}')
    
    modelo_entrenado_izquierda = True
    return clf2

def entrenar_decision_tree_derecha():
    global modelo_entrenado_derecha, clf3
    
    # Entrenamos el árbol de decisión
    X_train, X_test, y_train, y_test = split_data_derecha()
    
    clf3.fit(X_train, y_train)
    y_pred = clf3.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'\nPrecisión del Árbol de Decisión en test: {accuracy:.4f}')
    
    modelo_entrenado_derecha = True
    return clf3

def hacer_prediccion_decision_tree():
    """
    Predice si el jugador debe saltar o no usando el árbol de decisión.
    
    Returns:
        bool: True si el jugador debe saltar, False en caso contrario
    """
    global clf, modelo_entrenado_salto, jugador, bala, velocidad_bala, bala2, movimiento_izquierda, movimiento_derecha
    
    if not modelo_entrenado_salto:
        # Si el modelo no está entrenado aún, retornamos False (no saltar)
        return False
    
    # Datos actuales: velocidad de la bala y distancia_x al jugador
    distancia_x = abs(jugador.x - bala.x)
    distancia_y = abs(jugador.y - bala2.y)
    
    datos_actuales = [[abs(velocidad_bala), distancia_x, distancia_y, movimiento_izquierda, movimiento_derecha]]
    
    # Hacemos la predicción
    prediccion = clf.predict(datos_actuales)
    
    # Retornamos True si la predicción es 1 (saltar), False si es 0 (no saltar)
    return prediccion[0] == 1

def hacer_prediccion_izquierda_decision_tree():
    global clf2, modelo_entrenado_izquierda, jugador, bala, bala2, velocidad_bala, movimiento_derecha, salto
    
    if not modelo_entrenado_izquierda:
        return False
    
    # Datos actuales: velocidad de la bala y distancia_x al jugador
    distancia_x = abs(jugador.x - bala.x)
    distancia_y = abs(jugador.y - bala2.y)
    datos_actuales = [[abs(velocidad_bala), distancia_x, distancia_y, movimiento_derecha, salto]]
    
    # Hacemos la predicción
    prediccion = clf2.predict(datos_actuales)
    
    return prediccion[0] == 1

def hacer_prediccion_derecha_decision_tree():
    global clf3, modelo_entrenado_derecha, jugador, bala, bala2, velocidad_bala, movimiento_izquierda, salto
    
    if not modelo_entrenado_derecha:
        return False
    
    # Datos actuales: velocidad de la bala y distancia_x al jugador
    distancia_x = abs(jugador.x - bala.x)
    distancia_y = abs(jugador.y - bala2.y)
    datos_actuales = [[abs(velocidad_bala), distancia_x, distancia_y, movimiento_izquierda, salto]]
    
    # Hacemos la predicción
    prediccion = clf3.predict(datos_actuales)
    
    return prediccion[0] == 1

def entrenar_knn():
    """
    Entrena un modelo KNN para predecir si el jugador debe saltar o no.
    
    Returns:
        El modelo entrenado
    """
    global modelo_entrenado_salto, knn
    
    # Entrenamos el KNN
    X_train, X_test, y_train, y_test = split_data_x()
    
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'\nPrecisión del KNN en test: {accuracy:.4f}')
    
    modelo_entrenado_salto = True
    return knn

def entrenar_knn_izquierda():
    """
    Entrena un modelo KNN para predecir si el jugador debe moverse a la izquierda.
    
    Returns:
        El modelo entrenado
    """
    global modelo_entrenado_izquierda, knn2
    
    # Entrenamos el KNN
    X_train, X_test, y_train, y_test = split_data_izquierda()
    
    knn2.fit(X_train, y_train)
    y_pred = knn2.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'\nPrecisión del KNN para movimiento izquierdo en test: {accuracy:.4f}')
    
    modelo_entrenado_izquierda = True
    return knn2

def entrenar_knn_derecha():
    """
    Entrena un modelo KNN para predecir si el jugador debe moverse a la derecha.
    
    Returns:
        El modelo entrenado
    """
    global modelo_entrenado_derecha, knn3
    
    # Entrenamos el KNN
    X_train, X_test, y_train, y_test = split_data_derecha()
    
    knn3.fit(X_train, y_train)
    y_pred = knn3.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'\nPrecisión del KNN para movimiento derecho en test: {accuracy:.4f}')
    
    modelo_entrenado_derecha = True
    return knn3

# Funciones de predicción para KNN
def hacer_prediccion_knn():
    """
    Predice si el jugador debe saltar o no usando KNN.
    
    Returns:
        bool: True si el jugador debe saltar, False en caso contrario
    """
    global knn, modelo_entrenado_salto, jugador, bala, bala2, velocidad_bala, movimiento_izquierda, movimiento_derecha
    
    if not modelo_entrenado_salto:
        # Si el modelo no está entrenado aún, retornamos False (no saltar)
        return False
    
    # Datos actuales: velocidad de la bala y distancia_x al jugador
    distancia_x = abs(jugador.x - bala.x)
    distancia_y = abs(jugador.y - bala2.y)
    
    datos_actuales = [[abs(velocidad_bala), distancia_x, distancia_y, movimiento_izquierda, movimiento_derecha]]
    
    # Hacemos la predicción
    prediccion = knn.predict(datos_actuales)
    
    # Retornamos True si la predicción es 1 (saltar), False si es 0 (no saltar)
    return prediccion[0] == 1

def hacer_prediccion_izquierda_knn():
    """
    Predice si el jugador debe moverse a la izquierda usando KNN.
    
    Returns:
        bool: True si el jugador debe moverse a la izquierda, False en caso contrario
    """
    global knn2, modelo_entrenado_izquierda, jugador, bala, bala2, velocidad_bala, movimiento_derecha, salto
    
    if not modelo_entrenado_izquierda:
        return False
    
    # Datos actuales: velocidad de la bala y distancia_x al jugador
    distancia_x = abs(jugador.x - bala.x)
    distancia_y = abs(jugador.y - bala2.y)
    datos_actuales = [[abs(velocidad_bala), distancia_x, distancia_y, movimiento_derecha, salto]]
    
    # Hacemos la predicción
    prediccion = knn2.predict(datos_actuales)
    
    return prediccion[0] == 1

def hacer_prediccion_derecha_knn():
    """
    Predice si el jugador debe moverse a la derecha usando KNN.
    
    Returns:
        bool: True si el jugador debe moverse a la derecha, False en caso contrario
    """
    global knn3, modelo_entrenado_derecha, jugador, bala, bala2, velocidad_bala, movimiento_izquierda, salto
    
    if not modelo_entrenado_derecha:
        return False
    
    # Datos actuales: velocidad de la bala y distancia_x al jugador
    distancia_x = abs(jugador.x - bala.x)
    distancia_y = abs(jugador.y - bala2.y)
    datos_actuales = [[abs(velocidad_bala), distancia_x, distancia_y, movimiento_izquierda, salto]]
    
    # Hacemos la predicción
    prediccion = knn3.predict(datos_actuales)
    
    return prediccion[0] == 1
        
def hacer_prediccion():
    """
    Función que decide qué modelo usar para hacer la predicción.
    
    Returns:
        bool: True si el jugador debe saltar, False en caso contrario
    """
    if usar_red_neuronal:
        return hacer_prediccion_red_neuronal()
    elif usar_arbol_decision:
        return hacer_prediccion_decision_tree()
    elif usar_knn:
        return hacer_prediccion_knn()
    else:
        return False
def hacer_prediccion_izquierda():
    """
    Función que decide qué modelo usar para hacer la predicción de movimiento izquierda.
    
    Returns:
        bool: True si el jugador debe moverse a la izquierda, False en caso contrario
    """
    if usar_red_neuronal:
        return hacer_prediccion_izquierda_red_neuronal()
    elif usar_arbol_decision:
        return hacer_prediccion_izquierda_decision_tree()
    elif usar_knn:
        return hacer_prediccion_izquierda_knn()
    else:
        return False
    
def hacer_prediccion_derecha():
    """
    Función que decide qué modelo usar para hacer la predicción de movimiento a la derecha.
    
    Returns:
        bool: True si el jugador debe moverse a la derecha, False en caso contrario
    """
    if usar_red_neuronal:
        return hacer_prediccion_derecha_red_neuronal()
    elif usar_arbol_decision:
        return hacer_prediccion_derecha_decision_tree()
    elif usar_knn:
        return hacer_prediccion_derecha_knn()
    else:
        return False
# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-10, -5)  # Velocidad aleatoria de la bala
        bala_disparada = True
        
def disparar_bala2():
    global bala_disparada2, velocidad_bala2
    if not bala_disparada2:
        bala_disparada2 = True
    
# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False

def reset_bala2():
    global bala2, bala_disparada2, movimiento_derecha, movimiento_izquierda
    bala2.y = 100  # Reiniciar la posición de la segunda bala
    bala_disparada2, movimiento_derecha, movimiento_izquierda = False, False, False  # Reiniciar el movimiento
    jugador.x = X_JUGADOR     # Reiniciar la posición del jugador
    
# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15  # Restablecer la velocidad de salto
            en_suelo = True

# Función para manejar el movimiento lateral           
def manejar_movimiento_lateral():
    global jugador, movimiento_izquierda, movimiento_derecha, paso_lateral

    if movimiento_izquierda and jugador.x > 40:
        jugador.x -= paso_lateral  # Mover a la izquierda
    if movimiento_derecha and jugador.x < 160:
        jugador.x += paso_lateral  # Mover a la derecha
        
        
# Función para actualizar el juego
def update():
    global bala, bala2, velocidad_bala, velocidad_bala2, current_frame, frame_count, fondo_x1, fondo_x2

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    # Si el primer fondo sale de la pantalla, lo movemos detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w

    # Si el segundo fondo sale de la pantalla, lo movemos detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar los fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar el jugador con la animación
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Dibujar la nave
    pantalla.blit(nave_img, (nave.x, nave.y))
    pantalla.blit(nave2_img, (nave2.x, nave2.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala
        
    if bala_disparada2:
        bala2.y += velocidad_bala2
        
    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()
        
    if bala2.y > h:
        reset_bala2()

    pantalla.blit(bala_img, (bala.x, bala.y))
    pantalla.blit(bala_img, (bala2.x, bala2.y)) 
    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala) or jugador.colliderect(bala2):
        print("Colisión detectada!")
        reiniciar_juego()  # Terminar el juego y mostrar el menú

# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala, bala2, velocidad_bala, salto
    
    distancia_x = abs(jugador.x - bala.x)
    distancia_y = abs(jugador.y - bala2.y)
    
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    izquierda = 1 if movimiento_izquierda else 0  # 1 si se mueve a la izquierda, 0 si no
    derecha = 1 if movimiento_derecha else 0  # 1 si se mueve a la derecha, 0 si no
    
    # Guardar velocidad de la bala, distancia_x al jugador y si saltó o no
    datos_modelo.append((velocidad_bala, distancia_x, distancia_y, izquierda, derecha, salto_hecho))

# Función para pausar el juego y guardar los datos
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto, usar_red_neuronal, usar_arbol_decision, usar_knn, modelo_entrenado_salto
    global modelo_entrenado_derecha, modelo_entrenado_izquierda
    global datos_modelo

    pantalla.fill(NEGRO)
    texto1 = fuente.render("Presiona 'N' para usar Red Neuronal", True, BLANCO)
    texto2 = fuente.render("Presiona 'A' para usar Árbol de Decisión", True, BLANCO)
    texto3 = fuente.render("Presiona 'K' para usar KNN", True, BLANCO)
    texto4 = fuente.render("Presiona 'M' para Modo Manual (entrenamiento)", True, BLANCO)
    texto5 = fuente.render("Presiona 'Q' para Salir", True, BLANCO)
    
    pantalla.blit(texto1, (w // 4, h // 2 - 60))
    pantalla.blit(texto2, (w // 4, h // 2 - 30))
    pantalla.blit(texto3, (w // 4, h // 2))
    pantalla.blit(texto4, (w // 4, h // 2 + 30))
    pantalla.blit(texto5, (w // 4, h // 2 + 60))
    
    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_n:
                    modo_auto = True
                    menu_activo = False
                    
                    usar_red_neuronal = True
                    usar_arbol_decision = False
                    usar_knn = False                    
                    # Verificar si hay datos para entrenar
                    if len(datos_modelo) > 0:
                        # Forzar el reentrenamiento al cambiar de modelo
                        modelo_entrenado_salto, modelo_entrenado_derecha, modelo_entrenado_izquierda = False, False, False
                        
                        entrenar_red_neuronal()
                        entrenar_red_neuronal_izquierda()
                        entrenar_red_neuronal_derecha()
                        
                    elif len(datos_modelo) == 0:
                        print("No hay datos para entrenar el modelo. Juega en modo manual primero.")
                        modo_auto = False  # Volver a modo manual si no hay datos
                        
                elif evento.key == pygame.K_a: # Arboles de decisión
                    modo_auto = True
                    menu_activo = False
                    
                    usar_arbol_decision = True                    
                    usar_red_neuronal = False
                    usar_knn = False
                    # Verificar si hay datos para entrenar
                    if len(datos_modelo) > 0:
                        # Forzar el reentrenamiento al cambiar de modelo
                        modelo_entrenado_salto, modelo_entrenado_derecha, modelo_entrenado_izquierda = False, False, False
                        
                        entrenar_decision_tree()
                        entrenar_decision_tree_izquierda()
                        entrenar_decision_tree_derecha()
                    elif len(datos_modelo) == 0:
                        print("No hay datos para entrenar el modelo. Juega en modo manual primero.")
                        modo_auto = False  # Volver a modo manual si no hay datos
                
                elif evento.key == pygame.K_k: # KNN
                    modo_auto = True
                    menu_activo = False  
                    
                    usar_knn = True
                    usar_arbol_decision = False
                    usar_red_neuronal = False
                    # Verificar si hay datos para entrenar
                    if len(datos_modelo) > 0:
                        # Forzar el reentrenamiento al cambiar de modelo
                        modelo_entrenado_salto, modelo_entrenado_derecha, modelo_entrenado_izquierda = False, False, False
                        
                        entrenar_knn()
                        entrenar_knn_izquierda()
                        entrenar_knn_derecha()
                        
                    elif len(datos_modelo) == 0:
                        print("No hay datos para entrenar el modelo. Juega en modo manual primero.")
                        modo_auto = False  # Volver a modo manual si no hay datos
                                                
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    menu_activo = False
                    datos_modelo = []  # Reiniciar los datos del modelo
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()
# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, bala2, nave, bala_disparada, bala_disparada2, salto, en_suelo
    global modelo_entrenado_salto, movimiento_izquierda, movimiento_derecha
    global modelo_entrenado_izquierda, modelo_entrenado_derecha    
    
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = X_JUGADOR, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    bala2.y = 100
    bala2.x = X_BALA2  # Asegurar que bala2 vuelve a su posición X original
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    bala_disparada2 = False
    salto = False
    en_suelo = True
    movimiento_izquierda, movimiento_derecha = False, False  # Reiniciar el movimiento lateral
    
    # No reiniciar el estado de entrenamiento del modelo, solo mantenerlo
    # modelo_entrenado_salto, modelo_entrenado_derecha, modelo_entrenado_izquierda = False, False, False
    
    # Mostrar los datos recopilados hasta el momento
    print("Datos recopilados para el modelo: ", datos_modelo)
    
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo
    
def main():
    global salto, en_suelo, bala_disparada, bala_disparada2, movimiento_izquierda, movimiento_derecha

    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:  # Detectar la tecla espacio para saltar
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_LEFT:  # Presiona la tecla izquierda
                    movimiento_izquierda = True
                if evento.key == pygame.K_RIGHT:  # Presiona la tecla derecha
                    movimiento_derecha = True
                    
                if evento.key == pygame.K_p:  # Presiona 'p' para pausar el juego
                    pausa_juego()
                if evento.key == pygame.K_q:  # Presiona 'q' para terminar el juego
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    
                    pygame.quit()
                    exit()
                    
        if not pausa:
            manejar_movimiento_lateral()
            # Modo manual: el jugador controla el salto
            if not modo_auto:
                if salto:
                    manejar_salto()
                # Guardar los datos si estamos en modo manual
                guardar_datos()
                
            # Modo automático: el modelo predice cuándo saltar
            elif modo_auto:
                
                movimiento_izquierda = False
                if hacer_prediccion_izquierda():
                    movimiento_izquierda = True
                
                movimiento_derecha = False
                if hacer_prediccion_derecha():
                    movimiento_derecha = True
                        
                if en_suelo:
                    # Usar la función unificada de predicción
                    if hacer_prediccion():
                        salto = True
                        en_suelo = False
                if salto:
                    manejar_salto()
                    
            
            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
            
            if not bala_disparada2:
                disparar_bala2()    
                
            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(30)  # Limitar el juego a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
