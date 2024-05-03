# [GameModel.py]

debug = False


def print_debug(message):
    new_message = "[GameModel.py]: " + message
    if debug:
        print(new_message)


class GameModel:
    def __init__(self):
        print_debug("Me han instanciado pero no estoy implementado!")
