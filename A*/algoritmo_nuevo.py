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
        # sera el camino del final
        self.camino = {}
        
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

    def encontrar_vecinos(self, curr_coor:tuple, datos:tuple):
        curr_x, curr_y = curr_coor

        # g es el costo de llegar al vecino
        # h es la distancia entre, el vecino y el final
        # f es la suma de g y h

        g, h, f = None, None, None
        
        # El costo de las direcciones sera 10 para mov uni
        direcciones = [
            (+1, 0, 10),    # Derecha 
            (-1, 0, 10),    # Izquierda 
            (0, +1, 10),    # Arriba
            (0, -1, 10),    # Abajo 
            (+1, +1, 14),   # Diagonal derecha arriba
            (+1, -1, 14),   # Diagonal derecha abajo 
            (-1, +1, 14),   # Diagonal izquierda arriba
            (-1, -1, 14)    # Diagonal izquierda abajo
        ]
        
        for dx, dy, costo in direcciones:
            next_x, next_y = curr_x + dx, curr_y + dy
            vecino_coor = (next_x, next_y)

            # Comprobamos si las coordenadas son validas y ademas no esten en la lista cerrada
            # la coordenada en x es mayor a 0 y menor a la longitud del tablero
            # la coordenada en y es mayor a 0 y menor a la longitud del tablero
            if (0 <= next_x < len(self.board) and 0 <= next_y < len(self.board[0])) and (vecino_coor not in self.lista_cerrada):
                

                # Verificamos el vecino es el final
                if (next_x, next_y) == self.coor_fin:
                    # construimos el final
                    print("Encontramos el camino")
                    time.sleep(10)
                    return 
    
                # Cambiamos el color de la casilla, para saber que es un vecino
                self.board[next_x][next_y].color = (9, 125, 100)
                time.sleep(0.1)

                # guardamos la coordenada
                next_coor = (next_x, next_y)
    
                # verificamos que no este en la lista abierta, si esta veremos si volvemos a calcular f,g,h 
                if next_coor not in self.lista_abierta:
                    g = costo + datos[0]
                    h = self.heuristic(next_coor, self.coor_fin) 
                    f = g + h
                    self.lista_abierta[next_coor] = (g, h, f)

                    # primimimos por consola
                    print(f"Nodo: {next_coor}, G: {g}, H: {h}, F: {f}")
                
                # lista en la lista abierta
                else:
                    g = costo + datos[0]
                    h = self.heuristic(next_coor, self.coor_fin) 
                    f = g + h
                    if g < self.lista_abierta[next_coor][0]:
                        self.lista_abierta[next_coor] = (g, h, f)

                self.update_callback()

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
        
        # dimensiones = (len(self.board), len(self.board[0]))
        # print(f'Las dimensiones del tablero son: {dimensiones}')
        self.curr_coor = self.coor_inicio   
        self.datos = (0,0,0)

        while self.curr_coor != self.coor_fin:
            self.encontrar_vecinos(self.curr_coor, self.datos)
            
            # print(f'Lista abierta: {self.lista_abierta}')

            # En lugar de cambiar self.lista_abierta a una lista, obtenemos el nodo con la f más baja
            if not self.lista_abierta:  # Verificar si la lista está vacía
                print("No se encontró un camino")
                break
                
            # Encontrar la coordenada con menor f
            next_coor = min(self.lista_abierta, key=lambda k: self.lista_abierta[k][2])
            self.datos = self.lista_abierta[next_coor]
            
            # Eliminarlo de la lista abierta
            del self.lista_abierta[next_coor]
            
            self.curr_coor = next_coor
            
            # Agregamos la coordenada actual a la lista cerrada
            self.lista_cerrada.add(self.curr_coor)

            print(f'f mas pequena: {next_coor} datos {self.datos}')