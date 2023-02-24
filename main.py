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
from PySide2.QtCore import QPoint, QObject, QRunnable, Signal, QThreadPool, QThread, Qt

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
                QThread.msleep(200)
                self.signals.result.emit(var_in_worker)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.POINT_X = [20, 30, 40]
        self.POINT_Y = [20, 20, 20]
        self.SNAKE_DIRECTION = 'RIGHT'
        self.SNAKE_STEP = 10

        self.threadpool = QThreadPool()  # Пул потоков

        path_ico = str(Path(os.getcwd()))
        main_ico = QIcon(path_ico + '/ico/snake.png')
        self.setWindowIcon(main_ico)

        self.init_UI()

    def init_UI(self):
        self.setFixedSize(500, 500)
        self.setWindowTitle('Snake')

        self.label = QLabel()
        self.canvas = QPixmap(500, 500)
        self.canvas.fill(QColor('green'))
        self.label.setPixmap(self.canvas)
        self.setCentralWidget(self.label)

        self.worker = Worker()
        self.worker.signals.result.connect(self.worker_output)
        self.threadpool.start(self.worker)

        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.show()

    def draw_snake(self):
        if self.SNAKE_DIRECTION == 'RIGHT':
            self.POINT_X.pop(0)
            self.POINT_Y.pop(0)
            self.POINT_X.append(self.POINT_X[-1] + self.SNAKE_STEP)
            self.POINT_Y.append(self.POINT_Y[-1])
        if self.SNAKE_DIRECTION == 'DOWN':
            self.POINT_X.pop(0)
            self.POINT_Y.pop(0)
            self.POINT_X.append(self.POINT_X[-1])
            self.POINT_Y.append(self.POINT_Y[-1] + self.SNAKE_STEP)

        if self.SNAKE_DIRECTION == 'LEFT':
            self.POINT_X.pop(0)
            self.POINT_Y.pop(0)
            self.POINT_X.append(self.POINT_X[-1] - self.SNAKE_STEP)
            self.POINT_Y.append(self.POINT_Y[-1])

        if self.SNAKE_DIRECTION == 'UP':
            self.POINT_X.pop(0)
            self.POINT_Y.pop(0)
            self.POINT_X.append(self.POINT_X[-1])
            self.POINT_Y.append(self.POINT_Y[-1] - self.SNAKE_STEP)

        self.canvas = QPixmap(500, 500)
        self.canvas.fill(QColor('green'))
        self.label.setPixmap(self.canvas)

        self.canvas = self.label.pixmap()
        painter = QPainter(self.canvas)
        pen = QPen()
        pen.setWidth(10)
        pen.setColor(QColor('blue'))
        painter.setPen(pen)
        painter.drawPolyline([
            QPoint(self.POINT_X[0], self.POINT_Y[0]),
            QPoint(self.POINT_X[1], self.POINT_Y[1]),
            QPoint(self.POINT_X[2], self.POINT_Y[2])]
        )
        painter.end()
        self.label.setPixmap(self.canvas)

    def worker_output(self, s):
        print(s)
        self.draw_snake()

    def keyPressEvent(self, event):
        # Проверяем направление движения змеи
        result = SNAKE_DIRECTION[event.key()]  # отслеживаем нажатие на кнопку
        if self.SNAKE_DIRECTION == result:  # направление совпадает
            pass  # ничего не делаем
        elif result == 'RIGHT' and self.SNAKE_DIRECTION == 'LEFT':  # направление противоположно
            pass
        elif result == 'LEFT' and self.SNAKE_DIRECTION == 'RIGHT':  # направление противоположно
            pass
        elif result == 'DOWN' and self.SNAKE_DIRECTION == 'UP':  # направление противоположно
            pass
        elif result == 'UP' and self.SNAKE_DIRECTION == 'DOWN':  # направление противоположно
            pass
        else:  # направление можно поменять
            self.SNAKE_DIRECTION = result
            print(self.SNAKE_DIRECTION)

    def closeEvent(self, event):
        self.worker.autoDelete()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    app.exec_()
