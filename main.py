# -----------------------------------------------------------
# Игра "змейка"
#
# 2023 Kuznetsov Konstantin
# email kuznetsovkm@yandex.ru

# -----------------------------------------------------------

import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QStyleFactory


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle('Painter')
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    app.exec_()
