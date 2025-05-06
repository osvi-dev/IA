# Explicación del Código del Juego con Aprendizaje Automático

Este código implementa un juego simple utilizando Pygame, donde un jugador debe esquivar balas disparadas por una nave. Incluye un modo manual y un modo automático que utiliza una red neuronal para decidir cuándo saltar. A continuación, se detalla su estructura y funcionalidad.

## 🔨 Dependencias
- **Pygame**: Para la creación de la interfaz gráfica y manejo de eventos.
- **Random**: Generación de velocidades aleatorias para las balas.
- **Pandas/CSV**: Manejo de datos (comentado en el código).
- **Scikit-learn**: Implementación de tres algoritmos de aprendizaje automático:

  - `MLPClassifier`: Red neuronal para modo automático.
  - `DecisionTreeClassifier`: Árbol de decisión para modo automático.
  - `LogisticRegression`: Regresión logística para modo automático.

---

## 🎮 Componentes Principales del Juego

### 1. **Elementos Gráficos**
- **Jugador**: Animado con 4 sprites, salta con la tecla `Espacio`.
- **Bala**: Se dispara desde la derecha hacia el jugador.
- **Nave UFO**: Posicionada en la parte derecha de la pantalla.
- **Fondo**: Dos imágenes en movimiento continuo para efecto de desplazamiento.
- **Menú**: Permite seleccionar entre:
  - modo manual (`M`)
  - Red Neuronal (`N`) para modo automático
  - Árbol de Decisión (`A`) para modo automático
  - Regresión Logística (`L`) para modo automático
  - Salir (`Q`)


### 2. **Mecánicas del Juego**
- **Salto**: Controlado por gravedad y velocidad inicial.
- **Colisiones**: Si la bala impacta al jugador, el juego se reinicia.
- **Modo Pausa**: Tecla `P` detiene/reanuda el juego.
- **Fondo en Movimiento**: Crea la ilusión de avance continuo.

---

## 🤖 Integración con Red Neuronal

### 🔄 Flujo de Datos
1. **Recolección de Datos (Modo Manual)**:
   - **Características**: Velocidad de la bala y distancia al jugador.
   - **Target**: `1` si el jugador saltó, `0` si no.
   - Almacenamiento en `datos_modelo`.

2. **Entrenamiento del Modelo**:
   - **Preprocesamiento**: Normalización con `StandardScaler`.
   - **División de Datos**: 80% entrenamiento, 20% prueba.
   - **Algoritmos disponibles**:

  - `Red Neuronal (MLPClassifier)`: Perceptrón multicapa con una capa oculta de 10 neuronas.
  - `Árbol de Decisión (DecisionTreeClassifier)`: Modelo basado en reglas para clasificación.
  - `Regresión Logística (LogisticRegression)`: Modelo lineal para clasificación binaria.
   - **Precisión**: Evaluada con `accuracy_score`.

3. **Predicción (Modo Automático)**:
   - Usa el modelo entrenado para decidir saltos basado en la velocidad actual de la bala y la distancia al jugador.

---

## 📝 Funciones Clave

### 🕹️ Funciones del Juego
- `manejar_salto()`: Controla la física del salto (gravedad y posición).
- `disparar_bala()`: Inicia el movimiento de la bala con velocidad aleatoria.
- `update()`: Actualiza posiciones, animaciones y detecta colisiones.
- `guardar_datos()`: Almacena datos en modo manual para entrenamiento.

### 🧠 Funciones del Modelo
- `split_data()`: Divide los datos recopilados en conjuntos de entrenamiento y prueba.
Funciones específicas por modelo:

- **Red Neuronal**:
  - `entrenar_red_neuronal()`: Entrena el modelo MLP con los datos recolectados.
  - `hacer_prediccion_red_neuronal()`: Decide saltos según la red neuronal.

- **Árbol de Decisión**:

  - `entrenar_decision_tree()`: Entrena el árbol de decisión.
  - `hacer_prediccion_decision_tree()`: Decide saltos según el árbol.


- **Regresión Logística**:

  - `entrenar_logistic_regression()`: Entrena el modelo de regresión logística.
  - `hacer_prediccion_logistic_regression()`: Decide saltos según este modelo.

- hacer_prediccion(): Función unificada que delega a la predicción del modelo seleccionado.

---

## 🎛️ Estructura del Código

### ⚙️ Inicialización
- Configuración de Pygame, dimensiones de pantalla, carga de sprites, y creación de rectángulos (jugador, bala, nave).

### 🔁 Bucle Principal (`main()`)
1. **Manejo de Eventos**: 
   - Teclas (`Espacio` para saltar, `P` para pausa, `Q` para salir).
2. **Modo de Juego**:
   - **Manual**: Guarda datos cada frame.
   - **Automático**:  Se usa el modelo seleccionado (red neuronal, árbol de decisión o regresión logística) para determinar cuándo saltar.
3. **Actualización**: 
   - Movimiento del fondo, animaciones, y renderizado.
   - Reinicio tras colisión y vuelta al menú.

---

## 🖥️ Ejecución
```python
if __name__ == "__main__":
    main()
