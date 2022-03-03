# includes
import win32api
import sys
import time
import pyautogui
import random
import math
import threading

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QStyle
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPainterPath
from PyQt5.QtCore import Qt

def getFps():
    device = win32api.EnumDisplayDevices()
    settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
    return getattr(settings, 'DisplayFrequency')

def getUnit(fraction):
    width = 0
    if (pyautogui.size().width >= pyautogui.size().height):
        width = pyautogui.size().height
    else:
        width = pyautogui.size().width
    return width * fraction

def getMouseDirection(pos, pos2):
    mousePos = pos2
    xIsSup = mousePos.x >= pos.x
    yIsSup = mousePos.y >= pos.y
    
    angle = 0
    if (xIsSup and yIsSup):
        angle = 90 + abs(math.atan((mousePos.y - pos.y) / (pos.x - mousePos.x + 0.1)) * 180 / math.pi)
    if (xIsSup == False and yIsSup):
        angle = 270 + math.atan((mousePos.y - pos.y) / (mousePos.x - pos.x + 0.1)) * 180 / math.pi
    if (xIsSup and yIsSup == False):
        angle = 90 - math.atan((pos.y - mousePos.y) / (mousePos.x - pos.x + 0.1)) * 180 / math.pi
    if (xIsSup == False and yIsSup == False):
        angle = 270 + math.atan((pos.y - mousePos.y) / (pos.x - mousePos.x + 0.1)) * 180 / math.pi
    return int(angle)

class Struct(object): pass

class Tank():
    def __init__(self, mode):
        # define pos
        self.pos = Struct()
        self.pos.x = random.randint(0, pyautogui.size().width)
        self.pos.y = random.randint(0, pyautogui.size().height)
        # define direction
        self.direction = Struct()
        self.direction.mouse = random.randint(0, 359)
        self.direction.body = random.randint(0, 359)
        self.direction.canon = random.randint(0, 359)
        # define color
        self.color = Struct()
        self.color.r = random.randint(15, 240)
        self.color.g = random.randint(15, 240)
        self.color.b = random.randint(15, 240)
        # rest
        self.mode = mode
        self.gaz = []
        self.speed = 1

class Chenille:
    def __init__(self, direction, pos):
        self.direction = direction
        self.pos = pos

class Gaz:
    def __init__(self, direction, pos):
        self.direction = direction
        self.pos = pos
        self.size = 30

# var
fps = getFps()
unit = getUnit(0.1 / 100)

# define tank shape
tankShape = Struct()
tankShape.body = Struct()
tankShape.body.chenille = Struct()
tankShape.body.chenille.length = 120
tankShape.body.chenille.width = 100
tankShape.body.gardeBoue = Struct()
tankShape.body.gardeBoue.length = tankShape.body.chenille.length
tankShape.body.gardeBoue.width = 65
tankShape.body.cabine = Struct()
tankShape.body.cabine.length = 80
tankShape.body.cabine.width = tankShape.body.gardeBoue.width
tankShape.canon = Struct()
tankShape.canon.cabine = Struct()
tankShape.canon.cabine.length = 50
tankShape.canon.cabine.width = 40
tankShape.canon.fut = Struct()
tankShape.canon.fut.length = 50
tankShape.canon.fut.width = 12
tankShape.canon.silencieux = Struct()
tankShape.canon.silencieux.length = 10
tankShape.canon.silencieux.width = 20

lsTank = []
lsChenille = []
lsObus = []
lsBomb = []

