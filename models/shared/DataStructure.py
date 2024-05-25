# [DataStructure.py]
from queue import Queue
import json
import copy
import random
from ..GameModel import GameModel

debug = False


def print_debug(message):
    new_message = "[DataStructure.py]: " + message
    if debug:
        print(new_message)


class Operador:
    def __init__(self, nombre: str, dx: int, dy: int) -> None:
        """
        Inicializa un operador

        Args:
            nombre (str): El nombre del operador.
            dx (int): El cambio de coordenada en x.
            dy (int): El cambio de coordenada en y.

        Returns:
            None
        """
        self.nombre = nombre
        self.dx = dx  # Cambio en x
        self.dy = dy  # Cambio en y

    def get_nombre(self) -> str:
        return self.nombre

    def get_dx(self) -> int:
        return self.dx

    def get_dy(self) -> int:
        return self.dy

    def __str__(self) -> str:
        return self.nombre


class Estado:
    def __init__(self, x: int, y: int):
        """
        Inicializa un estado.

        Args:
            x (int): La coordenada en x.
            y (int): La coordenada en y.

        Returns:
            None
        """
        self.x = x
        self.y = y

    def get_coordenadas(self):
        return [self.x, self.y]       

    def __str__(self) -> str:
        """
        Muestra informacion sobre las coordenadas.

        Args:
            None

        Returns:
            Las coordenadas en string.
        """
        a_string = "{} {} {}".format(
            str(self.x), str(self.y))
        return a_string

class Problema:
    def __init__(self, estado_inicial: Estado, jugador1: str, jugador2: str, tablero):
        """
        Inicializa un nuevo problema

        Args:
            estado_inicial (Estado): El estado actual del problema.
            matriz (): La matriz que representa el ambiente.


        Returns:
            Las coordenadas en string.
        """
        self.estado_inicial = estado_inicial
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.tablero = tablero

    def __str__(self) -> str:
        mensaje = "Estado inicial: {} -> Estado objetivo: {1}".format(
            self.estado_inicial, self.jugador1, self.jugador2, self.tablero)
        return mensaje

    def get_estado_inicial(self) -> Estado:
        return self.estado_inicial
    
    def get_jugador1(self) -> str:
        return self.jugador1
    
    def get_jugador2(self) -> str:
        return self.jugador2
    
    def get_tablero(self):
        return self.tablero
    
    def movimientos_jugador(estado: Estado):
        return GameModel.generateHorseMoves(estado)
    
    def nuevo_estado(self, estado: Estado) -> Estado:
        return random.choice(self.movimientos_jugador(estado))
    
    def es_estado_objetivo(self, estado: Estado):
        if self.movimientos_jugador(estado) == []:
            return True
        else:
            return False
        
    def utilidad(estado: Estado) -> int:
        """
        Evalúa un estado y devuelve un valor numérico que representa 
        qué tan bueno es ese estado para el jugador.

        Args:
            estado (Estado): El estado a evaluar.

        Returns:
            int: Valor numérico de la evaluación del estado.
        """   
        x, y = estado.get_coordenadas()
        return x + y


    '''    def resultado(self, estado: Estado, operador: Operador) -> Estado:
        """
        Genera un nuevo estado aplicando un operador sobre el actual.

        Args:
            estado (Estado): El estado actual.
            operador (Operador): El operador que se quiere aplicar al estado.

        Returns:
            nuevo_estado (Estado): Un nuevo estado que surge de aplicar el operador al estado actual.
            None si el nuevo estado no cumple con las reglas de juego.
        """
        nuevo_estado = Estado(estado.x + operador.dx, estado.y + operador.dy)
        if self.es_estado_valido(nuevo_estado):
            return nuevo_estado
        else:
            return None'''


