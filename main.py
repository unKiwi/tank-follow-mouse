# includes
# import win32api
import sys
import time
import keyboard
import mouse
import pyautogui
import random
import math
import threading

from PyQt5.QtCore import Qt, QPoint
#from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow#, QLabel, QStyle
#from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPainter, QColor#, QBrush, QPen, QPainterPath
from PyQt5.QtCore import Qt

class Struct(object): pass

# define config
conf = Struct()
conf.dist = 400
conf.newGaz = 0.4
conf.newChenille = 0.30
conf.addTankKey = "a"
conf.rmTankKey = "e"
conf.color = Struct()
conf.color.contrast = 20
conf.color.chenille = Struct()
conf.color.chenille.r = 55
conf.color.chenille.g = 56
conf.color.chenille.b = 62
conf.color.canon = QColor(34, 37, 42)

# def getFps():
#     device = win32api.EnumDisplayDevices()
#     settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
#     return getattr(settings, 'DisplayFrequency')

# def rebond(angleIncident, angleWall):
#     print(angleIncident, angleWall)

def distance(position1, position2):
    return math.sqrt(math.pow(position1.x - position2.x, 2) + math.pow(position1.y - position2.y, 2))

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
        # define speed
        self.speed = Struct()
        self.speed.translate = 120
        self.speed.rotate = Struct()
        self.speed.rotate.body = 90
        self.speed.rotate.canon = 120
        # define color
        self.color = Struct()
        self.color.r = random.randint(conf.color.contrast, 255 - conf.color.contrast)
        self.color.g = random.randint(conf.color.contrast, 255 - conf.color.contrast)
        self.color.b = random.randint(conf.color.contrast, 255 - conf.color.contrast)
        # rest
        self.mode = mode
        self.gaz = []

class Chenille:
    def __init__(self, direction, pos):
        self.direction = direction
        self.pos = pos
        self.opacity = 255

class Gaz:
    def __init__(self, direction, pos):
        self.direction = direction
        self.pos = pos
        self.size = 30
        self.speed = 60
        self.hide = 30

class Obus:
    def __init__(self, direction, pos):
        self.direction = direction
        self.pos = pos
        self.nbRebond = 1
        self.speed = 500

