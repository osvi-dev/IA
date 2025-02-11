class Algoritmo():

    def __init__(self, informacion:dict, board):
        self.informacion = informacion
        self.board = board

    def imprimir(self):
        print(self.informacion)
        
class NodoExtendido():
    def __init__(self, nodo,  g:int, h:int, f:int, padre):
        pass
