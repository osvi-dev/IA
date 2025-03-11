import pygame
import os

# Configuraciones iniciales
ANCHO_VENTANA = 600
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos (Instrucciones en la terminal)")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
GRIS_CLARO = (192, 192, 192)  # Simboliza los nodos en la Lista Abierta (LA)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
ROJO = (255, 0, 0)  # Indica el nodo seleccionado para avanzar

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        
        # Atributos para el algoritmo A*
        self.G = 0  # Costo desde el inicio hasta el nodo actual
        self.H = 0  # Estimación del costo hasta el nodo final
        self.F = 0  # Costo total (F = G + H)
        self.padre = 0 # Nodo anterior para que al final se marque la ruta mas corta

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def es_gris(self):
        return self.color == GRIS_CLARO

    def es_rojo(self):
        return self.color == ROJO

    def restablecer(self):
        self.color = BLANCO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_gris(self):
        if not self.es_inicio():  # Asegurar que el nodo inicio no cambie de color
            self.color = GRIS_CLARO

    def hacer_rojo(self):
        self.color = ROJO

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

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
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

print("\nBienvenido al algoritmo A* para encontrar la ruta más corta.")
print("Instrucciones:")
print("- Haga clic izquierdo para seleccionar el nodo inicio y fin.")
print("- Despues Haga clic izquierdo en un nodo para marcarlo como pared.")
print("- Haga clic derecho para eliminar un nodo.")
print("- Presione 'S' para iniciar a marcar las posibles rutas.")