class Invisible(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__press_pos = QPoint()

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

        # draw all tank
        for tank in lsTank:
            painter.translate(tank.pos.x, tank.pos.y)
            painter.rotate(tank.direction.body)

            # draw body
            painter.setBrush(QColor(55, 56, 62))
            dimen = tankShape.body.chenille
            painter.drawRect(int(-unit * dimen.width / 2), int(-unit * dimen.length / 2), int(unit * dimen.width), int(unit * dimen.length))
            painter.setBrush(QColor(tank.color.r + 15, tank.color.g + 15, tank.color.b + 15))
            dimen = tankShape.body.gardeBoue
            painter.drawRect(int(-unit * dimen.width / 2), int(-unit * dimen.length / 2), int(unit * dimen.width), int(unit * dimen.length))
            painter.setBrush(QColor(tank.color.r, tank.color.g, tank.color.b))
            dimen = tankShape.body.cabine
            painter.drawRect(int(-unit * dimen.width / 2), int(-unit * dimen.length / 2), int(unit * dimen.width), int(unit * dimen.length))

            painter.rotate(tank.direction.canon - tank.direction.body)

            # draw canon
            painter.setBrush(QColor(tank.color.r - 15, tank.color.g - 15, tank.color.b - 15))
            dimen = tankShape.canon.cabine
            painter.drawRect(int(-unit * dimen.width / 2), int(-unit * dimen.length / 2), int(unit * dimen.width), int(unit * dimen.length))
            painter.setBrush(QColor(34, 37, 42))
            dimen = tankShape.canon.fut
            painter.drawRect(int(-unit * dimen.width / 2), int(-unit * (dimen.length + tankShape.canon.cabine.length / 2)), int(unit * dimen.width), int(unit * dimen.length))
            painter.setBrush(QColor(tank.color.r + 15, tank.color.g + 15, tank.color.b + 15))
            dimen = tankShape.canon.silencieux
            painter.drawRect(int(-unit * dimen.width / 2), int(-unit * (dimen.length / 2 + tankShape.canon.cabine.length / 2 + tankShape.canon.fut.length)), int(unit * dimen.width), int(unit * dimen.length))

            painter.rotate(-(tank.direction.canon - tank.direction.body))
            painter.rotate(-tank.direction.body)
            painter.translate(-tank.pos.x, -tank.pos.y)

    def my_operations(self):
        for i in range(len(lsTank)):
            # update tank
            lsTank[i].direction.mouse = getMouseDirection(lsTank[i].pos, pyautogui.position())
            # rotate canon
            difAngle = lsTank[i].direction.mouse - lsTank[i].direction.canon
            difAngle = (difAngle + 180) % 360 - 180
            if (difAngle < 3):
                lsTank[i].direction.canon -= 1
            elif (difAngle > 3):
                lsTank[i].direction.canon += 1
            
            if (lsTank[i].direction.canon < 0):
                lsTank[i].direction.canon = 359
            elif (lsTank[i].direction.canon > 359):
                lsTank[i].direction.canon = 0

            mousePos = pyautogui.position()
            if (math.pow(mousePos.x - lsTank[i].pos.x, 2) + math.pow(mousePos.y - lsTank[i].pos.y, 2) > math.pow(unit * 150, 2)):
                # rotate body
                difAngle = lsTank[i].direction.mouse - lsTank[i].direction.body
                difAngle = (difAngle + 180) % 360 - 180
                if (difAngle < 3):
                    lsTank[i].direction.body -= 1
                    lsTank[i].direction.canon -= 1
                elif (difAngle > 3):
                    lsTank[i].direction.body += 1
                    lsTank[i].direction.canon += 1

                if (lsTank[i].direction.body < 0):
                    lsTank[i].direction.body = 359
                elif (lsTank[i].direction.body > 359):
                    lsTank[i].direction.body = 0

                # tank forward
                moveX = math.sin(math.radians(lsTank[i].direction.body)) * unit
                moveY = math.cos(math.radians(lsTank[i].direction.body)) * unit
                lsTank[i].pos.x += moveX
                lsTank[i].pos.y -= moveY

        self.update()

# traitement
lsTank.append(Tank("player"))
# lsTank.append(Tank("ia"))

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

# class Invisible(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.__press_pos = QPoint()

#         # set window pos
#         self.top = tank.pos.y
#         self.left = tank.pos.x

#         self.initUI()

#     def initUI(self):
#         self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
#         self.setAttribute(Qt.WA_TranslucentBackground)

#         self.setGeometry(0, 0, pyautogui.size().width, pyautogui.size().height)

#         self.paintEvent(self)

#     def paintEvent(self, event):

#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)
#         painter.setPen(Qt.NoPen)
#         painter.translate(tank.pos.x, tank.pos.y)

#         # draw body
#         painter.rotate(tank.direction.body)
#         painter.setBrush(QColor(55, 56, 62))
#         painter.drawRect(-unit * 25, -unit * 30, unit * 50, unit * 60)
#         painter.setBrush(QColor(tank.color.r + 15, tank.color.g + 15, tank.color.b + 15))
#         painter.drawRect(-unit * 16, -unit * 30, unit * 32, unit * 60)
#         painter.setBrush(QColor(tank.color.r, tank.color.g, tank.color.b))
#         painter.drawRect(-unit * 16, -unit * 19, unit * 32, unit * 38)

#         # draw canon
#         painter.rotate(tank.direction.canon - tank.direction.body)
#         painter.setBrush(QColor(tank.color.r - 15, tank.color.g - 15, tank.color.b - 15))
#         painter.drawRect(-unit * 10, -unit * 12, unit * 20, unit * 24)
#         painter.setBrush(QColor(34, 37, 42))
#         painter.drawRect(-unit * 3, -unit * 12, unit * 6, -unit * 24)
#         painter.setBrush(QColor(tank.color.r + 15, tank.color.g + 15, tank.color.b + 15))
#         painter.drawRect(-unit * 5, -unit * 36, unit * 10, -unit * 6)

#         painter.rotate(-(tank.direction.canon - tank.direction.body))
#         painter.rotate(-tank.direction.body)
#         painter.translate(-tank.pos.x, -tank.pos.y)

#         # draw gaz
#         for gaz in tank.gaz:
#             painter.drawEllipse(int(-gaz.pos.x - gaz.size / 2), int(gaz.pos.y - gaz.size / 2), int(gaz.size), int(gaz.size))

#     def my_operations(self):
#         # update tank
#         setMouseDirection()
#         # rotate canon
#         difAngle = tank.direction.mouse - tank.direction.canon
#         difAngle = (difAngle + 180) % 360 - 180
#         if (difAngle < 3):
#             tank.direction.canon -= 1
#         elif (difAngle > 3):
#             tank.direction.canon += 1
        
#         if (tank.direction.canon < 0):
#             tank.direction.canon = 359
#         elif (tank.direction.canon > 359):
#             tank.direction.canon = 0

#         # gaz
#         for gaz in tank.gaz:
#             gaz.size -= 0.1
#             if (gaz.size <= 0):
#                 tank.gaz.pop(0)
#         if (len(tank.gaz) == 0):
#             pos = Struct()
#             moveX = math.sin(math.radians(tank.direction.body)) * unit * 10
#             moveY = math.cos(math.radians(tank.direction.body)) * unit * 42
#             pos.x = tank.pos.x + moveX
#             pos.y = tank.pos.y + moveY
#             direction = tank.direction.body - 180
#             if (direction < 0):
#                 direction = 360 - direction
#             tank.gaz.append(Gaz(direction, pos))

#         mousePos = pyautogui.position()
#         if (math.pow(mousePos.x - tank.pos.x, 2) + math.pow(mousePos.y - tank.pos.y, 2) > math.pow(unit * 150, 2)):
#             # rotate body
#             difAngle = tank.direction.mouse - tank.direction.body
#             difAngle = (difAngle + 180) % 360 - 180
#             if (difAngle < 3):
#                 tank.direction.body -= 1
#                 tank.direction.canon -= 1
#             elif (difAngle > 3):
#                 tank.direction.body += 1
#                 tank.direction.canon += 1

#             if (tank.direction.body < 0):
#                 tank.direction.body = 359
#             elif (tank.direction.body > 359):
#                 tank.direction.body = 0

#             # tank forward
#             moveX = math.sin(math.radians(tank.direction.body)) * unit
#             moveY = math.cos(math.radians(tank.direction.body)) * unit
#             tank.pos.x += moveX
#             tank.pos.y -= moveY

#         self.update()