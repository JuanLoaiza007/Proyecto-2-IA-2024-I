# [MainController.py]

import os
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from views.MainView import Ui_MainWindow
from models.MainModel import MainModel
from models.shared.tools.Dialog import Dialog

debug = False


def print_debug(message):
    new_message = "[MainController.py]: " + message
    if debug:
        print(new_message)


class MainController:
    # Funcion para inicializar (general)
    def cargar(self, main_window):
        self.modelo = MainModel()
        self.MainWindow = main_window
        self.minSizeHint = QSize(800, 600)
        self.maxSizeHint = QSize(800, 600)
        self.restart_window_size()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        # Listeners específicos
        self.ui.box_dificultad.currentIndexChanged.connect(self.cambiar_dificultad)
        self.ui.btn_iniciar.clicked.connect(self.iniciar)
        self.ui.btn_sobre.clicked.connect(self.mostrar_sobre_nosotros)

        self.ui.box_dificultad.addItems(self.modelo.dificultades)
        self.cargar_imagenes()

    def block_window_size(self):
        self.MainWindow.setFixedSize(self.MainWindow.size())

    def restart_window_size(self):
        self.MainWindow.setMinimumSize(self.minSizeHint)
        self.MainWindow.setMaximumSize(self.maxSizeHint)

    def cargar_imagenes(self):
        # image_path = os.path.abspath(
        #     "./views/assets/gui/sidebar_image.png")
        # self.ui.lbl_side_image.setPixmap(QtGui.QPixmap(image_path))
        print_debug(
            "cargar_imagenes -> La funcion de cargar imagenes aún no está implementada"
        )

    def cambiar_dificultad(self):
        self.modelo.dificultad = self.ui.box_dificultad.currentText()

    def mostrar(self, main_window):
        self.cargar(main_window)
        self.MainWindow.show()

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

    def mostrar_dialogo(self, titulo, mensaje):
        self.block_focus()
        Dialog.mostrar_dialogo(titulo, mensaje)
        self.unblock_focus()

    def iniciar(self):
        from controllers.GameController import GameController

        if not (self.modelo.dificultad):
            self.mostrar_dialogo("Error", f"La dificultad es {self.modelo.dificultad}")
            return None
        self.controlador = GameController()
        self.controlador.cargar(self.MainWindow)
        self.controlador.startGame(self.modelo.dificultad)

    def mostrar_sobre_nosotros(self):
        from controllers.AboutUsController import AboutUsController

        self.AboutUsController = AboutUsController()
        self.AboutUsController.mostrar(self.MainWindow)
