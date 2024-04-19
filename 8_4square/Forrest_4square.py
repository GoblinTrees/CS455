import time
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

    def speak(self,words:str):
        self.engine.say(words)
        self.engine.runAndWait()
        
robot = Robot()
count = 0
quadNum = 5


def findDistances():
    #print("in function")
    try:
        #print("in try")
        ser = serial.Serial()
        ser.port = '/dev/ttyUSB0'
        ser.baudrate = 115200
        ser.bytesize = serial.EIGHTBITS
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.timeout = 1
        ser.open()

        num1 = 0
        num2 = 0
        num3 = 0
        num4 = 0

        confidenceInt =0
        while confidenceInt < 10:
            print("ConInt: ", confidenceInt)
            temp = ser.readline()
            dataentry = ser.readline()
            data = [dataentry[1],dataentry[2],dataentry[3],dataentry[4]]
            # print("Data1: ",data[1])
            if str(data[0]) == 'null' or str(data[1]) == 'null' or str(data[2]) == 'null' or str(data[3]) == 'null':
                print("bad data1, trying again")
            elif str(data[0]) == 'nan' or str(data[1]) == 'nan' or str(data[2]) == 'nan' or str(data[3]) == 'nan':
                print("bad data2, trying again")
            elif (data[0] == 0 or data[1] == 0 or data[2] == 0 or data[3] == 0):
                print("baddata3")

            else:
                confidenceInt += 1
                num1 += float(data[0])
                num2 += float(data[1])
                num3 += float(data[2])
                num4 += float(data[3])
                #2nd data validation
                # print(data[0])
                # print(data[1])
                # print(data[2])
                # print(data[3])

        num1 = num1 / 1000
        num2 = num2 / 1000
        num3 = num3 / 1000
        num4 = num4 / 1000


        print("got data")
        ser.close()
        return [num1, num2, num3, num4]
    finally:
        print("finally")
        #doneofdjakdhfjkalhjdfla
        ser.close()

def findQuadrant():
    data = findDistances()
    print("Quadrant data:")
    print(data)
    min = np.argmin(data)
    print("Min:",min)
    return min

def turn90():
    l_motors = 5000
    robot.tango.setTarget(robot.L_MOTORS, l_motors)
    t.sleep(.87)
    l_motors = 6000
    robot.tango.setTarget(robot.L_MOTORS, l_motors)

def findAngle(distance1,distance2):
    angle: int
    drivedist = 1
    d =distance1**2 +distance2**2 -drivedist**2
    c = 2*distance2*distance1
    angle = math.acos(d/c)
    return angle

def turnAngle(angle):
    #.01 sec per degree
    l_motors = 5000
    robot.tango.setTarget(robot.L_MOTORS, l_motors)
    t.sleep(.01 * angle)
    l_motors = 6000
    robot.tango.setTarget(robot.L_MOTORS, l_motors)

def driveForward():
    l_motors = 5400
    r_motors = 7000
    robot.tango.setTarget(robot.L_MOTORS, l_motors)
    robot.tango.setTarget(robot.R_MOTORS, r_motors)
    t.sleep(1)
    motors = 6000
    robot.tango.setTarget(robot.L_MOTORS, motors)
    robot.tango.setTarget(robot.R_MOTORS, motors)

def driveBackward():
    l_motors = 6600
    r_motors = 5000
    robot.tango.setTarget(robot.L_MOTORS, l_motors)
    robot.tango.setTarget(robot.R_MOTORS, r_motors)
    t.sleep(.5)
    motors = 6000
    robot.tango.setTarget(robot.L_MOTORS, motors)
    robot.tango.setTarget(robot.R_MOTORS, motors)

def findPylon(quadNum, robot):
    arr = np.zeros((5, 4))

    for i in range(5):
        arr[i] = findDistances()
        turn90()
    min = np.argmin(arr)
    print("Min: ",min)
    row = min % 4
    for i in range(row):
        turn90()

def leaveSquare(distance):
    # parametrized distance, uses the distance to the pylon instead of nominal distance so it should be an overestimate.
    exitTime = distance/.347
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

def findExit():
    # drive straight and find distances at two end points
    arrn = np.zeros((5, 4))
    arrn[0] = findDistances()
    driveForward()
    arrn[1] = findDistances()
    
    # Find the quadrant and print it out
    quad = findQuadrant()
    print("In quadrant ", quad)
    robot.speak("In quadrant "+ str(quad))
    

    # find the difference between the target at the two end points
    diff = arrn[0, quad] - arrn[1, quad]

    # if the change is negative, the robot drove away from the pylon, rotate 180 then drive straight until it leaves the square
    if diff < -.05:
        turn90()
        turn90()
        leaveSquare(arrn[1, quad])
    # if the change is negligible, rotate 90 degrees and try again
    elif 0 < diff and diff < .05:
        turn90()
        findExit()
    # if the change is positive, the robot drove towards the pylon, just exit the square
    elif diff > .05:
        leaveSquare(arrn[1, quad])
    # extra case for nan, null, or other weird input
    else:
        robot.speak("I'm lost")
        print("Could not find exit")



findExit()



