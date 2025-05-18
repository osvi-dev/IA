# Documentación del Juego con Aprendizaje Automático

Este código implementa un juego simple utilizando Pygame, donde un jugador debe esquivar balas disparadas por naves espaciales. El juego integra algoritmos de machine learning para el modo automático en el que la IA controla al jugador. A continuación, se detalla su estructura y funcionalidad.

## 🔨 Dependencias
- **Pygame**: Para la creación de la interfaz gráfica y manejo de eventos.
- **Random**: Generación de velocidades aleatorias para las balas.
- **Pandas**: Manejo de datos (importado pero no utilizado activamente).
- **Scikit-learn**: Implementación de tres algoritmos de aprendizaje automático:
  - `MLPClassifier`: Red neuronal para modo automático.
  - `DecisionTreeClassifier`: Árbol de decisión para modo automático.
  - `KNeighborsClassifier`: K-Vecinos más cercanos para modo automático.

---

## 🎮 Componentes Principales del Juego

### 1. **Elementos Gráficos**
- **Jugador**: Animado con 4 sprites, puede:
  - Saltar con la tecla `Espacio`
  - Moverse lateralmente con las teclas `←` y `→`
- **Balas**: 
  - Bala horizontal: Se dispara desde la derecha hacia el jugador.
  - Bala vertical: Se dispara desde arriba hacia abajo.
- **Naves UFO**: 
  - Una posicionada en la parte derecha de la pantalla.
  - Otra posicionada en la parte superior.
- **Fondo**: Dos imágenes en movimiento continuo para efecto de desplazamiento.
- **Menú**: Permite seleccionar entre:
  - Modo manual (`M`)
  - Red Neuronal (`N`) para modo automático
  - Árbol de Decisión (`A`) para modo automático
  - K-Vecinos más cercanos (`K`) para modo automático
  - Salir (`Q`)

### 2. **Mecánicas del Juego**
- **Salto**: Controlado por gravedad y velocidad inicial.
- **Movimiento Lateral**: El jugador puede moverse a la izquierda o derecha para esquivar.
- **Colisiones**: Si cualquier bala impacta al jugador, el juego se reinicia.
- **Modo Pausa**: Tecla `P` detiene/reanuda el juego.
- **Fondo en Movimiento**: Crea la ilusión de avance continuo.

---

## 🤖 Integración con Machine Learning

### 🔄 Flujo de Datos
1. **Recolección de Datos (Modo Manual)**:
   - **Características**: 
     - Velocidad de la bala horizontal
     - Distancia X entre jugador y bala horizontal
     - Distancia Y entre jugador y bala vertical
     - Estado de movimiento lateral (izquierda/derecha)
     - Estado de salto
   - **Targets**: 
     - `salto_hecho`: 1 si el jugador saltó, 0 si no.
     - `izquierda`: 1 si se mueve a la izquierda, 0 si no.
     - `derecha`: 1 si se mueve a la derecha, 0 si no.
   - Almacenamiento en `datos_modelo`.

2. **Entrenamiento del Modelo**:
   - **Preprocesamiento**: Normalización con `StandardScaler` para los modelos de red neuronal.
   - **División de Datos**: 80% entrenamiento, 20% prueba.
   - **Algoritmos disponibles**:
     - `Red Neuronal (MLPClassifier)`: Perceptrón multicapa con una capa oculta de 10 neuronas.
     - `Árbol de Decisión (DecisionTreeClassifier)`: Modelo basado en reglas para clasificación.
     - `K-Vecinos más cercanos (KNeighborsClassifier)`: Clasificación basada en los 5 vecinos más cercanos.
   - **Precisión**: Evaluada con `accuracy_score`.

3. **Predicción (Modo Automático)**:
   - Para cada acción (salto, movimiento izquierda, movimiento derecha), se usa el modelo correspondiente para decidir la acción a tomar en función de:
     - Velocidad actual de la bala horizontal
     - Distancia X entre jugador y bala horizontal
     - Distancia Y entre jugador y bala vertical
     - Estado actual del jugador

---

## 📝 Funciones Clave

