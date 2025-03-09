import numpy as np
import time 
class Algoritmo:

    def __init__(self, informacion: dict, board, update_callback):
        self.informacion = informacion
        self.board = board
        self.coor_inicio = None
        self.coor_fin = None
        self.lista_cerrada = set()
        # sera un diccionario porque vamos a guardar la coordenada y el costo
        self.lista_abierta = {}
        # para actualizar la interfaz grafica
        self.update_callback = update_callback

    def definir_inicio_fin(self):
        """
        Define las coordenadas de inicio y fin, y agrega las paredes a la lista cerrada.

        :return: None
        """
        for coor, nodo in self.informacion.items():
            if nodo.es_inicio():
                self.coor_inicio = coor
            elif nodo.es_fin():
                self.coor_fin = coor
            elif nodo.es_pared():
                self.lista_cerrada.add(coor)
    
    def heuristic(self, a:tuple, b:tuple):
        """
        Calcula la distancia entre dos nodos utilizando la distancia
        Euclideana.

        :param a: Las coordenadas del nodo 1.
        :type a: tuple
        :param b: Las coordenadas del nodo 2.
        :type b: tuple
        :return: La distancia entre los dos nodos.
        :rtype: float
        """
        return np.linalg.norm(np.array(a) - np.array(b))

    def encontrar_vecinos(self, curr_coor):
        curr_x, curr_y = curr_coor

        # g es el costo de llegar al vecino
        # h es la distancia entre, el vecino y el final
        # f es la suma de g y h

        g, h, f = None
        
        # El costo de las direcciones sera 10 para mov uni
        direcciones = [
            (+1, 0, 10),    # Arriba
            (-1, 0, 10),    # Abajo
            (0, +1, 10),    # Derecha
            (0, -1, 10),    # Izquierda
            (+1, +1, 14),   # Diagonal arriba derecha
            (+1, -1, 14),   # Diagonal abajo derecha
            (-1, +1, 14),   # Diagonal arriba izquierda
            (-1, -1, 14)    # Diagonal abajo izquierda
        ]
        
        for dx, dy, costo in direcciones:
            next_x, next_y = curr_x + dx, curr_y + dy
            # Comprobamos si las coordenadas son validas y ademas no esten en la lista cerrada
            # la coordenada en x es mayor a 0 y menor a la longitud del tablero
            # la coordenada en y es mayor a 0 y menor a la longitud del tablero
            if (0 <= next_x < len(self.board) and 0 <= next_y < len(self.board[0])) and ((next_x, next_y) not in self.lista_cerrada):
                
                # Camibamos el color de la casilla, para saber que es un vecino
                self.board[next_x][next_y] = (0, 0, 100)
                time.sleep(0.1)
                # Verificamos el vecino es el final
                if (next_x, next_y) == self.coor_fin:
                    # construimos el final
                    return 
            # guardamos la coordenada
            next_coor = (next_x, next_y)
            # verificamos que no este en la lista abierta, si esta veremos si volvemos a calcular f,g,h 
            if next_coor not in self.lista_abierta:
                g = costo
                h = self.heuristic(next_coor, self.coor_fin)
                f = g + h
                self.lista_abierta[next_coor] = (g, h, f)
            
            self.update_callback

    def resolver(self):
        """
        Resuelve el problema de encontrar el camino más corto en un tablero
        desde un nodo inicial hasta un nodo final utilizando el algoritmo A*.

        El método define los nodos inicial y final, y utiliza una cola de
        prioridad para expandir los nodos más prometedores, calculando los
        valores de g, h y f para cada nodo. Si se encuentra un camino al
        nodo final, este se reconstruye y se marca en el tablero. En caso
        contrario, informa que no se encontró un camino.

        :raises ValueError: Si no existe un nodo de inicio o fin definido.
        """

        self.definir_inicio_fin()
        if self.coor_inicio is None or self.coor_fin is None:
            return  # No hay inicio o fin

        self.encontrar_vecinos(self.coor_inicio)
        