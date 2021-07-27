#!/usr/bin/env python3

from dotenv import load_dotenv
import socket
import pygame
import json
import time
import os

load_dotenv()
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 3000))

controllerInit, socketInit = 0, 0

clock = pygame.time.Clock()

while True:

    # Controller initialization
    if controllerInit == 0:
        try:
            pygame.init()
            pygame.joystick.init()
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
        except:
            controllerInit = 0
            print("Joystick initialization failed.")
            time.sleep(1)
        else:
            #Print joystick name & ID
            controllerInit = 1

    # Socket initialization
    if socketInit == 0:
        try:
            tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpSocket.connect((HOST, PORT))
        except:
            socketInit = 0
            print("Socket connection failed.")
            time.sleep(1)
        else:
            socketInit = 1

    # Data read from controller axes
    pygame.event.get()
    aResult, bResult = [], []
    axes = joystick.get_numaxes()
    for i in range(axes):
        axis = joystick.get_axis(i)
        aResult.append('{:>6.3f}'.format(axis))

    # Data read from controller buttons
    buttons = joystick.get_numbuttons()
    for i in range(buttons):
        button = joystick.get_button(i)
        bResult.append('{:>2}'.format(button))

    # JSON encode for socket communication
    data = json.dumps({"axis": aResult, "buttons": bResult})

    # Package transfer & Error handling
    try:
        tcpSocket.sendall(data.encode())
        statusMessage = tcpSocket.recv(1024)
    except:
        socketInit = 0
        print("Connection refused.")

    # Debug
    #print(statusMessage)
    
    # PyGame tickrate
    clock.tick(20)