# -----------------------------------------------------------
# Игра "змейка"
#
# 2023 Kuznetsov Konstantin
# email kuznetsovkm@yandex.ru

# -----------------------------------------------------------

import sys
import os
from pathlib import Path

from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QStyleFactory, QLabel
from PySide2.QtGui import QIcon, QPixmap, QPainter, QPen, QColor
from PySide2.QtCore import QPoint



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

        self.label = QLabel()
        canvas = QPixmap(500, 500)
        canvas.fill(QColor('green'))
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        self.draw_something()
        self.show()

    def draw_something(self):
        canvas = self.label.pixmap()
        painter = QPainter(canvas)
        pen = QPen()
        pen.setWidth(15)
        pen.setColor(QColor('blue'))
        painter.setPen(pen)
        painter.drawLine(
            QPoint(100, 100),
            QPoint(150, 100)
        )
        painter.end()
        self.label.setPixmap(canvas)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    app.exec_()
