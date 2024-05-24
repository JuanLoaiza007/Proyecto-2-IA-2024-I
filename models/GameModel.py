# [GameModel.py]
import random

debug = False


def print_debug(message):
    new_message = "[GameModel.py]: " + message
    if debug:
        print(new_message)


class GameModel:
    def __init__(self):
        self.difficulty = None
        self.tablero = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        self.setInitialRandomPositionToPlayers()

    def setInitialRandomPositionToPlayers(self):
        filas = len(self.tablero)

        columnas = len(self.tablero[0])
        pos1 = (random.randint(0, filas - 1), random.randint(0, columnas - 1))
        pos2 = pos1

        while pos2 == pos1:
            pos2 = (random.randint(0, filas - 1), random.randint(0, columnas - 1))

        self.tablero[pos1[0]][pos1[1]] = 1
        self.tablero[pos2[0]][pos2[1]] = 2

    def generateHorseMoves(self, old_pos):
        filas = range(len(self.tablero))
        columnas = range(len(self.tablero[0]))

        movimientos = [
            (2, 1),
            (-2, 1),
            (2, -1),
            (-2, -1),
            (1, 2),
            (-1, 2),
            (1, -2),
            (-1, -2),
        ]
        posibles_movimientos = []

        for movimiento in movimientos:
            new_pos = (old_pos[0] + movimiento[0], old_pos[1] + movimiento[1])
            if (
                new_pos[0] in filas
                and new_pos[1] in columnas
                and self.isFreePosition(new_pos)
            ):
                posibles_movimientos.append(new_pos)
        return posibles_movimientos

    def isFreePosition(self, pos):
        return self.tablero[pos[0]][pos[1]] == 0

    def isValidHorseMove(self, old_pos, new_pos):
        dx = abs(old_pos[0] - new_pos[0])
        dy = abs(old_pos[1] - new_pos[1])
        print_debug("dx: " + str(dx) + " dy: " + str(dy))
        return (dx, dy) in [(1, 2), (2, 1)]

    def isValidMove(self, old_pos, new_pos):
        return self.isValidHorseMove(old_pos, new_pos) and self.isFreePosition(new_pos)

    def canMoveFrom(self, old_pos):
        possible_moves = self.generateHorseMoves(old_pos)
        for move in possible_moves:
            if self.isValidMove(old_pos, move):
                return True
        return False

    def countPoints(self, someone="Machine"):
        count = 0
        now = 1 if someone == "Machine" else 2
        taked = 3 if someone == "Machine" else 4
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[i])):
                if self.tablero[i][j] == now or self.tablero[i][j] == taked:
                    count += 1
        return count

    def searchCoords(self, someone="Machine"):
        id = 1 if someone == "Machine" else 2
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[0])):
                if self.tablero[i][j] == id:
                    return (i, j)
        raise Exception(f"No se encontró a {someone}")

    def printTablero(self):
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[0])):
                print(self.tablero[i][j], end=" ")
            print()
