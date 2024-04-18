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
    min = np.argmin(data)
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
    t.sleep(.5)
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

def main():
    arrn = np.zeros((5, 4))

    # drive straight and find distances at two end points
    arrn[0] = findDistances()
    driveForward()
    quad = findQuadrant()
    arrn[1] = findDistances()

    
    d1 = arrn[0, quad]
    d2 = arrn[1, quad]

    ang = findAngle(d1,d2)
    turnAngle(ang)

main()



