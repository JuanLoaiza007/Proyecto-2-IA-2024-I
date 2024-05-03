# [Dialog.py]

from views.SmDialogAccept import Ui_Dialog as SmDialogAccept
from models.shared.tools.iTimerPyQt5 import iTimerPyQt5
from PyQt5 import QtWidgets


class Dialog:
    @staticmethod
    def mostrar_dialogo(titulo, mensaje):
        iTimerPyQt5.iniciar(1)

        new_dialog = QtWidgets.QDialog()
        new_ui = SmDialogAccept()
        new_ui.setupUi(new_dialog)
        new_dialog.setModal(True)
        new_dialog.show()
        new_ui.lbl_title.setText(titulo)
        new_ui.lbl_body.setText(mensaje)

        new_dialog.exec()
