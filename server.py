import socket



import win32api
from time import sleep
from PIL import Image
import io
import time
import pygame
from pygame.locals import *
from pynput.mouse import Listener
import numpy as np
from random import randint
import pyautogui
from threading import Thread
# PyQt5
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QAction, QMessageBox
from PyQt5.QtGui import QPixmap, QMouseEvent, QWheelEvent
from PyQt5.QtCore import QRect, Qt


print("[SERVER]: STARTED")
sock = socket.socket()
sock.bind(('192.168.0.6', 9091)) # Your Server
sock.listen()
conn, addr = sock.accept()
mouse_click = ''
scroll = 0
keyboard_pressed = ''
# def on_click(x, y, button, pressed):
#     if pressed:
#         if(str(button) == "Button.left" or str(button) == "Button.right"):
#             mouse_click = str(button)
#         else:
#             mouse_click = 'None'
#         print(mouse_click)
class Dekstop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def keyPressEvent(self, event):
        global keyboard_pressed
        keyboard_pressed = event.text()
        print(event.text())
    def mousePressEvent(self, event: QMouseEvent):
        global mouse_click
        if event.button() == Qt.LeftButton:
            #print("Left mouse clicked")
            mouse_click = "L"
        if event.button() == Qt.RightButton:
            #print("Left mouse clicked")
            mouse_click = "R"
    def wheelEvent(self, event: QWheelEvent) -> None:
        global scroll
        scroll = scroll+1
        #print("Scroll")
    def ChangeImage(self):
        try:
            print("[SERVER]: CONNECTED: {0}!".format(addr[0]))
            while True:
                global scroll
                global mouse_click
                global keyboard_pressed
                img_bytes = conn.recv(9999999)
                #print(img_bytes)
                self.pixmap.loadFromData(img_bytes)
                #self.label.setScaledContents(True)
                self.label.resize(self.width(), self.height())
                self.label.setPixmap(self.pixmap)
                # pygame.init()
                # pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                #a = win32api.GetKeyState(0x01)
                # b = win32api.GetKeyState(0x02)
                # print(b)
                # if(a!=0):
                #     print(a)
                #     click = 'L'
                data = pyautogui.position()
                send1 = str(data.x)
                send2 = str(data.y)
                # for event in pygame.event.get():
                #     if event.type == pygame.MOUSEBUTTONDOWN:
                #         if event.button == 1:
                #             click = "L"
                #         elif event.button == 2:
                #             click= "C"
                #         elif event.button == 3:
                #             click = "R"
                data = send1 + "," + send2 + "," + mouse_click + "," + keyboard_pressed + "," + str(scroll)
                mouse_click = ''
                keyboard_pressed = ''
                scroll = 0
                print(data)
                conn.send(data.encode('utf-8'))
                #sleep(1/30)
        except ConnectionResetError:
            QMessageBox.about(self, "ERROR", "[SERVER]: The remote host forcibly terminated the existing connection!")
            conn.close()

    def initUI(self):
        self.pixmap = QPixmap()
        self.label = QLabel(self)
        self.label.resize(self.width(), self.height())
        self.setGeometry(QRect(pyautogui.size()[0] // 4, pyautogui.size()[1] // 4, 1920, 1080))
        #self.setFixedSize(self.width(), self.height())
        self.showMaximized()
        self.setWindowTitle("[SERVER] Remote Desktop: " + str(randint(99999, 999999)))
        self.start = Thread(target=self.ChangeImage, daemon=True)
        self.start.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dekstop()
    ex.show()
    sys.exit(app.exec())