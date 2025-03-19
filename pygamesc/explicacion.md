# Explicación del Código del Juego con Aprendizaje Automático

Este código implementa un juego simple utilizando Pygame, donde un jugador debe esquivar balas disparadas por una nave. Incluye un modo manual y un modo automático que utiliza una red neuronal para decidir cuándo saltar. A continuación, se detalla su estructura y funcionalidad.

## 🔨 Dependencias
- **Pygame**: Para la creación de la interfaz gráfica y manejo de eventos.
- **Random**: Generación de velocidades aleatorias para las balas.
- **Pandas/CSV**: Manejo de datos (comentado en el código).
- **Scikit-learn**: Entrenamiento de una red neuronal (`MLPClassifier`) para el modo automático.

---

## 🎮 Componentes Principales del Juego

### 1. **Elementos Gráficos**
- **Jugador**: Animado con 4 sprites, salta con la tecla `Espacio`.
- **Bala**: Se dispara desde la derecha hacia el jugador.
- **Nave UFO**: Posicionada en la parte derecha de la pantalla.
- **Fondo**: Dos imágenes en movimiento continuo para efecto de desplazamiento.
- **Menú**: Permite seleccionar entre modo manual (`M`), automático (`A`), o salir (`Q`).

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
   - **Algoritmo**: `MLPClassifier` (Perceptrón Multicapa).
   - **Preprocesamiento**: Normalización con `StandardScaler`.
   - **División de Datos**: 80% entrenamiento, 20% prueba.
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
- `entrenar_modelo()`: Entrena la red neuronal con los datos recolectados.
- `hacer_prediccion()`: Devuelve `True`/`False` según la decisión del modelo.

---

## 🎛️ Estructura del Código

### ⚙️ Inicialización
- Configuración de Pygame, dimensiones de pantalla, carga de sprites, y creación de rectángulos (jugador, bala, nave).

### 🔁 Bucle Principal (`main()`)
1. **Manejo de Eventos**: 
   - Teclas (`Espacio` para saltar, `P` para pausa, `Q` para salir).
2. **Modo de Juego**:
   - **Manual**: Guarda datos cada frame.
   - **Automático**: Usa el modelo para saltar.
3. **Actualización**: 
   - Movimiento del fondo, animaciones, y renderizado.
   - Reinicio tras colisión o activación del menú.

---

## 🖥️ Ejecución
```python
if __name__ == "__main__":
    main()