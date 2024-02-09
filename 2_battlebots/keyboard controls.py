import tkinter as tk
from maestro import Controller
from Xlib import XK

keycode_to_keysym = {}
for name in dir(XK):
    if name.startswith("XK_"):
        keycode = getattr(XK, name)
        keysym = XK.keysym_to_string(keycode)
        if keysym:
            keycode_to_keysym[keycode] = keysym


MOTORS = 0
TURN = 1
# L_MOTORS = 0
# R_MOTORS = 1
BODY = 2
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

        self.l_shoulder = 6000
        self.l_bicep = 6000
        self.l_elbow = 6000
        self.l_forarm = 6000
        self.l_wrist = 6000
        self.l_fingers = 6000

        self.r_shoulder = 6000
        self.r_bicep = 6000
        self.r_elbow = 6000
        self.r_forarm = 6000
        self.r_wrist = 6000
        self.r_fingers = 6000

    def head(self, key):
        print(key.keysym)
        if key.keysym == "Up":
            self.headTurn += 200
            if self.headTurn > 7900:
                self.headTurn = 7900
            self.tango.setTarget(HEADTURN, self.headTurn)
        elif key.keysym == "Down":
            self.headTurn -= 200
            if self.headTurn < 1510:
                self.headTurn = 1510
            self.tango.setTarget(HEADTURN, self.headTurn)
        elif key.keysym == "Right":
            self.headTilt += 200
            if self.headTilt > 7900:
                self.headTilt = 7900
            self.tango.setTarget(HEADTILT, self.headTilt)
        elif key.keysym == "Left":
            self.headTilt -= 200
            if self.headTilt < 1510:
                self.headTilt = 1510
            self.tango.setTarget(HEADTILT, self.headTilt)

    def waist(self, key):
        keysym = keycode_to_keysym.get(key.keycode)
        print(keysym)

        if keysym == "Right":
            self.body += 200
            if (self.body > 7900):
                self.body = 7900
            self.tango.setTarget(BODY, self.body)
            print("waist right")
        elif keysym == "Left":
            self.body -= 200
            if (self.body < 1510):
                self.body = 1510
            self.tango.setTarget(BODY, self.body)
            print('waist left')

    def arrow(self, key):
        keysym = keycode_to_keysym.get(key.keycode)
        print(keysym)

        # backwards
        if keysym == "Down":
            self.motors += 200
            if (self.motors > 7900):
                self.motors = 7900
            print(self.motors)
            self.tango.setTarget(MOTORS, self.motors)
            # self.tango.setTarget(R_MOTORS, self.motors)

        # forwards
        elif keysym == "Up":
            self.motors -= 200
            if (self.motors < 1510):
                self.motors = 1510
            print(self.motors)
            self.tango.setTarget(MOTORS, self.motors)
            # self.tango.setTarget(R_MOTORS, self.motors)

        # right
        elif keysym == "Right":
            self.turn += 200
            if (self.turn > 7400):
                self.turn = 7400
            print(self.turn)
            self.tango.setTarget(TURN, self.turn)

        # left
        elif keysym == "Left":
            self.turn -= 200
            if (self.turn < 2110):
                self.turn = 2110
            print(self.turn)
            self.tango.setTarget(TURN, self.turn)

        # escape (estop)
        elif keysym == "Escape":
            self.default = 6000
            self.tango.setTarget(MOTORS, self.default)
            self.tango.setTarget(TURN, self.default)
            self.tango.setTarget(BODY, self.default)
            self.tango.setTarget(HEADTILT, self.default)
            self.tango.setTarget(HEADTURN, self.default)
            self.tango.setTarget(L_SHOULDER, self.default)
            self.tango.setTarget(L_BICEP, self.default)
            self.tango.setTarget(L_ELBOW, self.default)
            self.tango.setTarget(L_FORARM, self.default)
            self.tango.setTarget(L_WRIST, self.default)
            self.tango.setTarget(L_FINGERS, self.default)
            self.tango.setTarget(R_SHOULDER, self.default)
            self.tango.setTarget(R_BICEP, self.default)
            self.tango.setTarget(R_ELBOW, self.default)
            self.tango.setTarget(R_FORARM, self.default)
            self.tango.setTarget(R_WRIST, self.default)
            self.tango.setTarget(R_FINGERS, self.default)

    def l_arm(self, key):
        keysym = keycode_to_keysym.get(key.keycode)
        print(keysym)
        if keysym == "s":
            print("Shoulder")
            self.l_shoulder += 200
            if (self.l_shoulder < 2110):
                self.l_shoulder = 2110
            print(self.l_shoulder)
            self.tango.setTarget(L_SHOULDER, self.l_shoulder)
    
    def r_arm(self, key):
        print(key.keycode)
        print(key.keysym)
        match key:
            case 42:
                print("Shoulder")
            case 43:
                print("Bicep")
            case 44:
                print("Elbow")
            case 45:
                print("Forearm")
            case 46:
                print("Wrist")
            case 47:
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
win.bind('<g>', keys.l_arm)
win.bind('<h>', keys.l_arm)
win.bind('<j>', keys.l_arm)
win.bind('<k>', keys.l_arm)
win.bind('<l>', keys.l_arm) 

win.bind('<Escape>', keys.arrow)
win.mainloop()
keys = KeyControl(win)
