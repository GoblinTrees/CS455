import serial
import time
import numpy as np
from maestro import Controller

class Robot:
    def __init__(self):
        self.L_MOTORS = 1
        self.R_MOTORS = 0
        self.r_motors = 6000
        self.l_motors = 6000
        self.tango = Controller()
        
robot = Robot()
searching = True
count = 0
quadrant = False
quadNum = 5
arr = np.zeros((10, 4))

try:
    ser = serial.Serial()
    ser.port = '/dev/ttyUSB0'
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 1
    ser.open()
    time.sleep(1)
    l_motors = 5600
    r_motors = 6800
    robot.tango.setTarget(robot.L_MOTORS, l_motors)
    robot.tango.setTarget(robot.R_MOTORS, r_motors)
    time.sleep(1)
    l_motors = 6000
    r_motors = 6000
    robot.tango.setTarget(robot.L_MOTORS, l_motors)
    robot.tango.setTarget(robot.R_MOTORS, r_motors)
    while searching:
        if count >= 9:
            searching = False
        try:
            temp = ser.readline()
            #print("line1: ", temp) #hex values
            data = str(ser.readline()).split(",")
            #print("line2: ", data) # decimal values
            if quadrant:
                arr[0, 0] = str(data[1])
                arr[0, 1] = str(data[2])
                arr[0, 2] = str(data[3])
                arr[0, 3] = str(data[4])
                l_motors = 5000
                robot.tango.setTarget(robot.L_MOTORS, l_motors)
                time.sleep(.25)
                l_motors = 6000
                robot.tango.setTarget(robot.L_MOTORS, l_motors)
                l_motors = 5600
                r_motors = 6800
                robot.tango.setTarget(robot.L_MOTORS, l_motors)
                robot.tango.setTarget(robot.R_MOTORS, r_motors)
                time.sleep(1)
                l_motors = 6000
                r_motors = 6000
                robot.tango.setTarget(robot.L_MOTORS, l_motors)
                robot.tango.setTarget(robot.R_MOTORS, r_motors)
                temp = ser.readline()
                data = str(ser.readline()).split(",")
                arr[1, 0] = str(data[1])
                arr[1, 1] = str(data[2])
                arr[1, 2] = str(data[3])
                arr[1, 3] = str(data[4])
                if arr[0, quadNum] < arr[1, quadNum]:
                    #rotate 180 and drive out
                    l_motors = 5000
                    robot.tango.setTarget(robot.L_MOTORS, l_motors)
                    time.sleep(.25)
                    l_motors = 6000
                    robot.tango.setTarget(robot.L_MOTORS, l_motors)
                else:
                    #drive out
                    l_motors = 5600
                    r_motors = 6800
                    robot.tango.setTarget(robot.L_MOTORS, l_motors)
                    robot.tango.setTarget(robot.R_MOTORS, r_motors)
                    time.sleep(3)
                    l_motors = 6000
                    r_motors = 6000
                    
            if str(data[1]) == 'null' or str(data[2]) == 'null' or str(data[3]) == 'null' or str(data[4]) =='null':
                print("bad data, trying again")
            else:
                arr[0, 0] = str(data[1])
                arr[0, 1] = str(data[2])
                arr[0, 2] = str(data[3])
                arr[0, 3] = str(data[4])
                count += 1
            print(arr)
            #searching = False
            min = np.argmin(arr[0])
            #print(min)
            if min % 4 == 0:
                quadNum = 0
                print("quadrant 0")
            if min % 4 == 1:
                quadNum = 1
                print("quadrant 1")
            if min % 4 == 2:
                quadNum = 2
                print("quadrant 2")
            if min % 4 == 3:
                quadNum = 3
                print("quadrant 3")
            quadrant = True
        except Exception as e:
            print("Error processing data:", e)
            break  # Exit the loop if an error occurs
        finally:
            print("Mission Successful")
except Exception as e:
    print("ERROR IN FIRST TRY OF GET DISTANCES:", e)
    pass
ser.close()

