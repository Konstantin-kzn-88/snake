# -----------------------------------------------------------
# Игра "змейка"
# 2023 Kuznetsov Konstantin
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import sys
import os
from pathlib import Path
import random

from PySide2.QtWidgets import QApplication, QMainWindow, QStyleFactory, QLabel
from PySide2.QtGui import QIcon, QPixmap, QPainter, QPen, QColor
from PySide2.QtCore import QPoint, QObject, QRunnable, Signal, QThreadPool, QThread, Qt

# Направление стрелок
SNAKE_DIRECTION = {16777236: 'RIGHT',
                   16777234: 'LEFT',
                   16777235: 'UP',
                   16777237: 'DOWN'}

# Скорость змеи (скрость отрисовки, мс)
SPEED = 150


# Класс цикла для задержки отрисовки
class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(str)
    result = Signal(str)


class Worker(QRunnable):
    def __init__(self, is_running: bool):
        super().__init__()
        self.signals = WorkerSignals()
        self.is_running = is_running

    def run(self):
        try:
            var_in_worker = 'work'
            while self.is_running:
                QThread.msleep(SPEED)
                self.signals.result.emit(var_in_worker)
        except Exception as e:
            self.signals.error.emit(str(e))


# Главное окно
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Начальные координаты змеи
        self.POINT_X = [20, 30, 40, 50, 60, 70, 80]
        self.POINT_Y = [20, 20, 20, 20, 20, 20, 20]
        self.SNAKE_DIRECTION = 'RIGHT'
        self.SNAKE_STEP = 10
        # Начальные координаты еды
        self.POINT_X_FOOD = random.randint(1, 49) * 10
        self.POINT_Y_FOOD = random.randint(1, 49) * 10

        self.threadpool = QThreadPool()

        path_ico = str(Path(os.getcwd()))
        main_ico = QIcon(path_ico + '/ico/snake.png')
        self.setWindowIcon(main_ico)

        self.init_UI()

    def init_UI(self):
        self.setFixedSize(500, 500)
        self.setWindowTitle('Snake')
        # Поле игровое
        self.label = QLabel()
        self.canvas = QPixmap(500, 500)
        self.canvas.fill(QColor('green'))
        self.label.setPixmap(self.canvas)
        self.setCentralWidget(self.label)
        self.canvas = self.label.pixmap()
        # Цикл отрисовки змеи
        self.worker = Worker(is_running=True)
        self.worker.signals.result.connect(self.worker_output)
        self.threadpool.start(self.worker)

        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.show()

    def draw_snake(self):
        # Координаты змеи
        if self.SNAKE_DIRECTION == 'RIGHT':
            self.POINT_X.append(self.POINT_X[-1] + self.SNAKE_STEP)
            self.POINT_Y.append(self.POINT_Y[-1])
        elif self.SNAKE_DIRECTION == 'DOWN':
            self.POINT_X.append(self.POINT_X[-1])
            self.POINT_Y.append(self.POINT_Y[-1] + self.SNAKE_STEP)
        elif self.SNAKE_DIRECTION == 'LEFT':
            self.POINT_X.append(self.POINT_X[-1] - self.SNAKE_STEP)
            self.POINT_Y.append(self.POINT_Y[-1])
        elif self.SNAKE_DIRECTION == 'UP':
            self.POINT_X.append(self.POINT_X[-1])
            self.POINT_Y.append(self.POINT_Y[-1] - self.SNAKE_STEP)
        # Координаты еды и условие "если змея съела еду"
        if self.POINT_X[-1] == self.POINT_X_FOOD and self.POINT_Y[-1] == self.POINT_Y_FOOD:
            self.POINT_X.append(self.POINT_X_FOOD)
            self.POINT_Y.append(self.POINT_Y_FOOD)
            self.POINT_X_FOOD = random.randint(1, 49) * 10
            self.POINT_Y_FOOD = random.randint(1, 49) * 10
        else:
            self.POINT_X.pop(0)
            self.POINT_Y.pop(0)
        # очистка поля
        self.canvas.fill(QColor('green'))
        painter = QPainter(self.canvas)
        pen = QPen()
        pen.setWidth(10)

        # нарисуем змею
        for i in range(len(self.POINT_X)):
            if i == len(self.POINT_X) - 1:
                pen.setColor(QColor('yellow'))
                painter.setPen(pen)
            else:
                pen.setColor(QColor('blue'))
                painter.setPen(pen)
            painter.drawEllipse(QPoint(self.POINT_X[i], self.POINT_Y[i]), 3, 3)

        # Нарисуем еду
        pen.setColor(QColor('red'))
        painter.setPen(pen)
        painter.drawEllipse(QPoint(self.POINT_X_FOOD, self.POINT_Y_FOOD), 3, 3)

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
        elif (result, self.SNAKE_DIRECTION) in (('RIGHT', 'LEFT'), ('LEFT', 'RIGHT'),
                                                ('DOWN', 'UP'), ('UP', 'DOWN')):  # направление противоположно
            pass  # ничего не делаем
        else:  # направление можно поменять
            self.SNAKE_DIRECTION = result

    def closeEvent(self, event):
        self.worker.is_running = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    app.exec_()
