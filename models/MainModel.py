# [MainModel.py]

from models.shared.tools.File_selector import File_selector

debug = True


def print_debug(message):
    new_message = "[MainModel.py]: " + message
    if debug:
        print(new_message)


class MainModel:
    def __init__(self) -> None:
        print_debug("Me han instanciado pero aún no estoy implementado.")
