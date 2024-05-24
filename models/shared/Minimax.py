# [Minimax.py]

from DataStructureAlt import (
    Problema,
    Nodo,
)


def minimax(nodo, profundidad, maximizando, alpha=float("-inf"), beta=float("inf")):
    if profundidad == 0 or not nodo.expandir("Machine") and not nodo.expandir("Human"):
        return nodo.calcular_heuristica()

    if maximizando:
        max_eval = float("-inf")
        for hijo in nodo.expandir("Machine"):
            eval = minimax(hijo, profundidad - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float("inf")
        for hijo in nodo.expandir("Human"):
            eval = minimax(hijo, profundidad - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def mejor_jugada(tablero, profundidad):
    problema_inicial = Problema(tablero)
    nodo_raiz = Nodo(problema_inicial)

    mejor_valor = float("-inf")
    mejor_movimiento = None

    for hijo in nodo_raiz.expandir("Machine"):
        valor = minimax(hijo, profundidad - 1, False)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_movimiento = hijo.problema.tablero

    return mejor_movimiento


if __name__ == "__main__":
    tablero = [[0, 0, 0, 0], [0, 1, 3, 0], [0, 4, 0, 0], [0, 0, 2, 0]]

    profundidad = 2
    mejor_mov = mejor_jugada(tablero, profundidad)

    print("Para: ")
    for fila in tablero:
        print(fila)
    print(f"Mejor jugada para la máquina con profundidad de {profundidad} es:")
    for fila in mejor_mov:
        print(fila)
