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


#MOTORS = 0
#TURN = 1
L_MOTORS = 1
R_MOTORS = 0
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
        self.r_motors = 6000
        self.l_motors = 6000
        #self.motors = 6000
        #self.turn = 6000

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
        print(key.keycode)
        print(key.keysym)
        match key:
            case 38:
                self.headTurn += 200
                if self.headTurn > 7900:
                    self.headTurn = 7900
                self.tango.setTarget(HEADTURN, self.headTurn)
            case 40:
                self.headTurn -= 200
                if self.headTurn < 1510:
                    self.headTurn = 1510
                self.tango.setTarget(HEADTURN, self.headTurn)
            case 25:
                self.headTilt += 200
                if self.headTilt > 7900:
                    self.headTilt = 7900
                self.tango.setTarget(HEADTILT, self.headTilt)
            case 39:
                self.headTilt -= 200
                if self.headTilt < 1510:
                    self.headTilt = 1510
                self.tango.setTarget(HEADTILT, self.headTilt)

    def waist(self, key):
        keysym = keycode_to_keysym.get(key.keycode)
        print(key.keycode)
        print(keysym)

        match key.keycode:
            case 54:
                self.body += 200
                if (self.body > 7900):
                    self.body = 7900
                self.tango.setTarget(BODY, self.body)
                print("waist right")
            case 52:
                self.body -= 200
                if (self.body < 1510):
                    self.body = 1510
                self.tango.setTarget(BODY, self.body)
                print('waist left')

    def arrow(self, key):
        keysym = keycode_to_keysym.get(key.keycode)
        print(key.keycode)
        print(keysym)

        match key.keycode:
            # backwards
            case 111:
                if self.l_motors == 6000:
                    self.r_motors = 6400
                    self.l_motors = 5800
                else:
                    self.l_motors -= 200
                    if self.r_motors > 7900:
                        self.r_motors = 7900
                    # Increment speed by 200 in the forward direction
                    self.r_motors += 200

                print(self.r_motors)
                print(self.l_motors)
                self.tango.setTarget(L_MOTORS, self.l_motors)
                self.tango.setTarget(R_MOTORS, self.r_motors)

            # ...

            case 116:
                if self.l_motors == 6000:
                    self.r_motors = 5600
                    self.l_motors = 6200
                else:
                    self.l_motors += 200
                    if self.r_motors < 1510:
                        self.r_motors = 1510
                    # Increment speed by 200 in the reverse direction
                    self.r_motors -= 200

                print(self.r_motors)
                print(self.l_motors)
                self.tango.setTarget(L_MOTORS, self.l_motors)
                self.tango.setTarget(R_MOTORS, self.r_motors)

            # right
            case 113:
                self.r_motors += 200
                if (self.r_motors > 7900):
                    self.r_motors = 7900
                print(self.r_motors)
                self.tango.setTarget(R_MOTORS, self.r_motors)

            # left
            case 114:
                self.l_motors -= 200
                if (self.l_motors < 2110):
                    self.l_motors = 2110
                print(self.l_motors)
                self.tango.setTarget(L_MOTORS, self.l_motors)

            # escape (estop)
            case 9:
                self.body = 6000
                self.headTurn = 6000
                self.headTilt = 6000
                self.r_motors = 6000
                self.l_motors = 6000
                #self.motors = 6000
                #self.turn = 6000

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
                self.default = 6000
                self.tango.setTarget(R_MOTORS, self.default)
                self.tango.setTarget(L_MOTORS, self.default)
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
        print(key.keycode)
        print(keysym)
        match key.keycode:
            case 28:
                print("Left Shoulder")
                self.l_shoulder += 200
                if (self.l_shoulder < 2110):
                    self.l_shoulder = 2110
                print(self.l_shoulder)
                self.tango.setTarget(L_SHOULDER, self.l_shoulder)
            case 29:
                print("Left Bicep")
                self.l_bicep += 200
                if (self.l_bicep < 2110):
                    self.l_bicep = 2110
                print(self.l_bicep)
                self.tango.setTarget(L_BICEP, self.l_bicep)
            case 30:
                print("Left Elbow")
                self.l_elbow += 200
                if (self.l_elbow < 2110):
                    self.l_elbow = 2110
                print(self.l_elbow)
                self.tango.setTarget(L_ELBOW, self.l_elbow)
            case 31:
                print("Left Forarm")
                self.l_forarm += 200
                if (self.l_forarm < 2110):
                    self.l_forarm = 2110
                print(self.l_forarm)
                self.tango.setTarget(L_FORARM, self.l_forarm)
            case 32:
                print("Left Wrist")
                self.l_wrist += 200
                if (self.l_wrist < 2110):
                    self.l_wrist = 2110
                print(self.l_wrist)
                self.tango.setTarget(L_WRIST, self.l_wrist)
            case 33:
                print("Left Fingers")
                self.l_fingers += 200
                if (self.l_fingers < 2110):
                    self.l_fingers = 2110
                print(self.l_fingers)
                self.tango.setTarget(L_FINGERS, self.l_fingers)
            case 41:
                print("Left Shoulder")
                self.l_shoulder -= 200
                if (self.l_shoulder < 2110):
                    self.l_shoulder = 2110
                print(self.l_shoulder)
                self.tango.setTarget(L_SHOULDER, self.l_shoulder)
            case 42:
                print("Left Bicep")
                self.l_bicep -= 200
                if (self.l_bicep < 2110):
                    self.l_bicep = 2110
                print(self.l_bicep)
                self.tango.setTarget(L_BICEP, self.l_bicep)
            case 43:
                print("Left Elbow")
                self.l_elbow -= 200
                if (self.l_elbow < 2110):
                    self.l_elbow = 2110
                print(self.l_elbow)
                self.tango.setTarget(L_ELBOW, self.l_elbow)
            case 44:
                print("Left Forarm")
                self.l_forarm -= 200
                if (self.l_forarm < 2110):
                    self.l_forarm = 2110
                print(self.l_forarm)
                self.tango.setTarget(L_FORARM, self.l_forarm)
            case 45:
                print("Left Wrist")
                self.l_wrist -= 200
                if (self.l_wrist < 2110):
                    self.l_wrist = 2110
                print(self.l_wrist)
                self.tango.setTarget(L_WRIST, self.l_wrist)
            case 46:
                print("Left Fingers")
                self.l_fingers -= 200
                if (self.l_fingers < 2110):
                    self.l_fingers = 2110
                print(self.l_fingers)
                self.tango.setTarget(L_FINGERS, self.l_fingers)
    
    def r_arm(self, key):
        print(key.keycode)
        print(key.keysym)
        match keysym:
            case 28:
                print("Right Shoulder")
                self.r_shoulder += 200
                if (self.r_shoulder < 2110):
                    self.r_shoulder = 2110
                print(self.r_shoulder)
                self.tango.setTarget(R_SHOULDER, self.r_shoulder)
            case 29:
                print("Left Bicep")
                self.r_bicep += 200
                if (self.r_bicep < 2110):
                    self.r_bicep = 2110
                print(self.r_bicep)
                self.tango.setTarget(R_BICEP, self.r_bicep)
            case 30:
                print("Left Elbow")
                self.r_elbow += 200
                if (self.r_elbow < 2110):
                    self.r_elbow = 2110
                print(self.r_elbow)
                self.tango.setTarget(R_ELBOW, self.r_elbow)
            case 31:
                print("Left Forarm")
                self.r_forarm += 200
                if (self.r_forarm < 2110):
                    self.r_forarm = 2110
                print(self.r_forarm)
                self.tango.setTarget(R_FORARM, self.r_forarm)
            case 32:
                print("Left Wrist")
                self.r_wrist += 200
                if (self.r_wrist < 2110):
                    self.r_wrist = 2110
                print(self.r_wrist)
                self.tango.setTarget(R_WRIST, self.r_wrist)
            case 33:
                print("Left Fingers")
                self.r_fingers += 200
                if (self.r_fingers < 2110):
                    self.r_fingers = 2110
                print(self.r_fingers)
                self.tango.setTarget(R_FINGERS, self.r_fingers)
            case 41:
                print("Left Shoulder")
                self.r_shoulder -= 200
                if (self.r_shoulder < 2110):
                    self.r_shoulder = 2110
                print(self.r_shoulder)
                self.tango.setTarget(R_SHOULDER, self.r_shoulder)
            case 41:
                print("Left Bicep")
                self.r_bicep -= 200
                if (self.r_bicep < 2110):
                    self.r_bicep = 2110
                print(self.r_bicep)
                self.tango.setTarget(R_BICEP, self.r_bicep)
            case 43:
                print("Left Elbow")
                self.r_elbow -= 200
                if (self.r_elbow < 2110):
                    self.r_elbow = 2110
                print(self.r_elbow)
                self.tango.setTarget(R_ELBOW, self.r_elbow)
            case 44:
                print("Left Forarm")
                self.r_forarm -= 200
                if (self.r_forarm < 2110):
                    self.r_forarm = 2110
                print(self.r_forarm)
                self.tango.setTarget(R_FORARM, self.r_forarm)
            case 45:
                print("Left Wrist")
                self.r_wrist -= 200
                if (self.r_wrist < 2110):
                    self.r_wrist = 2110
                print(self.r_wrist)
                self.tango.setTarget(R_WRIST, self.r_wrist)
            case 46:
                print("Left Fingers")
                self.r_fingers -= 200
                if (self.r_fingers < 2110):
                    self.r_fingers = 2110
                print(self.r_fingers)
                self.tango.setTarget(_RFINGERS, self.r_fingers)

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
win.bind('<t>', keys.l_arm)
win.bind('<y>', keys.l_arm)
win.bind('<u>', keys.l_arm)
win.bind('<i>', keys.l_arm)
win.bind('<o>', keys.l_arm)
win.bind('<p>', keys.l_arm)

# Left arm, other direction
win.bind('<f>', keys.l_arm)
win.bind('<g>', keys.l_arm)
win.bind('<h>', keys.l_arm)
win.bind('<j>', keys.l_arm)
win.bind('<k>', keys.l_arm)
win.bind('<l>', keys.l_arm) 

# Right arm
win.bind('<1>', keys.r_arm)
win.bind('<2>', keys.r_arm)
win.bind('<3>', keys.r_arm)
win.bind('<4>', keys.r_arm)
win.bind('<5>', keys.r_arm)
win.bind('<6>', keys.r_arm)

win.bind('<7>', keys.r_arm)
win.bind('<8>', keys.r_arm)
win.bind('<9>', keys.r_arm)
win.bind('<0>', keys.r_arm)
win.bind('<K>', keys.r_arm)
win.bind('<L>', keys.r_arm)

win.bind('<Escape>', keys.arrow)
win.mainloop()
keys = KeyControl(win)
