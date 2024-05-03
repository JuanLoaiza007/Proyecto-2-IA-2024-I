# [iTimerPyQt5.py]

from PyQt5.QtCore import QTimer, QEventLoop


class iTimerPyQt5:
    @staticmethod
    def iniciar(tiempo):
        loop = QEventLoop()
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(loop.quit)
        tiempo_ms = tiempo
        timer.start(tiempo_ms)
        loop.exec_()
