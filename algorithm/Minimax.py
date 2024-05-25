from models.shared.DataStructure import *


class Minimax:
    @staticmethod
    def minimax(problema: Problema):
        mejor_accion = None
        mejor_utilidad = 0

        inicial = problema.get_estado_inicial()

        for accion in problema.movimientos_jugador(inicial):
            nuevo_estado = problema.nuevo_estado(inicial, accion)
            print("Estado", nuevo_estado)
            utilidad = Minimax.valor_min(problema, nuevo_estado)

            if utilidad > mejor_utilidad:
                mejor_accion = accion
                mejor_utilidad = utilidad

        return mejor_accion

    @staticmethod
    def valor_min(problema: Problema, estado: Estado):
        if problema.es_estado_objetivo(estado):
            return problema.utilidad(estado)
        menor_valor = float("inf")

        for accion in problema.movimientos_jugador(estado):
            nuevo_estado = problema.nuevo_estado(estado, accion)
            utilidad = Minimax.valor_max(problema, nuevo_estado)
            menor_valor = min(menor_valor, utilidad)

        return menor_valor

    @staticmethod
    def valor_max(problema: Problema, estado: Estado):
        if problema.es_estado_objetivo(estado):
            return problema.utilidad(estado)
        mayor_valor = float("-inf")

        for accion in problema.movimientos_jugador(estado):
            nuevo_estado = problema.nuevo_estado(estado, accion)
            utilidad = Minimax.valor_min(problema, nuevo_estado)
            mayor_valor = max(mayor_valor, utilidad)

        return mayor_valor
