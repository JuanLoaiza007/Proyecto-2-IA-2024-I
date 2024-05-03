# [GameController.py]

import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize
from views.GameView import Ui_MainWindow
from models.GameModel import GameModel
from models.shared.tools.iTimerPyQt5 import iTimerPyQt5
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
        self.modelo = GameModel()
        self.MainWindow = main_window
        self.minSizeHint = QSize(800, 600)
        self.maxSizeHint = QSize(800, 600)
        self.restart_window_size()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        # self.deshabilitar_botones_footer()
        self.inicializar_tabla()

        # Hilo de procesamiento
        self.hilo_procesamiento: WorkerThread = None

        # Evento para cierre de programa
        self.MainWindow.destroyed.connect(self.cerrar_ventana)

        # Listeners
        self.ui.btn_ver_reporte.clicked.connect(self.mostrar_reporte)
        self.ui.btn_volver.clicked.connect(self.volver)

    def cerrar_procesamientos(self):
        try:
            if self.hilo_procesamiento != None and self.hilo_procesamiento.isRunning():
                self.hilo_procesamiento.exit()

        except RuntimeError:
            print_debug(
                "cerrar_procesamiento() -> He absorbido un problema con los hilos")

    def cerrar_ventana(self):
        self.cerrar_procesamientos()
        os._exit(0)

    def inicializar_tabla(self):
        self.ui.table_mapa.setRowCount(10)
        self.ui.table_mapa.setColumnCount(10)
        self.ui.table_mapa.verticalHeader().setVisible(False)
        self.ui.table_mapa.horizontalHeader().setVisible(False)
        self.ui.table_mapa.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)
        self.ui.table_mapa.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch)

    def actualizar_tabla(self):
        print_debug(
            "actualizar_tabla -> Me han llamado pero no estoy implementado.")

    def mostrar(self, main_window):
        self.cargar(main_window)
        self.MainWindow.show()

    def block_window_size(self):
        self.MainWindow.setFixedSize(self.MainWindow.size())

    def restart_window_size(self):
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
        self.restart_window_size()
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

    def mostrar_reporte(self):
        print_debug(
            "mostrar_reporte() -> Boton de mostrar reporte presionado!!!")

    def volver(self):
        self.cerrar_procesamientos()
        from controllers.MainController import MainController as NewController
        self.NewController = NewController()
        self.NewController.cargar(self.MainWindow)
        return None
