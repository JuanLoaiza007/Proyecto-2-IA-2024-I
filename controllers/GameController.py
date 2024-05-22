# [GameController.py]

import os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QSize, QCoreApplication
from views.GameView import Ui_MainWindow
from models.GameModel import GameModel
from models.shared.tools.iTimerPyQt5 import iTimerPyQt5
from models.shared.tools.Dialog import Dialog
from PyQt5.QtCore import QThread

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
        self.machineTurn = True
        self.modelo = GameModel()
        self.MainWindow = main_window
        self.minSizeHint = QSize(800, 600)
        self.maxSizeHint = QSize(800, 600)
        self.restartWindowSize()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.human_can_move = True
        self.machine_can_move = True

        self.buttons = []
        self.createBoard(len(self.modelo.tablero),
                         len(self.modelo.tablero[0]))
        self.paintBoard(self.modelo.tablero)
        self.updateGameState()

        # Hilo de procesamiento
        self.hilo_procesamiento: WorkerThread = None

        # Evento para cierre de programa
        self.MainWindow.destroyed.connect(self.cerrarVentana)

        # Listeners
        self.ui.btn_ver_reporte.clicked.connect(self.mostrarReporte)
        self.ui.btn_volver.clicked.connect(self.volver)

    def cerrarProcesamientos(self):
        try:
            if self.hilo_procesamiento != None and self.hilo_procesamiento.isRunning():
                self.hilo_procesamiento.exit()

        except RuntimeError:
            print_debug(
                "cerrar_procesamiento() -> He absorbido un problema con los hilos")

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
                    QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                button.setIconSize(icon_size)
                button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
                button.setObjectName(f"btn_{i}-{j}")
                button.setProperty("class", _translate(
                    "MainWindow", "ficha"))
                button.clicked.connect(
                    lambda checked, button=button: self.handle_button_click(button))
                self.ui.mainGridLayout.addWidget(button, i, j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def paintBoard(self, board):
        # Images path
        green_yoshi_abs_path = os.path.abspath(
            "./assets/images/green_yoshi.png")
        red_yoshi_abs_path = os.path.abspath("./assets/images/red_yoshi.png")

        # Icons
        green_yoshi_icon = QtGui.QIcon(green_yoshi_abs_path)
        red_yoshi_icon = QtGui.QIcon(red_yoshi_abs_path)
        null_icon = QtGui.QIcon()

        for i in range(len(board)):
            for j in range(len(board[0])):
                button = self.buttons[i][j]
                if board[i][j] == 1:
                    button.setIcon(green_yoshi_icon)
                    self.buttons[i][j].setStyleSheet(
                        "background-color: #2ecc71;")
                elif board[i][j] == 2:
                    button.setIcon(red_yoshi_icon)
                    self.buttons[i][j].setStyleSheet(
                        "background-color: #e74c3c;")
                else:
                    button.setIcon(null_icon)
                    if board[i][j] == 3:
                        self.buttons[i][j].setStyleSheet(
                            "background-color: #27ae60;")
                    elif board[i][j] == 4:
                        self.buttons[i][j].setStyleSheet(
                            "background-color: #c0392b;")
                    else:
                        self.buttons[i][j].setStyleSheet(
                            "background-color: white;")
        print("\n\n\n")

    def updateGameState(self):
        self.human_can_move = self.modelo.canMoveFrom(
            self.modelo.searchCoords("Human"))
        self.machine_can_move = self.modelo.canMoveFrom(
            self.modelo.searchCoords("Machine"))

        quienJuega = "Maquina" if self.deberiaJugarLaMaquina() else "Humano"
        puntosMaquina = self.modelo.countPoints("Machine")
        puntosHumano = self.modelo.countPoints("Human")

        self.ui.lbl_estado_juego.setText(
            f"Turno: {quienJuega} | Maquina: {puntosMaquina} | Humano: {puntosHumano}")

        if not (self.human_can_move) and not (self.machine_can_move):
            iTimerPyQt5.iniciar(200)
            if puntosMaquina > puntosHumano:
                winner = "Maquina"
            elif puntosMaquina < puntosHumano:
                winner = "Humano"
            else:
                winner = None
            resultado = f"ha ganado {winner}!" if winner else "es un empate!"
            Dialog.mostrar_dialogo(
                "Resultados", f"El juego ha terminado, {resultado}")

    def disable_button(self, i, j):
        self.buttons[i][j].setCursor(QtGui.QCursor(Qt.ArrowCursor))
        self.buttons[i][j].clicked.disconnect()

    def deberiaJugarLaMaquina(self):
        """
        Funcion que determina si la maquina debe jugar o no.
        ADVERTENCIA: Debe haber actualizado las variables human_can_move y machine_can_move antes de llamar esta funcion.
        """
        return (self.machineTurn and self.machine_can_move) or (not self.machineTurn and not (self.human_can_move))

    def handle_button_click(self, button):
        machineCoords = self.modelo.searchCoords("Machine")
        humanCoords = self.modelo.searchCoords("Human")

        i = int(button.objectName().split("_")[1].split("-")[0])
        j = int(button.objectName().split("-")[1])

        old_pos = None
        new_pos = (i, j)

        if self.deberiaJugarLaMaquina():
            old_pos = self.modelo.searchCoords("Machine")
        else:
            old_pos = self.modelo.searchCoords("Human")

        if (self.modelo.isValidMove(old_pos, new_pos)):

            if self.deberiaJugarLaMaquina():
                self.modelo.tablero[i][j] = 1
                self.modelo.tablero[machineCoords[0]][machineCoords[1]] = 3
            else:
                self.modelo.tablero[i][j] = 2
                self.modelo.tablero[humanCoords[0]][humanCoords[1]] = 4

            self.disable_button(i, j)
            self.machineTurn = not self.machineTurn

            self.modelo.printTablero()
            self.paintBoard(self.modelo.tablero)
            self.updateGameState()
        else:
            print_debug("Este movimiento no es válido")

    def mostrar(self, main_window):
        self.cargar(main_window)
        self.MainWindow.show()

    def mostrarDialogo(self, titulo, mensaje):
        self.block_focus()
        Dialog.mostrar_dialogo(titulo, mensaje)
        self.unblock_focus()

    def block_window_size(self):
        self.MainWindow.setFixedSize(self.MainWindow.size())

    def restartWindowSize(self):
        self.MainWindow.setMinimumSize(self.minSizeHint)
        self.MainWindow.setMaximumSize(self.maxSizeHint)

    def block_focus(self):
        """
        Funcion intuitiva para mostrar que la ventana principal NO es la que esta recibiendo eventos, ayuda a mostrar que el flujo de trabajo esta ocurriendo en otra ventana.
        """
        self.MainWindow.setEnabled(False)
        self.ui.centralwidget.setEnabled(False)
        self.ui.centralwidget.setVisible(False)
        self.block_window_size()

    def little_block_focus(self):
        """
        Funcion intuitiva para mostrar que la ventana principal esta procesando sin embargo el flujo de trabajo esta actualmente en ella.
        """
        self.MainWindow.setEnabled(False)
        self.ui.centralwidget.setEnabled(False)
        self.block_window_size()

    def unblock_focus(self):
        """
        Funcion intuitiva para revertir block_focus() y little_block_focus(), muestra que el flujo de trabajo esta ocurriendo en la ventana principal y habilita los eventos.
        """
        self.restartWindowSize()
        self.MainWindow.setEnabled(True)
        self.ui.centralwidget.setEnabled(True)
        self.ui.centralwidget.setVisible(True)

    def habilitar_botones_footer(self):
        self.ui.btn_volver.setVisible(True)
        self.ui.btn_volver.setEnabled(True)
        self.ui.btn_ver_reporte.setVisible(True)
        self.ui.btn_ver_reporte.setEnabled(True)

    def deshabilitar_botones_footer(self):
        self.ui.btn_volver.setVisible(False)
        self.ui.btn_volver.setEnabled(False)
        self.ui.btn_ver_reporte.setVisible(False)
        self.ui.btn_ver_reporte.setEnabled(False)

    def iniciar_juego(self):

        iTimerPyQt5.iniciar(100)

        # Empezar juego

        iTimerPyQt5.iniciar(100)

        # Uso de hilos de procesamiento

        # # Hilo para mantener la interfaz atenta
        # self.hilo_procesamiento = WorkerThread(self.modelo.iniciar_juego)
        # # Eventos que requieren los calculos del hilo
        # self.hilo_procesamiento.finished.connect(
        #     self.tarea_a_ejecutar)
        # # Inicia las tareas del hilo de la funcion run()
        # self.hilo_procesamiento.start()

    def mostrarReporte(self):
        print_debug(
            "mostrarReporte() -> Boton de mostrar reporte presionado!!!")

    def volver(self):
        self.cerrarProcesamientos()
        from controllers.MainController import MainController as NewController
        self.NewController = NewController()
        self.NewController.cargar(self.MainWindow)
        return None
