import serial
import time
import numpy as np
from maestro import Controller
import tkinter as tk

class Robot:
    def __init__(self, root):
        self.root = root
        self.L_MOTORS = 1
        self.R_MOTORS = 0
        self.r_motors = 6000
        self.l_motors = 6000
        self.tango = Controller()

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
            ser.close()
        except Exception as e:
            print("ERROR IN FIRST TRY OF GET DISTANCES:", e)
            pass

def findPylon(robot, searching, foundPylon, missionSuccess, pylon, numData, target, previousHighest):
    while searching:
        if foundPylon:
            # rotate for .5 seconds
            robot.r_motors = 7000
            robot.tango.setTarget(robot.R_MOTORS, robot.r_motors)
            time.sleep(.5)
            robot.r_motors = 6000
            robot.tango.setTarget(robot.R_MOTORS, robot.r_motors)

        try:
            # Your data processing logic goes here
            pass
        finally:
            print("Mission Successful")

root = tk.Tk()
robot = Robot(root)
findPylon(robot, searching, foundPylon, missionSuccess, pylon, numData, target, previousHighest)
root.mainloop()