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

            # Drive straight based on distance calculated in pylon[target]
            robot.r_motors = 6600
            robot.l_motors = 5800
            robot.tango.setTarget(robot.L_MOTORS, robot.l_motors)
            robot.tango.setTarget(robot.R_MOTORS, robot.r_motors)
            time.sleep(3)  # Adjust the time to drive as needed
            robot.r_motors = 6000
            robot.l_motors = 6000
            robot.tango.setTarget(robot.L_MOTORS, robot.l_motors)
            robot.tango.setTarget(robot.R_MOTORS, robot.r_motors)

            searching = False

        else:
            try:
                data = ser.readline().decode().strip()
                data_parts = data.split()
                if len(data_parts) == 15:  # Check if the data has all parts
                    # Extract relevant data
                    pylon_data = [int(data_parts[2]), int(data_parts[3]), int(data_parts[4]), int(data_parts[5])]
                    
                    if numData == 9:
                        print("Found 10 data points")
                        pylon = np.mean(dataPoints, axis=0)
                        target = np.argmax(pylon)
                        foundPylon = True
                        previousHighest = pylon[target]
                    else:
                        # Accumulate data points
                        numData += 1
                        dataPoints[numData] = pylon_data
            except Exception as e:
                print("Error processing data:", e)
                break  # Exit the loop if an error occurs
            finally:
                print("Mission Successful")

root = tk.Tk()
robot = Robot(root)
searching = True
foundPylon = False
pylon = None
numData = 0
target = none
previous highest = 0
missionSuccess = False

findPylon(robot, searching, foundPylon, missionSuccess, pylon, numData, target, previousHighest)
root.mainloop()