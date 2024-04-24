import RPi.GPIO as GPIO
import serial
import time as t
import numpy as np
import pyttsx3
from maestro import Controller
import math


class Robot:
    def __init__(self):
        self.L_MOTORS = 1
        self.R_MOTORS = 0
        self.r_motors = 6000
        self.l_motors = 6000
        self.tango = Controller()
        self.engine = pyttsx3.init()

    def speak(self, words: str):
        self.engine.say(words)
        self.engine.runAndWait()


robot = Robot()

# set GPIO mode
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
TRIG_PIN = 24
ECHO_PIN = 23

# set trig as output anc ECHO as input
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

GPIO.setwarnings(False)


def getObject():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    trigPin = 24
    echoPin = 23
    GPIO.setup(trigPin, GPIO.OUT)
    GPIO.setup(echoPin, GPIO.IN)
    GPIO.output(trigPin, False)
    t.sleep(.1)
    GPIO.output(trigPin, True)
    t.sleep(.00001)
    GPIO.output(trigPin, False)
    timeout = t.time()
    while GPIO.input(echoPin) == 0:
        if (t.time() - timeout) > 3:
            print("timeout during echo")
            return None
    pulseStart = t.time()
    timeout = t.time()
    while(GPIO.input(echoPin) == 1):
        if(t.time() - timeout > 3):
            print("timeout while receiving echo")
            return None
    pulseEnd = t.time()
    pulseDuration = pulseEnd - pulseStart
    distance = pulseDuration * 17150
    distance = float(round(distance, 2))
    return distance

def leaveSquare(distance, objDis):
    if objDis < 50:
        print("object detected, please move before i drive")
        t.sleep(2)
        return True
    # parametrized distance, uses the distance to the pylon instead of nominal distance so it should be an overestimate.
    else:
        exitTime = distance/.75
        l_motors = 5400
        r_motors = 7000
        robot.tango.setTarget(robot.L_MOTORS, l_motors)
        robot.tango.setTarget(robot.R_MOTORS, r_motors)
        t.sleep(exitTime)
        motors = 6000
        robot.tango.setTarget(robot.L_MOTORS, motors)
        robot.tango.setTarget(robot.R_MOTORS, motors)
        print("exited")
        robot.speak("Exited")
        return False

temp = getObject()
while temp > 20:
    temp = getObject()
    leaveSquare(1, temp)
    print("Distance: ", temp)

