# includes
import sys
import time
import pyautogui
import random
import math
import threading

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow #, QLabel, QStyle
#from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPainter, QColor #, QBrush, QPen, QPainterPath
from PyQt5.QtCore import Qt

class Struct(object): pass

def setMouseDirection():
    mousePos = pyautogui.position()
    xIsSup = mousePos.x >= tank.pos.x
    yIsSup = mousePos.y >= tank.pos.y
    if (xIsSup and yIsSup):
        tank.direction.mouse = 90 + abs(math.atan((mousePos.y - tank.pos.y) / (tank.pos.x - mousePos.x + 0.1)) * 180 / math.pi)
    elif (xIsSup == False and yIsSup):
        tank.direction.mouse = 270 + math.atan((mousePos.y - tank.pos.y) / (mousePos.x - tank.pos.x + 0.1)) * 180 / math.pi
    elif (xIsSup and yIsSup == False):
        tank.direction.mouse = 90 - math.atan((tank.pos.y - mousePos.y) / (mousePos.x - tank.pos.x + 0.1)) * 180 / math.pi
    elif (xIsSup == False and yIsSup == False):
        tank.direction.mouse = 270 + math.atan((tank.pos.y - mousePos.y) / (tank.pos.x - mousePos.x + 0.1)) * 180 / math.pi

    tank.direction.mouse = int(tank.direction.mouse)

# define conf
conf = Struct()
conf.windowSize = 20 / 100

# define dimen
dimen = Struct()
if (pyautogui.size()[0] >= pyautogui.size()[1]):
    dimen.tankArea = int(pyautogui.size().height * conf.windowSize)
else:
    dimen.tankArea = int(pyautogui.size().width * conf.windowSize)
dimen.unit = int(dimen.tankArea / 100)

# create tank
tank = Struct()
# define pos
tank.pos = Struct()
tank.pos.x = int(pyautogui.size().width * random.random())
tank.pos.y = int(pyautogui.size().height * random.random())
# define direction
tank.direction = Struct()
tank.direction.body = random.randint(0, 359)
tank.direction.canon = random.randint(0, 359)
setMouseDirection()
# define color
tank.color = Struct()
tank.color.r = random.randint(15, 240)
tank.color.g = random.randint(15, 240)
tank.color.b = random.randint(15, 240)

class Invisible(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__press_pos = QPoint()

        # set window pos
        self.top = tank.pos.y
        self.left = tank.pos.x

        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setGeometry(0, 0, pyautogui.size().width, pyautogui.size().height)

        self.paintEvent(self)

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.translate(tank.pos.x, tank.pos.y)

        # draw body
        painter.rotate(tank.direction.body)
        painter.setBrush(QColor(55, 56, 62))
        painter.drawRect(-dimen.unit * 25, -dimen.unit * 30, dimen.unit * 50, dimen.unit * 60)
        painter.setBrush(QColor(tank.color.r + 15, tank.color.g + 15, tank.color.b + 15))
        painter.drawRect(-dimen.unit * 16, -dimen.unit * 30, dimen.unit * 32, dimen.unit * 60)
        painter.setBrush(QColor(tank.color.r, tank.color.g, tank.color.b))
        painter.drawRect(-dimen.unit * 16, -dimen.unit * 19, dimen.unit * 32, dimen.unit * 38)

        # draw canon
        painter.rotate(tank.direction.canon - tank.direction.body)
        painter.setBrush(QColor(tank.color.r - 15, tank.color.g - 15, tank.color.b - 15))
        painter.drawRect(-dimen.unit * 10, -dimen.unit * 12, dimen.unit * 20, dimen.unit * 24)
        painter.setBrush(QColor(34, 37, 42))
        painter.drawRect(-dimen.unit * 3, -dimen.unit * 12, dimen.unit * 6, -dimen.unit * 24)
        painter.setBrush(QColor(tank.color.r + 15, tank.color.g + 15, tank.color.b + 15))
        painter.drawRect(-dimen.unit * 5, -dimen.unit * 36, dimen.unit * 10, -dimen.unit * 6)

        painter.rotate(-(tank.direction.canon - tank.direction.body))
        painter.rotate(-tank.direction.body)
        painter.translate(-tank.pos.x, -tank.pos.y)

        painter.setBrush(QColor(55, 56, 62))
        painter.drawRect(-dimen.unit * 25, -dimen.unit * 30, dimen.unit * 50, dimen.unit * 60)

    def my_operations(self):
        # update tank
        setMouseDirection()
        # rotate canon
        difAngle = tank.direction.mouse - tank.direction.canon
        difAngle = (difAngle + 180) % 360 - 180
        if (difAngle < 3):
            tank.direction.canon -= 1
        elif (difAngle > 3):
            tank.direction.canon += 1
        # rotate body
        difAngle = tank.direction.mouse - tank.direction.body
        difAngle = (difAngle + 180) % 360 - 180
        if (difAngle < 3):
            tank.direction.body -= 1
            tank.direction.canon -= 1
        elif (difAngle > 3):
            tank.direction.body += 1
            tank.direction.canon += 1

        if (tank.direction.body < 0):
            tank.direction.body = 359
        elif (tank.direction.body > 359):
            tank.direction.body = 0
        if (tank.direction.canon < 0):
            tank.direction.canon = 359
        elif (tank.direction.canon > 359):
            tank.direction.canon = 0

        mousePos = pyautogui.position()
        if (math.pow(mousePos.x - tank.pos.x, 2) + math.pow(mousePos.y - tank.pos.y, 2) > math.pow(dimen.unit * 100, 2)):
            # tank forward
            moveX = math.sin(math.radians(tank.direction.body)) * dimen.unit
            moveY = math.cos(math.radians(tank.direction.body)) * dimen.unit
            tank.pos.x += moveX
            tank.pos.y -= moveY

        self.update()

app = QApplication(sys.argv)
w = Invisible()
w.show()

def func():
    t = threading.Thread(target=w.my_operations)
    t.start()

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

set_interval(func, 0.01)

app.exec_()