class Nodo:
    """
    Clase que representa un nodo en un árbol de búsqueda.

    Cada nodo del árbol guarda la siguiente información:
    - El estado del problema
    - Una referencia al nodo padre
    - El operador que se aplicó para generar el nodo
    - Profundidad del nodo
    - El costo de la ruta desde la raíz hasta el nodo
    """

    def __init__(self, problema: Problema):
        """
        Inicializa un nuevo nodo raiz.

        Args:
            problema (Problema): El problema

        Atributos internos (get):
        - estado: El estado del problema.
        - padre: Una referencia al nodo padre.
        - operador: El operador que se aplicó para generar el nodo.
        - profundidad: La profundidad del nodo en el árbol.
        - costo_acumulado: El costo acumulado de la ruta desde la raíz hasta el nodo.
        """
        self.problema: Problema = problema
        self.padre: Nodo = None
        self.operador: Operador = None
        self.profundidad: int = 0
        self.costo_acumulado: int = 0

    def __str__(self) -> str:
        padre = None
        if self.padre != None:
            padre = self.padre.get_estado()
        mensaje = "Estado: {}, padre: {}, operador efectuado: {}, profundidad: {}, costo acumulado: {}".format(
            str(self.problema.get_estado_inicial()), str(padre), str(self.operador), str(self.profundidad), str(self.costo_acumulado))
        return mensaje

    def get_problema(self):
        return self.problema

    def set_problema(self, problema: Problema):
        self.problema = problema

    def get_estado(self):
        return self.problema.estado_inicial

    def get_padre(self):
        return self.padre

    def set_padre(self, padre: "Nodo"):
        self.padre = padre

    def get_operador(self):
        return self.operador

    def set_operador(self, operador: Operador):
        self.operador = operador

    def get_profundidad(self):
        return self.profundidad

    def set_profundidad(self, profundidad: int):
        self.profundidad = profundidad

    def get_costo_acumulado(self):
        return self.costo_acumulado

    def set_costo_acumulado(self, costo_acumulado: int):
        self.costo_acumulado = costo_acumulado

    def calcular_heuristica(self):
        return 0

    def expandir(self):
        # esto no se si se utilizara
        """
        Expande el nodo actual

        Args:
            Ninguno.

        Returns:
            list[Nodo]: Donde list[Nodo] corresponde a los hijos.
        """
        # Limpiar hijos por si las moscas
        self.hijos = []

        #operadores = self.problema.generar_operadores()

        #if len(operadores) == 0:
            #return self.hijos

        '''        for operador in operadores:
            # === Creacion y configuracion del nuevo estado ===
            # Creo un nuevo estado despues de aplicar el operador
            nuevo_estado = self.problema.resultado(
                self.problema.estado_inicial, operador)
            nuevo_estado.en_nave, nuevo_estado.movimientos_nave = self.problema.estado_inicial.get_info_nave()
            # Verifico si hay una nave en el nuevo estado y la activo
            if self.problema.hay_nave(nuevo_estado):
                nuevo_estado.activar_nave()

            # === Asignacion de costo y actualizacion del nuevo estado ===
            costo = 1

            # Si hay un enemigo al estado donde voy el costo será mayor
            if self.problema.hay_enemigo(nuevo_estado):
                costo = 5

            # Si puedo usar la nave en el estado actual se degenera su uso en el siguiente estado
            # y el costo será menor
            if self.problema.estado_inicial.puede_usar_nave():
                nuevo_estado.usar_nave()
                costo = 0.5

            # Creo el problema con el nodo ya configurado
            nuevo_problema = Problema(
                nuevo_estado, self.problema.get_estado_objetivo(), self.problema.get_matriz())

            if nuevo_estado != None:

                hijo = Nodo(nuevo_problema)
                hijo.set_padre(self)
                hijo.set_operador(operador)
                hijo.set_profundidad(self.profundidad + 1)
                hijo.set_costo_acumulado(self.costo_acumulado + costo)

                self.hijos.append(hijo)'''

        return self.hijos


if __name__ == '__main__':
    '''    estado_inicial = Estado(0, 0)
    estado_inicial.activar_nave()
    estado_inicial.activar_nave()

    estado_final = copy.deepcopy(estado_inicial)

    print(str(estado_inicial))

    for i in range(10):
        estado_final.usar_nave()

    print(str(estado_inicial))'''


class Test():
    @ staticmethod
    def start():
        print("[Test.py]: Has llamado a start()")