# var
fps = 144#getFps()
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
tankShape.canon.silencieux.width = 18

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
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_NoChildEventsForParent, True)
        self.setWindowFlags(Qt.Window | Qt.X11BypassWindowManagerHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)

        self.setGeometry(0, 0, pyautogui.size().width, pyautogui.size().height)

        self.paintEvent(self)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        # draw chenille
        for chenille in lsChenille:
            painter.translate(chenille.pos.x, chenille.pos.y)
            painter.rotate(chenille.direction)

            painter.setBrush(QColor(conf.color.chenille.r, conf.color.chenille.g, conf.color.chenille.b, int(chenille.opacity)))
            ######################################################################
            painter.drawRect(int(unit * -tankShape.body.chenille.width / 2), int(unit * tankShape.body.chenille.length / 2 - 1), int(unit * (tankShape.body.chenille.width - tankShape.body.gardeBoue.width) / 2), int(unit * 3))
            painter.drawRect(int(unit * +tankShape.body.chenille.width / 2), int(unit * tankShape.body.chenille.length / 2 - 1), int(unit * -(tankShape.body.chenille.width - tankShape.body.gardeBoue.width) / 2), int(unit * 3))
            
            painter.rotate(-chenille.direction)
            painter.translate(-chenille.pos.x, -chenille.pos.y)

        # draw obus
        for obus in lsObus:
            painter.translate(obus.pos.x, obus.pos.y)
            painter.rotate(obus.direction)

            painter.setBrush(QColor(248, 244, 244))
            painter.drawEllipse(int(unit * (-tankShape.canon.fut.width / 2)), int(unit * (-tankShape.canon.cabine.length / 2 + -tankShape.canon.fut.length + -tankShape.canon.fut.width / 2)), int(unit * tankShape.canon.fut.width), int(unit * tankShape.canon.fut.width))
            painter.drawRect(int(unit * (-tankShape.canon.fut.width / 2)), int(unit * (-tankShape.canon.cabine.length / 2 + -tankShape.canon.fut.length + tankShape.canon.fut.width / 8)), int(unit * tankShape.canon.fut.width), int(unit * tankShape.canon.fut.width))

            painter.rotate(-obus.direction)
            painter.translate(-obus.pos.x, -obus.pos.y)

        # draw all tank
        for tank in lsTank:
            # draw gaz
            painter.setBrush(QColor(tank.color.r + conf.color.contrast, tank.color.g + conf.color.contrast, tank.color.b + conf.color.contrast))
            for gaz in tank.gaz:
                painter.translate(gaz.pos.x, gaz.pos.y)
                painter.rotate(gaz.direction)

                painter.drawEllipse(int(unit * (tankShape.body.chenille.width / 5 + -gaz.size / 2)), int(unit * (-tankShape.body.chenille.length / 2 + -gaz.size / 2)), int(unit * gaz.size), int(unit * gaz.size))
                
                painter.rotate(-gaz.direction)
                painter.translate(-gaz.pos.x, -gaz.pos.y)

            # draw tank
            painter.translate(tank.pos.x, tank.pos.y)
            painter.rotate(tank.direction.body)

            # draw body
            painter.setBrush(QColor(conf.color.chenille.r, conf.color.chenille.g, conf.color.chenille.b))
            dimen = tankShape.body.chenille
            painter.drawRect(int(-unit * dimen.width / 2), int(-unit * dimen.length / 2), int(unit * dimen.width), int(unit * dimen.length))
            painter.setBrush(QColor(tank.color.r + conf.color.contrast, tank.color.g + conf.color.contrast, tank.color.b + conf.color.contrast))
            dimen = tankShape.body.gardeBoue
            painter.drawRect(int(-unit * dimen.width / 2), int(-unit * dimen.length / 2), int(unit * dimen.width), int(unit * dimen.length))
            painter.setBrush(QColor(tank.color.r, tank.color.g, tank.color.b))
            dimen = tankShape.body.cabine
            painter.drawRect(int(-unit * dimen.width / 2), int(-unit * dimen.length / 2), int(unit * dimen.width), int(unit * dimen.length))

            painter.rotate(tank.direction.canon - tank.direction.body)

            # draw canon
            painter.setBrush(QColor(tank.color.r - conf.color.contrast, tank.color.g - conf.color.contrast, tank.color.b - conf.color.contrast))
            dimen = tankShape.canon.cabine
            painter.drawRect(int(-unit * dimen.width / 2), int(-unit * dimen.length / 2), int(unit * dimen.width), int(unit * dimen.length))
            painter.setBrush(conf.color.canon)
            dimen = tankShape.canon.fut
            painter.drawRect(int(-unit * dimen.width / 2), int(-unit * (dimen.length + tankShape.canon.cabine.length / 2)), int(unit * dimen.width), int(unit * dimen.length))
            painter.setBrush(QColor(tank.color.r + conf.color.contrast, tank.color.g + conf.color.contrast, tank.color.b + conf.color.contrast))
            dimen = tankShape.canon.silencieux
            painter.drawRect(int(-unit * dimen.width / 2), int(-unit * (dimen.length / 2 + tankShape.canon.cabine.length / 2 + tankShape.canon.fut.length)), int(unit * dimen.width), int(unit * dimen.length))

            painter.rotate(-(tank.direction.canon - tank.direction.body))
            painter.rotate(-tank.direction.body)
            painter.translate(-tank.pos.x, -tank.pos.y)

    def my_operations(self):
        lastTank = 0
        for i in range(len(lsTank)):
            # update tank
            mousePos = 0
            if (lsTank[i].mode == "player"):
                mousePos = pyautogui.position()
            else:
                mousePos = lsTank[lastTank].pos
            lsTank[i].direction.mouse = getMouseDirection(lsTank[i].pos, mousePos)

            # rotate canon
            difAngle = lsTank[i].direction.mouse - lsTank[i].direction.canon
            difAngle = (difAngle + 180) % 360 - 180
            rotate = lsTank[i].speed.rotate.canon / fps
            if (difAngle < -rotate):
                lsTank[i].direction.canon -= rotate
            elif (difAngle > rotate):
                lsTank[i].direction.canon += rotate
            else:
                lsTank[i].direction.canon = lsTank[i].direction.mouse
            
            if (lsTank[i].direction.canon < 0):
                lsTank[i].direction.canon = 359
            elif (lsTank[i].direction.canon > 359):
                lsTank[i].direction.canon = 0

            if (distance(mousePos, lsTank[i].pos) > conf.dist):
                # rotate body
                difAngle = lsTank[i].direction.mouse - lsTank[i].direction.body
                difAngle = (difAngle + 180) % 360 - 180
                rotate = lsTank[i].speed.rotate.body / fps
                if (difAngle < -rotate):
                    lsTank[i].direction.body -= rotate
                    lsTank[i].direction.canon -= rotate
                elif (difAngle > rotate):
                    lsTank[i].direction.body += rotate
                    lsTank[i].direction.canon += rotate
                else:
                    lsTank[i].direction.body = lsTank[i].direction.mouse

                if (lsTank[i].direction.body < 0):
                    lsTank[i].direction.body = 359
                elif (lsTank[i].direction.body > 359):
                    lsTank[i].direction.body = 0

                # tank forward
                moveX = math.sin(math.radians(lsTank[i].direction.body)) * unit * lsTank[i].speed.translate / fps
                moveY = math.cos(math.radians(lsTank[i].direction.body)) * unit * lsTank[i].speed.translate / fps
                lsTank[i].pos.x += moveX
                lsTank[i].pos.y -= moveY

            # gaz
            for j in range(len(lsTank[i].gaz)):
                moveX = math.sin(math.radians(lsTank[i].gaz[j].direction)) * unit * lsTank[i].gaz[j].speed / fps
                moveY = math.cos(math.radians(lsTank[i].gaz[j].direction)) * unit * lsTank[i].gaz[j].speed / fps
                lsTank[i].gaz[j].pos.x += moveX
                lsTank[i].gaz[j].pos.y -= moveY
                lsTank[i].gaz[j].size -= lsTank[i].gaz[j].hide / fps
            if (len(lsTank[i].gaz) > 0):
                if (lsTank[i].gaz[0].size <= 0):
                    lsTank[i].gaz.pop(0)

            lastTank = i

        # chenille
        for i in range(len(lsChenille)):
            lsChenille[i].opacity -= 10 / fps
        if (len(lsChenille) > 0):
            if (lsChenille[0].opacity <= 0):
                lsChenille.pop(0)

        # obus
        for i in range(len(lsObus)):
            # move
            moveX = math.sin(math.radians(lsObus[i].direction)) * unit * lsObus[i].speed / fps
            moveY = math.cos(math.radians(lsObus[i].direction)) * unit * lsObus[i].speed / fps
            lsObus[i].pos.x += moveX
            lsObus[i].pos.y -= moveY

            # rebond
            # if (lsObus[i].nbRebond <= 0):
                # lsObus.pop(i)
                # break
            
            if (lsObus[i].pos.x < 0 or lsObus[i].pos.x > pyautogui.size().width):
            #     lsObus[i].direction = rebond(lsObus[i].direction, 0)
                lsObus.pop(i)
                break
            elif (lsObus[i].pos.y < 0 or lsObus[i].pos.y > pyautogui.size().height):
            #     lsObus[i].direction = rebond(lsObus[i].direction, 90)
                lsObus.pop(i)
                break
            
            # lsObus[i].nbRebond -= 1

        self.update()

