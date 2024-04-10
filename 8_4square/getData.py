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
    while searching:
        count += 1
        if count >= 9:
            searching = False
        l_motors = 7000
        r_motors = 5000
        robot.tango.setTarget(robot.L_MOTORS, l_motors)
        robot.tango.setTarget(robot.R_MOTORS, r_motors)
        time.sleep(1)
        l_motors = 6000
        r_motors = 6000
        robot.tango.setTarget(robot.L_MOTORS, l_motors)
        robot.tango.setTarget(robot.R_MOTORS, r_motors)
        try:
            temp = ser.readline()
            data = ser.readline().split(",")
            print(data)
        except Exception as e:
            print("Error processing data:", e)
            break  # Exit the loop if an error occurs
        finally:
            print("Mission Successful")
except Exception as e:
    print("ERROR IN FIRST TRY OF GET DISTANCES:", e)
    pass
ser.close()

