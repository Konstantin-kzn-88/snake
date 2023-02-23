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
from PySide2.QtCore import QPoint, QObject, QRunnable, Signal, QThreadPool, Qt


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
            self.signals.finished.emit()
            self.signals.result.emit(var_in_worker)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.LEN_SNAKE = 30  # начальная длина змеи
        self.POINT = (100, 100)  # точка головы змеи
        self.SNAKE_DIRECTION = 'RIGHT'

        self.threadpool = QThreadPool()  # Пул потоков

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
            QPoint(self.POINT[0], self.POINT[1]),
            QPoint(self.POINT[0] - self.LEN_SNAKE, self.POINT[1])
        )
        painter.end()
        self.label.setPixmap(canvas)

        worker = Worker()
        worker.signals.result.connect(self.worker_output)
        worker.signals.finished.connect(self.worker_complete)
        self.threadpool.start(worker)

    def worker_output(self, s):
        print(s)

    def worker_complete(self):
        print("THREAD COMPLETE!")

    def keyPressEvent(self, event):
        self.SNAKE_DIRECTION = SNAKE_DIRECTION[event.key()]
        print(self.SNAKE_DIRECTION)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    app.exec_()
