import numpy as np
import time 
class Algoritmo:

    def __init__(self, informacion: dict, board, update_callback):
        """
        Inicializa el objeto Algoritmo.

        :param informacion: Diccionario con las coordenadas de cada nodo y su tipo (inicio, fin, pared)
        :type informacion: dict
        :param board: Tablero de juego
        :type board: list
        :param update_callback: Funcion para actualizar la interfaz grafica
        :type update_callback: function
        :return: None
        """
        self.informacion = informacion
        self.board = board
        self.coor_inicio = None
        self.coor_fin = None
        self.lista_cerrada = set()
        # sera un diccionario porque vamos a guardar la coordenada y el costo
        self.lista_abierta = {}
        # para actualizar la interfaz grafica
        self.update_callback = update_callback
        # para almacenar el padre de cada nodo para reconstruir el camino
        self.parents = {}
        # sera el camino del final
        self.camino = []

        self.nodos_datos = {}
        
    def definir_inicio_fin(self):
        """
        Define las coordenadas de inicio y fin, y agrega las paredes a la lista cerrada.

        :return: None
        """
        for coor, nodo in self.informacion.items():
            if nodo.es_inicio():
                self.coor_inicio = coor
                self.lista_cerrada.add(coor)
            elif nodo.es_fin():
                self.coor_fin = coor
            elif nodo.es_pared():
                self.lista_cerrada.add(coor)
    
    def heuristic(self, a:tuple, b:tuple):
        """
        Calcula la heurística entre dos coordenadas utilizando la distancia de Manhattan.

        :param a: Coordenadas del primer nodo.
        :type a: tuple
        :param b: Coordenadas del segundo nodo.
        :type b: tuple
        :return: La distancia de Manhattan entre las dos coordenadas.
        :rtype: float
        """
        return np.sum(np.abs(np.array(a) - np.array(b)))

    def encontrar_vecinos(self, curr_coor:tuple, datos:tuple):
        """
        Encuentra los vecinos del nodo actual y calcula sus valores g, h y f.

        :param curr_coor: Coordenadas del nodo actual.
        :type curr_coor: tuple
        :param datos: Valores g, h y f del nodo actual.
        :type datos: tuple
        :return: True si encontró el nodo final, False en caso contrario.
        :rtype: bool
        """
        curr_x, curr_y = curr_coor

        # g es el costo de llegar al vecino
        # h es la distancia entre, el vecino y el final
        # f es la suma de g y h

        g, h, f = None, None, None
        
        # El costo de las direcciones sera 10 para mov uni
        direcciones = [
            (+1, 0, 1),    # Derecha 
            (-1, 0, 1),    # Izquierda 
            (0, +1, 1),    # Arriba
            (0, -1, 1),    # Abajo 
            (+1, +1, 1.414),   # Diagonal derecha arriba
            (+1, -1, 1.414),   # Diagonal derecha abajo 
            (-1, +1, 1.414),   # Diagonal izquierda arriba
            (-1, -1, 1.414)    # Diagonal izquierda abajo
        ]
        
        for dx, dy, costo in direcciones:
            next_x, next_y = curr_x + dx, curr_y + dy
            vecino_coor = (next_x, next_y)

            # Comprobamos si las coordenadas son validas y ademas no esten en la lista cerrada
            # la coordenada en x es mayor a 0 y menor a la longitud del tablero
            # la coordenada en y es mayor a 0 y menor a la longitud del tablero
            if (0 <= next_x < len(self.board) and 0 <= next_y < len(self.board[0])) and (vecino_coor not in self.lista_cerrada):
                
                # Verificamos si el vecino es el final
                if vecino_coor == self.coor_fin:
                    # Guardamos el padre del nodo final
                    self.parents[vecino_coor] = curr_coor
                    return True
    
                # Cambiamos el color de la casilla, para saber que es un vecino
                self.board[next_x][next_y].color = (9, 125, 100)

                # guardamos la coordenada
                next_coor = (next_x, next_y)
    
                # Calculamos los nuevos valores
                g = costo + datos[0]
                h = self.heuristic(next_coor, self.coor_fin) 
                f = g + h
                
                # Verificamos que no esté en la lista abierta o si el nuevo camino es mejor
                if next_coor not in self.lista_abierta or g < self.lista_abierta[next_coor][0]:
                    self.lista_abierta[next_coor] = (g, h, f)
                    self.parents[next_coor] = curr_coor
                    
                    # Imprimimos por consola
                print(f"Nodo: {next_coor}, G: {g}, H: {h}, F: {f}")

                self.update_callback()
                time.sleep(0.05)
                
        return False

    def reconstruir_camino(self):
        """
        Reconstruye el camino desde el nodo final hasta el nodo inicial.

        :return: None
        """
        current = self.coor_fin
        path = []
        
        while current != self.coor_inicio:
            path.append(current)
            current = self.parents[current]
            
        path.append(self.coor_inicio)
        path.reverse()  # Para tener el camino desde el inicio hasta el fin
        
        # Guardamos el camino
        self.camino = path
        
        # Pintamos el camino en el tablero
        for node in path:
            if node != self.coor_inicio and node != self.coor_fin:  # No pintar inicio ni fin
                x, y = node
                self.board[x][y].color = (255, 215, 0)  # Color dorado para el camino
                self.update_callback()
                time.sleep(0.1)
                
        # Imprimimos los parámetros del camino
        print("\nCamino encontrado:")
        for i, node in enumerate(path):
            if node in self.nodos_datos:
                g, h, f = self.nodos_datos[node]
                print(f"Paso {i}: {node}, G: {g}, H: {h}, F: {f}")
        
        print(f"Longitud del camino: {len(path)-1}")
        
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
            print("No hay inicio o fin definidos")
            return
        
        self.lista_abierta[self.coor_inicio] = (0, self.heuristic(self.coor_inicio, self.coor_fin), self.heuristic(self.coor_inicio, self.coor_fin))
        
        found_path = False

        while self.lista_abierta:
            # Encontrar la coordenada con menor f
            self.curr_coor = min(self.lista_abierta, key=lambda k: (self.lista_abierta[k][2]))
            
            # Actualizar self.datos con los valores del nodo actual - ESTA ES LA LÍNEA CLAVE QUE FALTA
            self.datos = self.lista_abierta[self.curr_coor]
            
            # Si llegamos al final, terminamos
            if self.curr_coor == self.coor_fin:
                found_path = True
                break
                
            # Eliminarlo de la lista abierta y guardarlo en nodos_datos
            self.nodos_datos[self.curr_coor] = self.datos
            del self.lista_abierta[self.curr_coor]
            
            # Agregamos la coordenada actual a la lista cerrada
            self.lista_cerrada.add(self.curr_coor)
            
            # Cambiar color para mostrar que está en la lista cerrada (explorado)
            if self.curr_coor != self.coor_inicio and self.curr_coor != self.coor_fin:
                x, y = self.curr_coor
                self.board[x][y].color = (200, 0, 0)  # Rojo para nodos explorados
                self.update_callback()
            
            # Buscar vecinos
            if self.encontrar_vecinos(self.curr_coor, self.datos):
                found_path = True
                break
        
        if found_path:
            self.reconstruir_camino()
        else:
            print("No se encontró un camino")