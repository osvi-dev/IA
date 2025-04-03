# Evalución Redes Neuronales Mediapipe

Nombre: José Osvaldo Constantino Bautista  
Modelar una red neuronal que pueda identificar emociones a través los valores obtenidos de los landmarks que genera mediapipe.  

- Definir el tipo de red neuronal y describir cada una de sus partes
    - Utilizaria redes neuronales multicapa.  
    Las partes de la red neuronal son:
        + Capas de entrada
        + Capas ocultas o intermedias
        + Capa o capas de salida
        + Pesos
        + Bias
        + funcion / funciones de activacion.

- Definir los patrones a utilizar
    - Ya que hemos elegido una red neuronal multicapa porque nos enfocaremos en varios puntos debido a los landmarks, me centraria en hacer un dataset donde recopile los puntos clave para las emociones que quiero detectar, un ejemplo: (61, 29) que hacen referencia a la boca ademas de los puntos:  (13,14) pertenecen al labio inferior y el labio superior en la parte central. los intentaria trackear con sus coordenadas para que lo pueda detectar en diferentes angulos, posiciones, etc. Así podriamos detectar si la persona esta feliz para este caso.   
    Serian asi para las emociones que queremos detectar.

- Definir función de activación es necesaria para este problema  
    + Relu
- ¿Que valores a la salida de la red se podrian esperar?
    - Los valores de salida se podrian esperar es la probabilidad de que sea X emocion, pero si hablamos un valor en concreto, no se sabe.

- Cuales son los valores máximos que puede tener el bias?
    - No se sabe el valor máximo que puede obtener el bias.
