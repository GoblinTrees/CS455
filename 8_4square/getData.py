import serial
import time
import numpy as np
import pyttsx3
from maestro import Controller
import math
import atexit

class Robot:
    def __init__(self):
        self.L_MOTORS = 1
        self.R_MOTORS = 0
        self.r_motors = 6000
        self.l_motors = 6000
        self.tango = Controller()
        self.engine = pyttsx3.init()
        
robot = Robot()
searching = True
count = 0
quadrant = False
findExit = False
quadNum = 5
arr = np.zeros((100, 4))

def findDistances(count, arr):
    try:
        ser = serial.Serial()
        ser.port = '/dev/ttyUSB0'
        ser.baudrate = 115200
        ser.bytesize = serial.EIGHTBITS
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.timeout = 1
        ser.open()
        temp = ser.readline()
        #print("line1: ", temp) #hex values
        data = str(ser.readline()).split(",")
        if str(data[1]) == 'null' or str(data[2]) == 'null' or str(data[3]) == 'null' or str(data[4]) =='null':
            print("bad data, trying again")
            findDistances(ser, count, arr)
        else:
            arr[count, 0] = str(data[1])
            arr[count, 1] = str(data[2])
            arr[count, 2] = str(data[3])
            arr[count, 3] = str(data[4])
            count += 1
        ser.close()
    except Exception as e:
        print(e)
        ser.close()

def findQuadrant(arr, robot, quadNum):
    min = np.argmin(arr[0])
    #print(min)
    if min % 4 == 0:
        quadNum = 0
        robot.engine.say("quadrant 0")
        robot.engine.runAndWait()
    if min % 4 == 1:
        quadNum = 1
        robot.engine.say("quadrant 1")
        robot.engine.runAndWait()
    if min % 4 == 2:
        quadNum = 2
        robot.engine.say("quadrant 2")
        robot.engine.runAndWait()
    if min % 4 == 3:
        quadNum = 3
        robot.engine.say("quadrant 3")
        robot.engine.runAndWait()

def findPylon(count, arr, quadNum, robot):
    #rotate right
    l_motors = 5000
    robot.tango.setTarget(robot.L_MOTORS, l_motors)
    time.sleep(1)
    l_motors = 6000
    robot.tango.setTarget(robot.L_MOTORS, l_motors)

    if arr[count - 1, quadNum] > arr[count, quadNum]:
        findDistances(count, arr)
        findPylon(count, arr)
    else:
        # pointed at the pylon
        # turn 30 degrees
        l_motors = 5000
        robot.tango.setTarget(robot.L_MOTORS, l_motors)
        time.sleep(.5)
        l_motors = 6000
        robot.tango.setTarget(robot.L_MOTORS, l_motors)

        if quadNum == 0:
            a = arr[count, 0]
            c = arr[count, 1]
            b = math.sqrt(a*a + c*c)
        elif quadNum == 1:
            a = arr[count, 2]
            c = arr[count, 1]
            b = math.sqrt(a*a + c*c)
        elif quadNum == 2:
            a = arr[count, 2]
            c = arr[count, 3]
            b = math.sqrt(a*a + c*c)
        else:
            a = arr[count, 0]
            c = arr[count, 3]
            b = math.sqrt(a*a + c*c)
    
        distance = .5/b * math.sqrt(a + b + c) * math.sqrt(b + c - a) * math.sqrt(a - b + c) * math.sqrt(a + b - c)
        # drive
        print(distance)
    try:
        while searching:
            findQuadrant(arr, robot)
            findPylon(count, arr, quadNum)

            # hard limit to cancel program
    finally:
        robot.tango.setTarget(robot.R_MOTORS, 6000)
        robot.tango.setTarget(robot.L_MOTORS, 6000)

