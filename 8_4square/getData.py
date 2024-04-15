import serial
import time
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
searching = True
count = 0
quadrant = False
findExit = False
quadNum = 5
arr = np.zeros((15, 4))

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
        temp = ser.readline()
        #print("line1: ", temp) #hex values
        data = str(ser.readline()).split(",")
        #print(data)
        if str(data[1]) == 'null' or str(data[2]) == 'null' or str(data[3]) == 'null' or str(data[4]) =='null':
            print("bad data, trying again")
            return findDistances()
        else:
            print("got data")
            return [data[1], data[2], data[3], data[4]]
        ser.close()
    except Exception as e:
        print(e)
        ser.close()

def findQuadrant():
    data = findDistances()
    min = np.argmin(data)
    #print(min)
    if min % 4 == 0:
        print("Quadrant Number: 0")
        return 0
        #robot.engine.say("quadrant 0")
        #robot.engine.runAndWait()
    if min % 4 == 1:
        print("Quadrant Number: 1")
        return 1
        #robot.engine.say("quadrant 1")
        #robot.engine.runAndWait()
    if min % 4 == 2:
        print("Quadrant Number: 2")
        return 2
        #robot.engine.say("quadrant 2")
        #robot.engine.runAndWait()
    if min % 4 == 3:
        print("Quadrant Number: 3")
        return 3
    
        #robot.engine.say("quadrant 3")
        #robot.engine.runAndWait()
        
def findPylon(count, quadNum, robot):
    arr = np.zeros((15, 4))
    print(findDistances)
    #arr[0] = findDistances()
    #arr[1] = findDistances()
    
    if arr[0, quadNum] > arr[1, quadNum]:
        print("keep turning")
        #rotate right
        l_motors = 5000
        robot.tango.setTarget(robot.L_MOTORS, l_motors)
        time.sleep(.35)
        l_motors = 6000
        robot.tango.setTarget(robot.L_MOTORS, l_motors)
    else:
        # pointed at the pylon

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
        print("distance: ", distance)
        
quadNum = findQuadrant()
findPylon(count, quadNum, robot)
#while searching:
    #findPylon(count, quadNum, robot)

