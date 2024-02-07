import tkinter as tk
from maestro import Controller                                                     

BODY = 0
L_MOTORS = 1
R_MOTORS = 2
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

class KeyControl():
    def __init__(self,win):
        self.root = win
        self.tango = Controller()
        self.body = 6000
        self.headTurn = 6000
        self.headTilt = 6000
        self.motors = 6000
        self.turn = 6000
        
    def head(self,key):
        print(key.keycode)
        if key.keycode == 38:
            self.headTurn += 200
            if(self.headTurn > 7900):
                self.headTurn = 7900
            self.tango.setTarget(HEADTURN, self.headTurn)
        elif key.keycode ==40:
            self.headTurn -= 200
            if(self.headTurn < 1510):
                self.headTurn = 1510
            self.tango.setTarget(HEADTURN, self.headTurn)
        elif key.keycode == 25:
            self.headTilt += 200
            if(self.headTilt > 7900):
                self.headTilt = 7900
            self.tango.setTarget(HEADTILT, self.headTilt)
        elif key.keycode == 39:
            self.headTilt -= 200
            if(self.headTilt < 1510):
                self.headTilt = 1510
            self.tango.setTarget(HEADTILT, self.headTilt)

    def waist(self, key):
        print(key.keycode)
        
        if key.keycode == 54:
            self.body += 200
            if(self.body > 7900):
                self.body = 7900
            self.tango.setTarget(BODY, self.body)
            print("waist right")
        elif key.keycode == 52:
            self.body -= 200
            if(self.body < 1510):
                self.body = 1510
            self.tango.setTarget(BODY, self.body)
            print ('waist left')

    def arrow(self, key):
        print(key.keycode)
        if key.keycode == 116:
            self.motors += 200
            if(self.motors > 7900):
                self.motors = 7900
            print(self.motors)
            self.tango.setTarget(MOTORS, self.motors)
        elif key.keycode == 111:
            self.motors -= 200
            if(self.motors < 1510):
                self.motors = 1510
            print(self.motors)
            self.tango.setTarget(MOTORS, self.motors)
        elif key.keycode == 114:
            self.turn += 200
            if(self.turn > 7400):
                self.turn = 7400
            print(self.turn)
            self.tango.setTarget(TURN, self.turn)
        elif key.keycode == 113:
            self.turn -= 200
            if(self.turn <2110):
                self.turn = 2110
            print(self.turn)
            self.tango.setTarget(TURN, self.turn)
        
        elif key.keycode == 9:
            self.motors = 6000
            self.turn = 6000
            self.tango.setTarget(MOTORS, self.motors)
            self.tango.setTarget(TURN, self.turn)
            exit

    def l_arm(self, key):
        print(key.keycode)
        if key.keycode == 29:
            print("Shoulder")
        elif key.keycode == 30:
            print("Bicep")
        elif key.keycode == 31:
            print("Elbow")
        elif key.keycode == 32:
            print("Forearm")
        elif key.keycode == 33:
            print("Wrist")
        elif key.keycode == 34:
            print("claw")
    
    def r_arm(self, key):
        print(key.keycode)
        if key.keycode == 42:
            print("Shoulder")
        elif key.keycode == 43:
            print("Bicep")
        elif key.keycode == 44:
            print("Elbow")
        elif key.keycode == 45:
            print("Forearm")
        elif key.keycode == 46:
            print("Wrist")
        elif key.keycode == 47:
            print("claw")

win = tk.Tk()
keys = KeyControl(win)

# Movement and Escape
win.bind('<Up>', keys.arrow)
win.bind('<Left>', keys.arrow)
win.bind('<Down>', keys.arrow)
win.bind('<Right>', keys.arrow)
win.bind('<space>', keys.arrow)

# Waist
win.bind('<z>', keys.waist)
win.bind('<c>', keys.waist)

# Head
win.bind('<w>', keys.head)
win.bind('<s>', keys.head)
win.bind('<a>', keys.head)
win.bind('<d>', keys.head)

# Left arm
win.bind('<y>', keys.l_arm)
win.bind('<u>', keys.l_arm)
win.bind('<i>', keys.l_arm)
win.bind('<o>', keys.l_arm)
win.bind('<p>', keys.l_arm)

# Right arm
win.bind('<h>', keys.r_arm)
win.bind('<j>', keys.r_arm)
win.bind('<k>', keys.r_arm)
win.bind('<l>', keys.r_arm)
win.bind('<;>', keys.r_arm)
win.bind('<esc>', keys.arrow)
win.mainloop()
keys = KeyControl(win)