# traitement
lsTank.append(Tank("player"))

app = QApplication(sys.argv)
w = Invisible()
w.show()

# redraw interval
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

set_interval(func, 1 / fps)

# gaz interval
def func2():
    for i in range(len(lsTank)):
        # direction
        direction = lsTank[i].direction.body - 180
        if (direction < 0):
            direction = 360 + direction

        # pos
        pos = Struct()
        pos.x = lsTank[i].pos.x
        pos.y = lsTank[i].pos.y

        # append
        lsTank[i].gaz.append(Gaz(direction, pos))

def set_interval2(func2, sec):
    def func_wrapper2():
        set_interval2(func2, sec)
        func2()
    t = threading.Timer(sec, func_wrapper2)
    t.start()
    return t

set_interval2(func2, conf.newGaz)

# chenille interval
def func3():
    for i in range(len(lsTank)):
        # direction
        direction = lsTank[i].direction.body

        # pos
        pos = Struct()
        pos.x = lsTank[i].pos.x
        pos.y = lsTank[i].pos.y

        # append
        lsChenille.append(Chenille(direction, pos))

def set_interval3(func3, sec):
    def func_wrapper3():
        set_interval3(func3, sec)
        func3()
    t = threading.Timer(sec, func_wrapper3)
    t.start()
    return t

set_interval3(func3, conf.newChenille)


def onClick():
    # add an obus for each tank
    for tank in lsTank:
        # direction
        direction = tank.direction.canon

        # pos
        pos = Struct()
        pos.x = tank.pos.x
        pos.y = tank.pos.y

        lsObus.append(Obus(direction, pos))

mouse.on_click(lambda: onClick())

def onKeyDown():
    while True:
        key = keyboard.read_key()
        key = key.lower()
        if key == conf.addTankKey:
            lsTank.append(Tank("ia"))
        elif key == conf.rmTankKey and len(lsTank) > 1:
            lsTank.pop()
        
        time.sleep(1)
tKeyDown = threading.Thread(target=onKeyDown)
tKeyDown.setDaemon(True)
tKeyDown.start()

app.exec_()