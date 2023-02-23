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
from PySide2.QtCore import QPoint, QObject, QRunnable, Signal, QThreadPool, QThread

SNAKE_DIRECTION = {16777236: 'RIGHT',
                   16777234: 'LEFT',
                   16777235: 'UP',
                   16777237: 'DOWN'}


class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(str)
    result = Signal(int)


class Worker(QRunnable):
    def __init__(self):
        """
        :param
        """
        super().__init__()
        self.signals = WorkerSignals()

    def run(self):
        try:
            var_in_worker = 1
        except Exception as e:
            self.signals.error.emit(str(e))
        else:
            while True:
                QThread.sleep(1)
                self.signals.result.emit(var_in_worker)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.LEN_SNAKE = 30  # начальная длина змеи
        self.POINT_X = 100
        self.POINT_Y = 100
        self.SNAKE_DIRECTION = 'RIGHT'
        self.SNAKE_STEP = 10

        self.threadpool = QThreadPool()  # Пул потоков

        path_ico = str(Path(os.getcwd()))
        main_ico = QIcon(path_ico + '/ico/snake.png')
        self.setWindowIcon(main_ico)

        self.init_UI()

    def init_UI(self):
        self.setGeometry(500, 500, 500, 500)
        self.setWindowTitle('Snake')

        self.label = QLabel()
        self.canvas = QPixmap(500, 500)
        self.canvas.fill(QColor('green'))
        self.label.setPixmap(self.canvas)
        self.setCentralWidget(self.label)


        worker = Worker()
        worker.signals.result.connect(self.worker_output)
        self.threadpool.start(worker)

        self.show()

    def draw_snake(self):
        self.POINT_X = self.POINT_X + self.SNAKE_STEP
        self.canvas = QPixmap(500, 500)
        self.canvas.fill(QColor('green'))
        self.label.setPixmap(self.canvas)

        self.canvas = self.label.pixmap()
        painter = QPainter(self.canvas)
        pen = QPen()
        pen.setWidth(15)
        pen.setColor(QColor('blue'))
        painter.setPen(pen)
        painter.drawLine(
            QPoint(self.POINT_X, self.POINT_Y),
            QPoint(self.POINT_X - self.LEN_SNAKE, self.POINT_Y)
        )
        painter.end()
        self.label.setPixmap(self.canvas)

    def worker_output(self, s):
        print(s)
        self.draw_snake()

    def keyPressEvent(self, event):
        self.SNAKE_DIRECTION = SNAKE_DIRECTION[event.key()]
        print(self.SNAKE_DIRECTION)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    app.exec_()
