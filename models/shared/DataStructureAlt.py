# [DataStructure.py]
import copy

debug = False


def print_debug(message):
    new_message = "[DataStructure.py]: " + message
    if debug:
        print(new_message)


movimientos = [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]


def generateHorseMoves(old_pos, board):
    """
    Genera los movimientos de caballo posibles en el tablero considerando movimientos de caballo legales (Dentro del tablero, en L y no ocupado).
    """
    filas = range(len(board))
    columnas = range(len(board[0]))

    posibles_movimientos = []

    for movimiento in movimientos:
        new_pos = (old_pos[0] + movimiento[0], old_pos[1] + movimiento[1])
        if (
            new_pos[0] in filas
            and new_pos[1] in columnas
            and isFreePosition(new_pos, board)
        ):
            posibles_movimientos.append(new_pos)
    return posibles_movimientos


def searchCoords(someone, board):
    id = 1 if someone == "Machine" else 2
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == id:
                return (i, j)
    raise Exception(f"No se encontró a {someone}")


def isFreePosition(pos, board):
    return board[pos[0]][pos[1]] == 0


def isValidMove(old_pos, new_pos, board):
    return new_pos in generateHorseMoves(old_pos, board)


def canMoveFrom(old_pos, board):
    possible_moves = generateHorseMoves(old_pos, board)
    if possible_moves == []:
        return False
    return True


class Problema:
    def __init__(self, tablero):
        self.tablero = tablero

        self.coordsHumano = searchCoords(
            "Human",
            self.tablero,
        )
        self.coordsMaquina = searchCoords(
            "Machine",
            self.tablero,
        )

        movsCaballoHumano = generateHorseMoves(self.coordsHumano, tablero)
        movsCaballoMaquina = generateHorseMoves(self.coordsMaquina, tablero)
        self.movsPosibleHumano = []
        self.movsPosibleMaquina = []

        for mov in movsCaballoHumano:
            if isValidMove(self.coordsHumano, mov, tablero):
                self.movsPosibleHumano.append(mov)
        for mov in movsCaballoMaquina:
            if isValidMove(self.coordsMaquina, mov, tablero):
                self.movsPosibleMaquina.append(mov)

    def __str__(self):
        tablero_to_print = ""
        for line in self.tablero:
            tablero_to_print += " ".join(str(x) for x in line) + "\n"
        return f"tablero:\n{tablero_to_print}"


class Nodo:
    """
    Clase que representa un nodo en un árbol.

    Cada nodo del árbol guarda la siguiente información:
    - El problema
    - Una referencia al nodo padre
    - Profundidad del nodo
    """

    def __init__(self, problema: Problema):
        """
        Inicializa un nuevo nodo raiz.
        """
        self.problema: Problema = problema
        self.padre: Nodo = None
        self.profundidad: int = 0

    def __str__(self) -> str:
        padre = None if not self.padre else f"someone at {self.padre.profundidad}"
        mensaje = f"Padre: {padre}, problema: {self.problema}, profundidad: {self.profundidad}\n"
        return mensaje

    def calcular_heuristica(self):
        heuristica = Heuristica(self.problema)
        return heuristica.getHeuristica()

    def expandir(self, someone):
        """
        Expande el nodo actual para someone.

        Args:
            someone (str): La maquina ("Machine") o el humano ("Human").

        Returns:
            list[Nodo]: Donde list[Nodo] corresponde a los hijos.
        """
        self.hijos = []
        movs = (
            self.problema.movsPosibleMaquina
            if someone == "Machine"
            else self.problema.movsPosibleHumano
        )
        actualPos = (
            self.problema.coordsMaquina
            if someone == "Machine"
            else self.problema.coordsHumano
        )

        for mov in movs:
            self.hijo = None
            nuevo_tablero = copy.deepcopy(self.problema.tablero)
            nuevo_tablero[actualPos[0]][actualPos[1]] = 3 if someone == "Machine" else 4
            nuevo_tablero[mov[0]][mov[1]] = 1 if someone == "Machine" else 2
            nuevo_problema = Problema(nuevo_tablero)
            hijo = Nodo(nuevo_problema)
            hijo.padre = self
            hijo.profundidad = self.profundidad + 1
            if hijo:
                self.hijos.append(hijo)

        return self.hijos


class Heuristica:
    def __init__(self, problema: Problema):

        self.problema = problema
        self.tablero = self.problema.tablero

        self.n = len(self.tablero)
        self.m = len(self.tablero[0])

        self.posicion_maquina = self.problema.coordsMaquina
        self.posicion_oponente = self.problema.coordsHumano
        self.num_movimientos_maquina = len(self.problema.movsPosibleMaquina)
        self.num_movimientos_oponente = len(self.problema.movsPosibleHumano)

        self.centro_maquina = self.control_centro(*self.posicion_maquina)
        self.centro_oponente = self.control_centro(*self.posicion_oponente)

        # Coeficientes ajustables
        a = 1.0
        b = 1.5
        c = 0.5
        d = 0.5

        self.heuristica = (
            a * self.num_movimientos_maquina
            - b * self.num_movimientos_oponente
            + c * self.centro_maquina
            - d * self.centro_oponente
        )

    def control_centro(self, x, y):
        centro_x, centro_y = self.n // 2, self.m // 2
        return -abs(x - centro_x) - abs(y - centro_y)

    def getHeuristica(self):
        return self.heuristica


if __name__ == "__main__":
    tablero = [[0, 0, 0, 0], [0, 0, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]]

    problema_inicial = Problema(tablero)
    nodo_raiz = Nodo(problema_inicial)

    print("Estado inicial del nodo raíz:")
    print(nodo_raiz)

    print("\nHeurística del nodo raíz:")
    print(nodo_raiz.calcular_heuristica())

    print("\nExpansión de movimientos de la máquina:")
    hijos = nodo_raiz.expandir("Machine")
    for hijo in hijos:
        print(hijo)

    print("\nExpansión de movimientos de la humano:")
    hijos = nodo_raiz.expandir("Human")
    for hijo in hijos:
        print(hijo)
