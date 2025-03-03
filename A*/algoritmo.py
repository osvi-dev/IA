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
        
        # Imprimir heurística del nodo inicial
        print(f"Nodo inicial {start}: h = {self.heuristic(start, end)}")

        while open_heap:
            current_f, current = heapq.heappop(open_heap)

            if current != start and current != end:
                fila, col = current
                self.board[fila][col].color = (0, 0, 255)  
                self.update_callback()  # Actualizar interfaz
                time.sleep(0.1)
            if current == end:
                self.reconstruir_camino(came_from, end, g_score)  # Pasamos g_score
                return

            if current in self.lista_cerrada:
                continue

            self.lista_cerrada.add(current)

            # Continuar con el proceso normal de A*
            for neighbor_fila, neighbor_col, cost in self.get_vecinos(current):
                neighbor = (neighbor_fila, neighbor_col)
                # detectamos si es el final:
                if neighbor == end:
                    came_from[neighbor] = current
                    g_score[neighbor] = g_score.get(current, 0) + cost  # Asegurar que g_score tenga el valor
                    self.reconstruir_camino(came_from, end, g_score)  # Pasamos g_score
                    return
                
                if neighbor in self.lista_cerrada:
                    continue

                tentative_g = g_score.get(current, float('inf')) + cost

                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    h = self.heuristic(neighbor, end)
                    f = tentative_g + h
                    # Imprimir la heurística para cada nodo evaluado
                    print(f"Nodo {neighbor}: g = {tentative_g}, h = {h}, f = {f}")
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
                new_coor = (new_fila, new_col)  # Corregido: usar tuple() en lugar de tuple
                if new_coor not in self.lista_cerrada:  # Solo agregar si no está en la lista cerrada
                    vecinos.append((new_fila, new_col, cost))
        return vecinos

    def reconstruir_camino(self, came_from:dict, current:tuple, g_score:dict):
        """
        Reconstruye el camino del nodo final al nodo inicial en el
        diccionario came_from y marca los nodos del camino en verde.
        También imprime la heurística de cada nodo en el camino.
        
        :param came_from: El diccionario con los nodos que llevan a cada nodo.
        :type came_from: dict
        :param current: El nodo final
        :type current: tuple
        :param g_score: Diccionario con los valores g para cada nodo
        :type g_score: dict
        """
        path = []
        total_cost = 0
        prev = None
        
        # Recopilar el camino y calcular el costo
        while current in came_from:
            path.append(current)
            if prev is not None:
                # Calcular la distancia entre nodos adyacentes
                if abs(current[0] - prev[0]) + abs(current[1] - prev[1]) == 1:
                    # Movimiento horizontal o vertical (costo 10)
                    total_cost += 10
                else:
                    # Movimiento diagonal (costo 14)
                    total_cost += 14
            prev = current
            current = came_from[current]
        path.append(self.coor_inicio)  # Añadir el nodo inicial
        
        # print("Camino encontrado (desde el final hasta el inicio):", path)
        path.reverse()
        # print("Camino encontrado (desde el inicio hasta el final):", path)
        print(f"Costo total del camino: {total_cost}")
        
        # Imprimir la heurística para cada nodo del camino
        print("\nHeurística para cada nodo del camino:")
        for i, nodo in enumerate(path):
            h = self.heuristic(nodo, self.coor_fin)
            g = g_score.get(nodo, 0)
            f = g + h
            print(f"Paso {i+1}: Nodo {nodo}: g = {g}, h = {h}, f = {f}")

        # Limpiar el tablero
        for fila in self.board:
            for nodo in fila:
                if not nodo.es_inicio() and not nodo.es_fin() and not nodo.es_pared():
                    nodo.color = (255, 255, 255)  # Blanco
        
        # Marcar el camino
        for coor in path:
            fila, col = coor
            nodo = self.board[fila][col]
            if not nodo.es_inicio() and not nodo.es_fin():
                nodo.color = (0, 255, 0)  # Verde

        self.update_callback()  # Actualizamos la interfaz al final