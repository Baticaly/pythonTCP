#!/usr/bin/env python3

from dotenv import load_dotenv
import socket
import json
import time
import os

load_dotenv()
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 3000))

socketInit = 0
controllerData =  '{}'

def failsafe():
    # Failsafe parameters & orientation fix
    print("FAILSAFE")
    controllerData = '{}'

def packageHandle(data):
    try:
        data = json.loads(data)
        axis = data.get("axis")
        buttons = data.get("buttons")
    except:
        failsafe()
        conn.close()
        print("Unexpected package, connection closed.")
        socketInit = 0
        return 0, 0
    else:
        return axis, buttons

while True:

    # Socket initialization
    if socketInit == 0:
        try:
            serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serversocket.bind((HOST, PORT))
            serversocket.listen()
            conn, addr = serversocket.accept()
        except:
            socketInit = 0
            print("No connection.")
            time.sleep(1)
        else:
            print('Connected by', addr)
            socketInit = 1

    # Package transfer & Error handling & JSON parse
    if socketInit == 1:
        try:
            data = conn.recv(1024)
            conn.sendall(data)
            controllerData = data
        except:
            socketInit = 0
            print("Connection refused.")
        else:
            axis, buttons = packageHandle(controllerData)

    print(axis)
            
            

