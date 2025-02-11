import pygame
import algoritmo
# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)

# definimos la lista abierta y cerrada

# en este diccionario vamos a guardar las coordenadas para hacer referencia 
# a los nodos inicio o fin, ademas de las paredes.
nodos = {}

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))
    
    def __str__(self):
        return f"(x: {self.fila}, y: {self.col}, color: {self.color})"
    
def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    """
    Obtiene la posición del click en la cuadrícula.
    :param pos: La posición del click en pixeles.
    :type pos: tuple
    :param filas: El número de filas en la cuadrícula.
    :type filas: int
    :param ancho: El ancho del área de dibujo.
    :type ancho: int
    :return: La fila y columna del nodo en la cuadrícula.
    :rtype: tuple
    """
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col
    
def ver_nodos():
    """
    Imprime todos los nodos que se han definido en la cuadrícula actual.
    """
    for cor, aux_nodo in nodos.items():
        print(aux_nodo)
    print("\n")

# TODO: tengo de definir un metodo para avanzar y calcular 
# g, f, y h para cada salto ademas del apuntador de donde brinque
def main(ventana, ancho):
    FILAS = 5
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()
                    # agregamos la coordenada del inicio al diccionario
                    nodos[(fila, col)] = inicio
                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()
                    # agregamos la coordenada del fin al diccionario
                    nodos[(fila, col)] = fin

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()
                    # agregamos la coordenada del muro al diccionario
                    nodos[(fila, col)] = nodo

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()

                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None
                # verificamos si las coordenadas ya existen en el diccionario
                # si existen las eliminamos
                if (fila, col) in nodos:    
                    nodos.pop((fila, col))
            # Una vez definido el inicio, el fin y los muros podemos apretar
            # la letra b para buscar el camino mas corto
            elif pygame.key.get_pressed()[pygame.K_b]:
                algorit = algoritmo.Algoritmo(nodos, grid)
                algorit.imprimir()
                

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)

# TODO: 
# 1. Definir el algoritmo A*
