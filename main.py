# -----------------------------------------------------------
# Игра "змейка"
#
# 2023 Kuznetsov Konstantin
# email kuznetsovkm@yandex.ru

# -----------------------------------------------------------

import sys
import os
from pathlib import Path

from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QStyleFactory
from PySide2.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        path_ico = str(Path(os.getcwd()))
        main_ico = QIcon(path_ico + '/ico/snake.png')
        self.setWindowIcon(main_ico)
        self.init_UI()

    def init_UI(self):
        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle('Snake')
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    app.exec_()