### 🕹️ Funciones del Juego
- `manejar_salto()`: Controla la física del salto (gravedad y posición).
- `manejar_movimiento_lateral()`: Permite el desplazamiento lateral del jugador.
- `disparar_bala()` y `disparar_bala2()`: Inician el movimiento de las balas.
- `update()`: Actualiza posiciones, animaciones y detecta colisiones.
- `guardar_datos()`: Almacena datos en modo manual para entrenamiento.

### 🧠 Funciones de Procesamiento de Datos
- `split_data_x()`: Divide los datos para entrenar el modelo de salto.
- `split_data_izquierda()`: Divide los datos para entrenar el modelo de movimiento izquierda.
- `split_data_derecha()`: Divide los datos para entrenar el modelo de movimiento derecha.

### 🧠 Funciones de Entrenamiento
- **Red Neuronal**:
  - `entrenar_red_neuronal()`: Entrena el modelo para salto.
  - `entrenar_red_neuronal_izquierda()`: Entrena el modelo para movimiento izquierda.
  - `entrenar_red_neuronal_derecha()`: Entrena el modelo para movimiento derecha.

- **Árbol de Decisión**:
  - `entrenar_decision_tree()`: Entrena el modelo para salto.
  - `entrenar_decision_tree_izquierda()`: Entrena el modelo para movimiento izquierda.
  - `entrenar_decision_tree_derecha()`: Entrena el modelo para movimiento derecha.

- **K-Vecinos**:
  - `entrenar_knn()`: Entrena el modelo para salto.
  - `entrenar_knn_izquierda()`: Entrena el modelo para movimiento izquierda.
  - `entrenar_knn_derecha()`: Entrena el modelo para movimiento derecha.

### 🧠 Funciones de Predicción
- `hacer_prediccion()`: Función unificada que delega la predicción de salto al modelo seleccionado.
- `hacer_prediccion_izquierda()`: Función unificada para predicción de movimiento izquierda.
- `hacer_prediccion_derecha()`: Función unificada para predicción de movimiento derecha.

### 🎛️ Funciones de Control del Juego
- `mostrar_menu()`: Interfaz para seleccionar el modo de juego.
- `pausa_juego()`: Controla la pausa/reanudación del juego.
- `reiniciar_juego()`: Resetea las posiciones tras colisión y muestra el menú.
- `main()`: Función principal que ejecuta el bucle del juego.

---

## 🎛️ Estructura del Código

### ⚙️ Inicialización
- Configuración de Pygame, dimensiones de pantalla, carga de sprites, y creación de rectángulos (jugador, balas, naves).
- Definición de modelos de machine learning (Red neuronal, Árbol de decisión, K-Vecinos).
- Inicialización de variables de control para salto, movimiento y estado del juego.

### 🔁 Bucle Principal (`main()`)
1. **Manejo de Eventos**: 
   - Teclas (`Espacio` para saltar, `←→` para movimiento lateral, `P` para pausa, `Q` para salir).
2. **Modos de Juego**:
   - **Manual**: El jugador controla el personaje y se guardan datos para entrenar los modelos.
   - **Automático**: Se usan los modelos entrenados para decidir:
     - Cuándo saltar
     - Cuándo moverse a la izquierda
     - Cuándo moverse a la derecha
3. **Actualización**: 
   - Movimiento del fondo, animaciones, y renderizado.
   - Manejo de colisiones y reinicio del juego.

---

## 🖥️ Ejecución
```python
if __name__ == "__main__":
    main()
```

## 🔄 Flujo del Juego
1. El juego comienza mostrando un menú para seleccionar modo de juego.
2. En modo manual:
   - El jugador controla el personaje usando el teclado.
   - Se recopilan datos de cada frame para entrenar los modelos.
3. En modo automático:
   - Se entrena un modelo separado para cada acción (salto, izquierda, derecha).
   - El modelo seleccionado (Red neuronal, Árbol o KNN) toma decisiones basadas en las condiciones actuales.
4. Si ocurre una colisión, el juego se reinicia y muestra el menú nuevamente.
