import heapq
import numpy as np
import time 
class Algoritmo:

    def __init__(self, informacion: dict, board, update_callback):
        self.informacion = informacion
        self.board = board
        self.coor_inicio = None
        self.coor_fin = None
        self.lista_cerrada = set()
        # para actualizar la interfaz grafica
        self.update_callback = update_callback

    def definir_inicio_fin(self):
        for coor, nodo in self.informacion.items():
            if nodo.es_inicio():
                self.coor_inicio = coor
            elif nodo.es_fin():
                self.coor_fin = coor
            elif nodo.es_pared():
                self.lista_cerrada.add(coor)

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

        start = self.coor_inicio
        end = self.coor_fin

        open_heap = []
        heapq.heappush(open_heap, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, end)}

        while open_heap:
            current_f, current = heapq.heappop(open_heap)

            if current != start and current != end:
                fila, col = current
                self.board[fila][col].color = (0, 0, 255)  # Azul
                self.update_callback()  # Actualizar interfaz
                time.sleep(0.1)
            if current == end:
                self.reconstruir_camino(came_from, end)
                return

            if current in self.lista_cerrada:
                continue

            self.lista_cerrada.add(current)

            for neighbor_fila, neighbor_col, cost in self.get_vecinos(current):
                neighbor = (neighbor_fila, neighbor_col)
                if neighbor in self.lista_cerrada:
                    continue

                tentative_g = g_score.get(current, float('inf')) + cost

                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self.heuristic(neighbor, end)
                    heapq.heappush(open_heap, (f, neighbor))
                    f_score[neighbor] = f

        print("No se encontró un camino")

    def heuristic(self, a:tuple, b:tuple):
        # Distancia Euclideana
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

    def get_vecinos(self, coor:tuple) -> list:
        """
        Obtiene los vecinos válidos de una celda en la cuadrícula.
        
        :param coor: Las coordenadas de la celda actual.
        :type coor: tuple
        :return: Una lista con las coordenadas de los vecinos válidos.
        :rtype: list
        """
        fila, col = coor
        vecinos = []
        directions = [
            (-1, 0, 10), (1, 0, 10), (0, -1, 10), (0, 1, 10), # Arriba, abajo, izquierda, derecha
            (-1, -1, 14), (-1, 1, 14), (1, -1, 14), (1, 1, 14) # diagonales
            ]  
        
        for df, dc, cost in directions:
            new_fila = fila + df
            new_col = col + dc
            if 0 <= new_fila < len(self.board) and 0 <= new_col < len(self.board[0]):
                vecinos.append((new_fila, new_col, cost))
        return vecinos

    def reconstruir_camino(self, came_from:dict, current:dict):
        """
        Reconstruye el camino del nodo final al nodo inicial en el
        diccionario came_from y marca los nodos del camino en verde.
        
        :param came_from: El diccionario con los nodos que llevan a cada nodo.
        :type came_from: dict
        :param current: El nodo final
        :type current: tuple
        """
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(self.coor_inicio)  # Añadir el nodo inicial
        print(path)
        path.reverse()
        print(path)

        for fila in self.board:
            for nodo in fila:
                if not nodo.es_inicio() and not nodo.es_fin() and not nodo.es_pared():
                    nodo.color = (255, 255, 255)  # Blanco
                    
        for coor in path:
            fila, col = coor
            nodo = self.board[fila][col]
            if not nodo.es_inicio() and not nodo.es_fin():
                nodo.color = (0, 255, 0)

        self.update_callback