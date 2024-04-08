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
        ser.parity =serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.timeout = 1
        ser.open()
        time.sleep(1)
        ser.close()
except Exception as e:
        print("ERROR IN FIRST TRY OF GET DISTANCES:",e)
        pass

ser.open()
searching = True
foundPylon = False
missionSuccess = False
pylon = np.zeros((4,), dtype=int)
numData = 0
target = None
previousHighest = None

def findPylon (self):
        while searching:
                if foundPylon:
                        # rotate for .5 seconds
                        self.r_motors = 7000
                        self.tango.setTarget(self.R_MOTORS, self.r_motors)
                        time.sleep(.5)
                        self.r_motors = 6000
                        self.tango.setTarget(self.R_MOTORS, self.r_motors)

                try:
                        # data looks like this when it first gets here
                        # mc 0f 00000663 000005a3 00000512 000004cb  ffffffff ffffffff ffffffff 095f c1 00146fb7 a0:0 22be
                        # 0  1  2        3        4        5        6        7        8        9        10   11 12       13   14
                        data=str(ser.readline())
                        data1 = str(ser.readline())
                        data1 = data1.split(',')
                        isNull = False
                        if foundPylon:
                        # check if its less than previous
                                if data1[target] < previousHighest:
                                        previousHighest = data1[target]
                                else:
                                        # rotate for .5 seconds
                                        self.r_motors = 7000
                                        self.tango.setTarget(self.R_MOTORS, self.r_motors)
                                        time.sleep(.5)
                                        self.r_motors = 6000
                                        self.tango.setTarget(self.R_MOTORS, self.r_motors)

                                        # drive straight based on distance calculated in pylon[target]
                                        self.r_motors = 6600
                                        self.l_motors = 5800
                                        self.tango.setTarget(self.L_MOTORS, self.l_motors)
                                        self.tango.setTarget(self.R_MOTORS, self.r_motors)
                                        time.sleep(3) # figure out how far this drives
                                        self.r_motors = 6000
                                        self.l_motors = 6000
                                        self.tango.setTarget(self.L_MOTORS, self.l_motors)
                                        self.tango.setTarget(self.R_MOTORS, self.r_motors)
                                        searching = False

                        else:
                                if numData == 10:
                                        pylon[0] = pylon[0]/10
                                        pylon[1] = pylon[1]/10
                                        pylon[2] = pylon[2]/10
                                        pylon[3] = pylon[3]/10
                                        target = pylon.argmax()
                                        foundPylon = True
                                        previousHighest = pylon[target]
                                else:
                                        for i in range(4):
                                                if data1[i] > 2000000 or data1[i] == None:
                                                        isNull = True
                                        if isNull == False:
                                                for i in range(4):
                                                        numData += 1
                                                        pylon[i] += data1[i]
                finally:
                        print("Mission Successful")
                                
root = tk.Tk()
robot = Robot(root)
findPylon(robot)
root.mainloop()