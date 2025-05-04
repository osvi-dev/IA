import pygame
import random
import pandas as pd
import csv

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

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
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático

# Variables para controlar el algoritmo elegido
usar_red_neuronal = False 
usar_arbol_decision = False

# Lista para guardar los datos de velocidad, distancia y salto (target)
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
menu_img = pygame.image.load('pygamesc/assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Variables para la bala
velocidad_bala = -10  # Velocidad de la bala hacia la izquierda
bala_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Definimos la red neuronal con una capa oculta de 10 neuronas
mlp = MLPClassifier(hidden_layer_sizes=(10,), activation='relu', solver='adam', max_iter=1000, random_state=42)

# Definimos el Decision Tree
clf = DecisionTreeClassifier()

# Variables para el modelo
modelo_entrenado = False
scaler = StandardScaler()  # Para normalizar los datos

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
    global modelo_entrenado, mlp, scaler
    
    if len(datos_modelo) == 0:
        print("No hay datos para entrenar el modelo. Juega en modo manual primero.")
        return None
        
    X, y = [], []
    for i in range(len(datos_modelo)):
        X.append([abs(datos_modelo[i][0]), datos_modelo[i][1]])  # velocidad_bala, distancia
        y.append(datos_modelo[i][2])  # salto_hecho
        
    print("\n\nLas X son: ", X)
    print("\n\nLas Y son: ", y)
    
    # Entrenamos la red neuronal
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Normalizamos los datos
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    mlp.fit(X_train, y_train)
    y_pred = mlp.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'\nPrecisión de la Red Neuronal en test: {accuracy:.4f}')
    
    modelo_entrenado = True
    return mlp

def hacer_prediccion_red_neuronal():
    """
    Predice si el jugador debe saltar o no usando el modelo entrenado.
    
    Returns:
        bool: True si el jugador debe saltar, False en caso contrario
    """
    global mlp, modelo_entrenado, scaler, jugador, bala, velocidad_bala
    
    if not modelo_entrenado:
        # Si el modelo no está entrenado aún, retornamos False (no saltar)
        return False
    
    # Datos actuales: velocidad de la bala y distancia al jugador
    distancia = abs(jugador.x - bala.x)
    datos_actuales = [[abs(velocidad_bala), distancia]]
    
    # Normalizamos los datos con el mismo scaler usado en el entrenamiento
    datos_normalizados = scaler.transform(datos_actuales)
    
    # Hacemos la predicción
    prediccion = mlp.predict(datos_normalizados)
    
    # Retornamos True si la predicción es 1 (saltar), False si es 0 (no saltar)
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
    global modelo_entrenado, clf
    
    if len(datos_modelo) == 0:
        print("No hay datos para entrenar el modelo. Juega en modo manual primero.")
        return None
        
    X, y = [], []
    for i in range(len(datos_modelo)):
        X.append([abs(datos_modelo[i][0]), datos_modelo[i][1]])  # velocidad_bala, distancia
        y.append(datos_modelo[i][2])  # salto_hecho
        
    print("\n\nLas X son: ", X)
    print("\n\nLas Y son: ", y)
    
    # Entrenamos el árbol de decisión
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'\nPrecisión del Árbol de Decisión en test: {accuracy:.4f}')
    
    modelo_entrenado = True
    return clf   

def hacer_prediccion_decision_tree():
    """
    Predice si el jugador debe saltar o no usando el árbol de decisión.
    
    Returns:
        bool: True si el jugador debe saltar, False en caso contrario
    """
    global clf, modelo_entrenado, jugador, bala, velocidad_bala
    
    if not modelo_entrenado:
        # Si el modelo no está entrenado aún, retornamos False (no saltar)
        return False
    
    # Datos actuales: velocidad de la bala y distancia al jugador
    distancia = abs(jugador.x - bala.x)
    datos_actuales = [[abs(velocidad_bala), distancia]]
    
    # Hacemos la predicción
    prediccion = clf.predict(datos_actuales)
    
    # Retornamos True si la predicción es 1 (saltar), False si es 0 (no saltar)
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
    else:
        return False

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-20, -6)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False

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

# Función para actualizar el juego
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2

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

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        reiniciar_juego()  # Terminar el juego y mostrar el menú

# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala, velocidad_bala, salto
    
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    # Guardar velocidad de la bala, distancia al jugador y si saltó o no
    datos_modelo.append((velocidad_bala, distancia, salto_hecho))

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
    global menu_activo, modo_auto, usar_red_neuronal, usar_arbol_decision, modelo_entrenado
    pantalla.fill(NEGRO)
    texto1 = fuente.render("Presiona 'N' para usar Red Neuronal", True, BLANCO)
    texto2 = fuente.render("Presiona 'A' para usar Árbol de Decisión", True, BLANCO)
    texto3 = fuente.render("Presiona 'M' para Modo Manual (entrenamiento)", True, BLANCO)
    texto4 = fuente.render("Presiona 'Q' para Salir", True, BLANCO)
    
    pantalla.blit(texto1, (w // 4, h // 2 - 60))
    pantalla.blit(texto2, (w // 4, h // 2 - 30))
    pantalla.blit(texto3, (w // 4, h // 2))
    pantalla.blit(texto4, (w // 4, h // 2 + 30))
    
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
                    
                    # Verificar si hay datos para entrenar
                    if not modelo_entrenado and len(datos_modelo) > 0:
                        entrenar_red_neuronal()
                    elif len(datos_modelo) == 0:
                        print("No hay datos para entrenar el modelo. Juega en modo manual primero.")
                        modo_auto = False  # Volver a modo manual si no hay datos
                        
                elif evento.key == pygame.K_a:
                    modo_auto = True
                    menu_activo = False
                    usar_red_neuronal = False
                    usar_arbol_decision = True
                    
                    # Verificar si hay datos para entrenar
                    if not modelo_entrenado and len(datos_modelo) > 0:
                        entrenar_decision_tree()
                    elif len(datos_modelo) == 0:
                        print("No hay datos para entrenar el modelo. Juega en modo manual primero.")
                        modo_auto = False  # Volver a modo manual si no hay datos
                                
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    menu_activo = False
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True
    # Mostrar los datos recopilados hasta el momento
    print("Datos recopilados para el modelo: ", datos_modelo)
    
    # Guardamos en un csv (opcional, comentado por defecto)
    # headings = ['velocidad_bala', 'distancia', 'salto_hecho']
    #with open('./prueba1.csv', mode='w', newline='') as file:
    #    writer = csv.writer(file)
    #    writer.writerow(headings)
    #    writer.writerows(datos_modelo)
    #print(f"Archivo 'prueba1.csv' creado exitosamente.") 
    
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo
    
def main():
    global salto, en_suelo, bala_disparada

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
                if evento.key == pygame.K_p:  # Presiona 'p' para pausar el juego
                    pausa_juego()
                if evento.key == pygame.K_q:  # Presiona 'q' para terminar el juego
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    
                    pygame.quit()
                    exit()
                    
        if not pausa:
            # Modo manual: el jugador controla el salto
            if not modo_auto:
                if salto:
                    manejar_salto()
                # Guardar los datos si estamos en modo manual
                guardar_datos()
                
            # Modo automático: el modelo predice cuándo saltar
            elif modo_auto:
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
                
            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(30)  # Limitar el juego a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
