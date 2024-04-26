import time
import threading
import pyttsx3
from maestro import Controller
import random

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

headMovements = ["reset", "look left", "look right", "look up", "look down"]
armMovements = ["reset", "prl", "prr", "prb", "lowerl", "lowerr", "pointl", "pointr", "upr", "upl"]

syndromeSpeech = ["See? Now you respect me, because I’m a threat.", "That’s the way it works.", "Turns out, there are a lot of people, whole countries, who want respect,",
          "and they will pay through the nose to get it.", "How do you think I got rich?", "I invented weapons, and now I have a weapon that only I can defeat,",
          "and when I unleash it, I’ll get…", "You sly dog! You got me monologuing! I can’t believe it.", "It’s cool, huh? Zero-point energy.", "I save the best inventions for myself.",
          "Am I good enough now? Who’s super now?", "I’m Syndrome, your nemesis and…Oh, brilliant"]

class Robot():
    def __init__(self):
        self.tango = Controller()

        # The taskmaster executor

        self.engine = pyttsx3.init()
        
        self.body = 6000
        self.headTurn = 6000
        self.headTilt = 6000
        self.r_motors = 6000
        self.l_motors = 6000

        self.l_shoulder = 6000
        self.l_bicep = 5800
        self.l_elbow = 6000
        self.l_forarm = 6000
        self.l_wrist = 6000
        self.l_fingers = 6000

        self.r_shoulder = 6000
        self.r_bicep = 6200
        self.r_elbow = 6000
        self.r_forarm = 6000
        self.r_wrist = 6000
        self.r_fingers = 6000
                
    def beginSpeech(self, speech):
        for line in speech:
            speechThread = threading.Thread(target = self.speak, args = (line,))
            movementThread = threading.Thread(target = self.moveBody)
            
            speechThread.start()
            movementThread.start()
            
            speechThread.join()
            movementThread.join()
            

    def speak(self, line):
        self.engine.say(line)
        print(line)
        self.engine.runAndWait()

    def moveBody(self):
        armMovement = random.choice(armMovements)
        headMovement = random.choice(headMovements)
        print(armMovement)
        print(headMovement)

        armThread = threading.Thread(target = self.moveArm, args = (armMovement,))
        headThread = threading.Thread(target = self.moveHead, args = (headMovement,))

        armThread.start()
        headThread.start()

        armThread.join()
        headThread.join()

    def moveHead(self, headChoice):
        match headChoice:
            case "reset":
                self.headTurn = 6000
                self.headTilt = 6000

                self.tango.setTarget(HEADTURN, self.headTurn)
                self.tango.setTarget(HEADTILT, self.headTilt)
                
            case "look left":
                self.headTurn = 7500
                self.tango.setTarget(HEADTURN, self.headTurn)

            case "look right":
                self.headTurn = 4500
                self.tango.setTarget(HEADTURN, self.headTurn)

            case "look up":
                self.headTilt = 7500
                self.tango.setTarget(HEADTILT, self.headTilt)

            case "look down":
                self.headTilt = 4500
                self.tango.setTarget(HEADTILT, self.headTilt)

    def moveArm(self, armChoice):
        match armChoice:
            case "reset":
                self.l_shoulder = 6000
                self.l_bicep = 5800
                self.l_elbow = 6000
                self.l_forarm = 6000
                self.l_wrist = 6000
                self.l_fingers = 6000

                self.r_shoulder = 6000
                self.r_bicep = 6200
                self.r_elbow = 6000
                self.r_forarm = 6000
                self.r_wrist = 6000
                self.r_fingers = 6000

                self.tango.setTarget(L_SHOULDER, self.l_shoulder)
                self.tango.setTarget(L_BICEP, self.l_bicep)
                self.tango.setTarget(L_ELBOW, self.l_elbow)
                self.tango.setTarget(L_FORARM, self.l_forarm)
                self.tango.setTarget(L_WRIST, self.l_wrist)
                self.tango.setTarget(L_FINGERS, self.l_fingers)

                self.tango.setTarget(R_SHOULDER, self.r_shoulder)
                self.tango.setTarget(R_BICEP, self.r_bicep)
                self.tango.setTarget(R_ELBOW, self.r_elbow)
                self.tango.setTarget(R_FORARM, self.r_forarm)
                self.tango.setTarget(R_WRIST, self.r_wrist)
                self.tango.setTarget(R_FINGERS, self.r_fingers)
                
            case "prl":
                self.l_shoulder = 6500

                self.tango.setTarget(L_SHOULDER, self.l_shoulder)

            case "prr":
                self.r_shoulder = 5500

                self.tango.setTarget(R_SHOULDER, self.r_shoulder)

            case "prb":
                self.l_shoulder = 7000
                self.r_shoulder = 5000

                self.tango.setTarget(L_SHOULDER, self.l_shoulder)
                self.tango.setTarget(R_SHOULDER, self.r_shoulder)

            case "lowerl":
                self.l_shoulder = 6000
                self.l_bicep = 5800
                self.l_elbow = 6000
                self.l_forarm = 6000
                self.l_wrist = 6000
                self.l_fingers = 6000

                self.tango.setTarget(L_SHOULDER, self.l_shoulder)
                self.tango.setTarget(L_BICEP, self.l_bicep)
                self.tango.setTarget(L_ELBOW, self.l_elbow)
                self.tango.setTarget(L_FORARM, self.l_forarm)
                self.tango.setTarget(L_WRIST, self.l_wrist)
                self.tango.setTarget(L_FINGERS, self.l_fingers)

            case "lowerr":
                self.r_shoulder = 6000
                self.r_bicep = 6200
                self.r_elbow = 6000
                self.r_forarm = 6000
                self.r_wrist = 6000
                self.r_fingers = 6000

                self.tango.setTarget(R_SHOULDER, self.r_shoulder)
                self.tango.setTarget(R_BICEP, self.r_bicep)
                self.tango.setTarget(R_ELBOW, self.r_elbow)
                self.tango.setTarget(R_FORARM, self.r_forarm)
                self.tango.setTarget(R_WRIST, self.r_wrist)
                self.tango.setTarget(R_FINGERS, self.r_fingers)
                
            case "pointl":
                self.l_shoulder = 7000
                self.l_bicep = 5000

                self.tango.setTarget(L_SHOULDER, self.l_shoulder)
                self.tango.setTarget(L_BICEP, self.l_bicep)
                
            case "pointr":
                self.r_shoulder = 5000
                self.r_bicep = 7000

                self.tango.setTarget(R_SHOULDER, self.r_shoulder)
                self.tango.setTarget(R_BICEP, self.r_bicep)

            case "upl":
                self.l_shoulder = 8000
                self.l_bicep = 5000

                self.tango.setTarget(L_SHOULDER, self.l_shoulder)
                self.tango.setTarget(L_BICEP, self.l_bicep)

            case "upr":
                self.r_shoulder = 4000
                self.r_bicep = 7000

                self.tango.setTarget(R_SHOULDER, self.r_shoulder)
                self.tango.setTarget(R_BICEP, self.r_bicep)
        

bot = Robot()
bot.beginSpeech(syndromeSpeech)
