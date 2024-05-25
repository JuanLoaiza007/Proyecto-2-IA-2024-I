# [GameController.py]

import os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QSize, QCoreApplication
from views.GameView import Ui_MainWindow
from models.GameModel import GameModel
from models.shared.DataStructure import *
from models.shared.tools.iTimerPyQt5 import iTimerPyQt5
from models.shared.tools.Dialog import Dialog
from models.shared.Minimax import mejor_jugada
from PyQt5.QtCore import QThread
import random

debug = True


def print_debug(message):
    new_message = "[GameController.py]: " + message
    if debug:
        print(new_message)


class WorkerThread(QThread):
    """
    Clase de Hilo Trabajador para ejecutar procesamiento en segundo plano y conservar la ventana recibiendo eventos.
    """

    def __init__(self, funcion, *args, **kwargs):
        super().__init__()
        self.funcion = funcion
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.funcion(*self.args, **self.kwargs)


class GameController:
    """
    Clase GameController.
    Gestiona todo lo necesario para ejecutar un algoritmo y mostrarlo visualmente

    Atencion! Antes de ejecutar "mostrar()":
        * cargar(mainwindow)
        * cargar_ambiente(ambiente)
        * cargar_algoritmo(algoritmo)
    """

    # Funcion para inicializar (general)
    def cargar(self, main_window):
        self.machineTurn = False
        self.modelo = GameModel()
        self.MainWindow = main_window
        self.minSizeHint = QSize(800, 600)
        self.maxSizeHint = QSize(800, 600)
        self.restartWindowSize()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        #  Configuracion de los jugadores
        self.human_can_move = True
        self.machine_can_move = True
        self.machineTurn = True

        # Configuracion del tablero de juego
        self.buttons = []
        self.createBoard(len(self.modelo.tablero), len(self.modelo.tablero[0]))
        self.paintBoard(self.modelo.tablero)
        self.updateGameState()
        self.searchAndDisableActualPosition()

        # Hilo de procesamiento
        self.hilo_procesamiento: WorkerThread = None

        # Evento para cierre de programa
        self.MainWindow.destroyed.connect(self.cerrarVentana)

        # Listeners
        self.ui.btn_volver.clicked.connect(self.volver)

    def cerrarProcesamientos(self):
        try:
            if (
                self.hilo_procesamiento is not None
                and self.hilo_procesamiento.isRunning()
            ):
                self.hilo_procesamiento.exit()

        except RuntimeError:
            print_debug(
                "cerrar_procesamiento() -> He absorbido un problema con los hilos"
            )

    def cerrarVentana(self):
        self.cerrarProcesamientos()
        os._exit(0)

    def createBoard(self, rows, cols):
        _translate = QCoreApplication.translate
        icon_size = None

        if rows <= 6 and cols <= 6:
            icon_size = QSize(80, 80)
        else:
            icon_size = QSize(30, 30)

        for i in range(rows):
            row_buttons = []
            for j in range(cols):
                button = QtWidgets.QPushButton(self.ui.mainFrame)
                button.setSizePolicy(
                    QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
                )
                button.setIconSize(icon_size)
                button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
                button.setObjectName(f"btn_{i}-{j}")
                button.setProperty("class", _translate("MainWindow", "ficha"))
                button.clicked.connect(
                    lambda checked, button=button: self.handleButtonClick(button)
                )
                self.ui.mainGridLayout.addWidget(button, i, j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def paintBoard(self, board):
        # Images path
        green_yoshi_abs_path = os.path.abspath("./assets/images/green_yoshi.png")
        red_yoshi_abs_path = os.path.abspath("./assets/images/red_yoshi.png")

        # Icons
        green_yoshi_icon = QtGui.QIcon(green_yoshi_abs_path)
        red_yoshi_icon = QtGui.QIcon(red_yoshi_abs_path)
        null_icon = QtGui.QIcon()

        try:
            for i in range(len(board)):
                for j in range(len(board[0])):
                    button = self.buttons[i][j]
                    if board[i][j] == 1:
                        button.setIcon(green_yoshi_icon)
                        self.buttons[i][j].setStyleSheet("background-color: #2ecc71;")
                    elif board[i][j] == 2:
                        button.setIcon(red_yoshi_icon)
                        self.buttons[i][j].setStyleSheet("background-color: #e74c3c;")
                    else:
                        button.setIcon(null_icon)
                        if board[i][j] == 3:
                            self.buttons[i][j].setStyleSheet(
                                "background-color: #27ae60;"
                            )
                        elif board[i][j] == 4:
                            self.buttons[i][j].setStyleSheet(
                                "background-color: #c0392b;"
                            )
                        else:
                            self.buttons[i][j].setStyleSheet("background-color: white;")
            print("\n\n\n")
        except Exception as e:
            print_debug(f"paintBoard() -> ERROR: {e}")

    def updateGame(self):
        try:
            self.machineTurn = not self.machineTurn  # Toggle machineTurn
            self.modelo.printTablero()
            self.paintBoard(self.modelo.tablero)
            self.updateGameState()  # Update gamestate
            self.move_machine()  # Ask if machine would like to move
        except Exception as e:
            print_debug(f"updateGame() -> ERROR: {e}")

    def updateGameState(self):
        self.human_can_move = self.modelo.canMoveFrom(self.modelo.searchCoords("Human"))
        self.machine_can_move = self.modelo.canMoveFrom(
            self.modelo.searchCoords("Machine")
        )

        x, y = self.modelo.searchCoords("Human")
        estado = Estado(x, y)

        humanUtility = Problema.utilidad(estado)
        print_debug(f"updateGameState() -> {humanUtility}")

        quienJuega = "Maquina" if self.shouldPlayMachine() else "Humano"
        puntosMaquina = self.modelo.countPoints("Machine")
        puntosHumano = self.modelo.countPoints("Human")

        self.ui.lbl_estado_juego.setText(
            f"Turno: {quienJuega} | Maquina: {puntosMaquina} | Humano: {puntosHumano}"
        )

        if not (self.human_can_move) and not (self.machine_can_move):
            if puntosMaquina == puntosHumano:
                winner = None
            else:
                winner = "la maquina" if puntosMaquina > puntosHumano else "el humano"

            resultado = f"ha ganado {winner}!" if winner else "es un empate!"
            self.mostrarDialogo("Resultados", f"El juego ha terminado, {resultado}")

    def disableButton(self, i, j):
        try:
            self.buttons[i][j].setCursor(QtGui.QCursor(Qt.ArrowCursor))
            self.buttons[i][j].clicked.disconnect()
        except Exception as e:
            print_debug(f"disableButton() -> ERROR: {e}")

    def searchAndDisableActualPosition(self):
        humanCoords = self.modelo.searchCoords("Human")
        machineCoords = self.modelo.searchCoords("Machine")

        self.disableButton(humanCoords[0], humanCoords[1])
        self.disableButton(machineCoords[0], machineCoords[1])

    def shouldPlayMachine(self):
        """
        Funcion que determina si la maquina debe jugar o no.
        ADVERTENCIA: Debe haber actualizado las variables human_can_move y machine_can_move antes de llamar esta funcion.
        """
        return (self.machineTurn and self.machine_can_move) or (
            not self.machineTurn and not (self.human_can_move)
        )

    def move_machine(self):
        """
        Funcion que realiza el movimiento de la máquina
        """
        if self.human_can_move or self.machine_can_move:
            if self.shouldPlayMachine() and self.machine_can_move:
                old_pos_machine = self.modelo.searchCoords("Machine")
                new_pos_machine = mejor_jugada(
                    self.modelo.tablero, self.modelo.intDifficulty
                )
                self.modelo.tablero[new_pos_machine[0]][new_pos_machine[1]] = 1
                self.modelo.tablero[old_pos_machine[0]][old_pos_machine[1]] = 3

                iTimerPyQt5.iniciar(1000)
                self.disableButton(new_pos_machine[0], new_pos_machine[1])
                self.updateGame()

    def handleButtonClick(self, button):
        if not self.shouldPlayMachine():
            i = int(button.objectName().split("_")[1].split("-")[0])
            j = int(button.objectName().split("-")[1])

            old_pos_human = self.modelo.searchCoords("Human")
            new_pos_human = (i, j)
            print_debug(f"handle_button_click() -> {old_pos_human} -> {new_pos_human}")

            if self.modelo.isValidMove(old_pos_human, new_pos_human):
                self.modelo.tablero[i][j] = 2
                self.modelo.tablero[old_pos_human[0]][old_pos_human[1]] = 4

                self.disableButton(i, j)
                self.updateGame()
            else:
                print_debug("Este movimiento no es válido")

    def mostrar(self, main_window):
        self.cargar(main_window)
        self.MainWindow.show()

    def mostrarDialogo(self, titulo, mensaje):
        self.blockFocus()
        Dialog.mostrar_dialogo(titulo, mensaje)
        self.unblockFocus()

    def blockWindowSize(self):
        self.MainWindow.setFixedSize(self.MainWindow.size())

    def restartWindowSize(self):
        self.MainWindow.setMinimumSize(self.minSizeHint)
        self.MainWindow.setMaximumSize(self.maxSizeHint)

    def blockFocus(self):
        """
        Funcion intuitiva para mostrar que la ventana principal NO es la que esta recibiendo eventos, ayuda a mostrar que el flujo de trabajo esta ocurriendo en otra ventana.
        """
        self.MainWindow.setEnabled(False)
        self.ui.centralwidget.setEnabled(False)
        self.ui.centralwidget.setVisible(False)
        self.blockWindowSize()

    def littleBlockFocus(self):
        """
        Funcion intuitiva para mostrar que la ventana principal esta procesando sin embargo el flujo de trabajo esta actualmente en ella.
        """
        self.MainWindow.setEnabled(False)
        self.ui.centralwidget.setEnabled(False)
        self.blockWindowSize()

    def unblockFocus(self):
        """
        Funcion intuitiva para revertir blockFocus() y littleBlockFocus(), muestra que el flujo de trabajo esta ocurriendo en la ventana principal y habilita los eventos.
        """
        self.restartWindowSize()
        self.MainWindow.setEnabled(True)
        self.ui.centralwidget.setEnabled(True)
        self.ui.centralwidget.setVisible(True)

    def startGame(self, difficulty):
        self.modelo.difficulty = difficulty
        self.modelo.intDifficulty = (
            2 if difficulty == "Facil" else 4 if difficulty == "Medio" else 6
        )
        self.ui.lbl_titulo.setText(f"Modo {difficulty}")
        self.move_machine()

    def volver(self):
        self.cerrarProcesamientos()
        from controllers.MainController import MainController as NewController

        self.NewController = NewController()
        self.NewController.cargar(self.MainWindow)
        return None
