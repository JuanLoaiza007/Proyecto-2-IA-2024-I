# [MainModel.py]

from models.shared.tools.File_selector import File_selector

debug = False


def print_debug(message):
    new_message = "[MainModel.py]: " + message
    if debug:
        print(new_message)


class MainModel:
    def __init__(self) -> None:
        self.dificultades = [
            "Principiante",
            "Amateur",
            "Experto",
        ]
        self.dificultad = None