def limpiar_terminal():
    """Limpia la terminal dependiendo del sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
def imprimir_estado(LA, LC, inicio, fin):
    """Imprime el estado actual de la Lista Abierta, Lista Cerrada, Nodo Inicio y Nodo Fin."""
    limpiar_terminal()
    print("Instrucciones:")
    print("- Presione 'D' para encontrar ruta paso por paso.")
    print("- Presione 'F' para finalizar y encontrar la ruta más corta.")
    print("\nEstado actual:")
    print("Lista Abierta (LA):", [(nodo.get_pos()) for nodo in LA])
    print("Lista Cerrada (LC):", [(nodo.get_pos()) for nodo in LC])
    print("Nodo Inicio:", inicio.get_pos() if inicio else "No definido")
    print("Nodo Fin:", fin.get_pos() if fin else "No definido")
    

def calcular_heuristica(nodo, fin):
    """ Calcula el valor H basado en la distancia en celdas al nodo fin. """
    if not fin:
        return 0
    fila_actual, col_actual = nodo.get_pos()
    fila_fin, col_fin = fin.get_pos()

    distancia_filas = abs(fila_fin - fila_actual)
    distancia_columnas = abs(col_fin - col_actual)

    return (distancia_filas + distancia_columnas) * 10

def marcar_nodos_adyacentes(grid, nodo_actual, fin, LA, LC, FILAS):
    """ Marca los nodos adyacentes en gris y actualiza sus valores G, H y F. """
    fila, col = nodo_actual.get_pos()
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Incluye diagonales

    for d in direcciones:
        nueva_fila = fila + d[0]
        nueva_col = col + d[1]

        if 0 <= nueva_fila < FILAS and 0 <= nueva_col < FILAS:
            nodo_adyacente = grid[nueva_fila][nueva_col]

            if nodo_adyacente.es_pared() or nodo_adyacente in LC:
                continue  # No procesar si es una pared o ya está en la lista cerrada
            
            # Determinar el costo de movimiento (10 si es ortogonal, 14 si es diagonal)
            costo_movimiento = 10 if d in [(-1, 0), (1, 0), (0, -1), (0, 1)] else 14
            nuevo_G = nodo_actual.G + costo_movimiento

            if nodo_adyacente in LA:
                # Si el nuevo G es menor, actualizamos el nodo
                if nuevo_G <= nodo_adyacente.G:
                    nodo_adyacente.G = nuevo_G
                    nodo_adyacente.F = nodo_adyacente.G + nodo_adyacente.H
                    nodo_adyacente.padre = nodo_actual  # Actualizar el nodo padre
                    
            else:
                # Si es la primera vez que se calcula, establecer valores
                nodo_adyacente.G = nuevo_G
                nodo_adyacente.H = calcular_heuristica(nodo_adyacente, fin)
                nodo_adyacente.F = nodo_adyacente.G + nodo_adyacente.H
                nodo_adyacente.hacer_gris()
                nodo_adyacente.padre = nodo_actual  # Asignar el nodo padre
                LA.append(nodo_adyacente)

def marcar_ruta_optima(nodo_fin):
    """ Retrocede desde el nodo final hasta el inicio para marcar la ruta óptima. """
    nodo_actual = nodo_fin.padre
    while nodo_actual and not nodo_actual.es_inicio():
        nodo_actual.color = (0, 0, 255)  # Azul para la ruta óptima
        nodo_actual = nodo_actual.padre

def avanzar_nodo(LA, LC, fin):
    """ Encuentra el nodo con el menor F y lo marca en rojo. """
    if not LA:
        print("\nNo hay más nodos en la lista abierta. No se encontró el camino.")
        return None

    menor_nodo = min(LA, key=lambda nodo: nodo.F)  # Encuentra el nodo con el menor F
    
    if menor_nodo == fin:
        print("\nllegamos al nodo final!!! No se pueden seleccionar más nodos.")
        return None  # Detiene la búsqueda si se llega al nodo final

    menor_nodo.hacer_rojo()  # Marca el nodo como seleccionado (rojo)
    LA.remove(menor_nodo)  # Lo eliminamos de la lista abierta
    LC.append(menor_nodo)  # Lo agregamos a la lista cerrada

    return menor_nodo

def ejecutar_algoritmo_completo(grid, inicio, fin, LA, LC, LS, FILAS):
    """ Ejecuta el algoritmo A* completo y muestra los resultados en consola. """
    while True:
        nuevo_nodo = avanzar_nodo(LA, LC, fin)
        if not nuevo_nodo:
            break
        marcar_nodos_adyacentes(grid, nuevo_nodo, fin, LA, LC, FILAS)
        imprimir_estado(LA, LC, inicio, fin)  # Actualiza la consola en cada paso
    
    if fin in LC:
        marcar_ruta_optima(fin)
    
    imprimir_estado(LA, LC, inicio, fin)
    print("\n¡Se ha llegado al nodo fin!")
    nodo_actual = fin
    while nodo_actual and nodo_actual.padre:
        LS.append(nodo_actual.get_pos())
        nodo_actual = nodo_actual.padre
    print("Ruta óptima (Presione 'C' para trazarla):", LS[::-1])  # Imprimir la ruta en orden inverso

def main(ventana, ancho):
    FILAS = 10
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None
    LA = []  # Lista Abierta
    LC = []  # Lista Cerrada
    LS = [] # Lista para almacenar la ruta mas corta

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
                    inicio.G = 0
                    inicio.padre = None  # El inicio no tiene padre
                    LC.append(inicio)  # Agregamos el nodo inicio a la lista cerrada

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()
                    
            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    imprimir_estado(LA, LC, inicio, fin)
                    marcar_nodos_adyacentes(grid, inicio, fin, LA, LC, FILAS)

                if event.key == pygame.K_d:
                    nuevo_nodo = avanzar_nodo(LA, LC, fin)
                    if nuevo_nodo:
                        marcar_nodos_adyacentes(grid, nuevo_nodo, fin, LA, LC, FILAS)
                    imprimir_estado(LA, LC, inicio, fin)
                    if nuevo_nodo == fin:
                        print("\n¡Se ha llegado al nodo fin!")

                if event.key == pygame.K_c and fin:
                    marcar_ruta_optima(fin)
                
                if event.key == pygame.K_f and inicio and fin:
                    ejecutar_algoritmo_completo(grid, inicio, fin, LA, LC, LS, FILAS)
                

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)