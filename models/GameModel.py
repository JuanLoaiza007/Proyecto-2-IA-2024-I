# [GameModel.py]

debug = True


def print_debug(message):
    new_message = "[GameModel.py]: " + message
    if debug:
        print(new_message)


class GameModel:
    def __init__(self):
        self.tablero = [[1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 2],
                        ]

    def count_machine_points(self):
        count = 0
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[0])):
                if self.tablero[i][j] == 1 or self.tablero[i][j] == 3:
                    count += 1
        return count

    def count_human_points(self):
        count = 0
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[0])):
                if self.tablero[i][j] == 2 or self.tablero[i][j] == 4:
                    count += 1
        return count

    def search_machine_coords(self):
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[0])):
                if self.tablero[i][j] == 1:
                    return (i, j)
        raise Exception("No se encontró a la máquina en el tablero")

    def search_human_coords(self):
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[0])):
                if self.tablero[i][j] == 2:
                    return (i, j)
        raise Exception("No se encontró al humano en el tablero")

    def imprimir_tablero(self):
        print_debug("imprimir_tablero() -> Imprimiendo el tablero")
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[0])):
                print(self.tablero[i][j], end=" ")
            print()
