import tkinter as tk
from maestro import Controller 

#Channels
BODY = 0
MOTORS = 1
TURN = 2
HEADTURN = 3
HEADTILT = 4
R_SHOULDER = 5
R_BICEP = 6
R_ELBOW = 7
R_FORARM = 8
R_WRIST = 9
R_FINGERS = 10
L_SHOULDER = 11
L_BICEP = 12
L_ELBOW = 13
L_FORARM = 14
L_WRIST = 15
L_FINGERS = 16

self.root = win
self.tango = Controller()

def moveServo(self):  
    self.L_BICEP = 6500
    self.tango.setTarget(L_BICEP, self.headTilt)
