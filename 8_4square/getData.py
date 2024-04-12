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
            min = np.argmin(arr)
            print(min)
            if min % 4 == 0:
                print("quadrant 0")
            if min % 4 == 1:
                print("quadrant 1")
            if min % 4 == 2:
                print("quadrant 2")
            if min % 4 == 3:
                print("quadrant 3")
            searching = False
        try:
            temp = ser.readline()
            #print("line1: ", temp) #hex values
            data = str(ser.readline()).split(",")
            #print("line2: ", data) # decimal values
            
            if str(data[1]) == 'null' or str(data[2]) == 'null' or str(data[3]) == 'null' or str(data[4]) =='null':
                print("bad data, trying again")
            else:
                arr[count, 0] = str(data[1])
                arr[count, 1] = str(data[2])
                arr[count, 2] = str(data[3])
                arr[count, 3] = str(data[4])
                count += 1
            
            print(arr)
        except Exception as e:
            print("Error processing data:", e)
            break  # Exit the loop if an error occurs
        finally:
            print("Mission Successful")
except Exception as e:
    print("ERROR IN FIRST TRY OF GET DISTANCES:", e)
    pass
ser.close()

