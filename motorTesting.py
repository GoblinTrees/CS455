import time
import serial
import time as t
import numpy as np
import pyttsx3
import sympy

from maestro import Controller
import math
import RPi.GPIO as GPIO
import threading
import pyttsx3
from sympy import symbols, Eq, solve



engine = pyttsx3.init()

xy = [-1, -1]


class Robot:
    def __init__(self):
        self.L_MOTORS = 1
        self.R_MOTORS = 0
        self.r_motors = 6000
        self.l_motors = 6000
        self.tango = Controller()
        self.engine = pyttsx3.init()
        self.distances = [-1.0, -1.0, -1.0, -1.0]  # This holds most current location data
        self.previous = [-999.1, -999.1, -999.1, -999.1]  # This holds previous location
        self.quad = -1  # Holds Quadrant info
        self.startmapping()  # Function call to start the multithreading to update the distances and quad in parrallel
        # self.xy = [-1, -1]

    def speak(self, words: str):
        self.engine.say(words)
        self.engine.runAndWait()

    def setmotor(self, *args):
        X, Y = symbols('X Y')

        if len(args) == 0:
            self.tango.setTarget(1, self.l_motors)
            self.tango.setTarget(0, self.r_motors)
        elif len(args) == 1:
            val = args
            self.tango.setTarget(1, val)
            self.tango.setTarget(0, 12000 - val)
        elif len(args) == 2:
            self.tango.setTarget(1, args[0])
            self.tango.setTarget(0, args[2])
        else:
            print("SETMOTOR() ERROR, TOO MANY ARGS")
            return

    def stop_after(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # Do something after the function runs
            return result

        return wrapper

    def startmapping(self):
        while True:

            self.findDistances()
            self.findQuad()
            # self.findxy()
            self.reportMap()


    def getHeading(self):
        firstquad = self.quad
        self.previous = self.distances  # store current location
        self.setmotor(6400, 5600)  # Go forward for one second
        time.sleep(1)
        self.setmotor(6000, 6000)
        time.sleep(1)  # Delay to get a better distance val
        if self.quad() == -1:
            print("---OUT OF BOUNDS---")
            return -1
        curDist = self.distances
        #TODO keep working here

    def getHeading2(self):
        priorxy = xy.copy()
        self.setmotor(6400, 5600)  # Go forward for one second
        time.sleep(1)
        self.setmotor(6000, 6000)
        time.sleep(1)  # Delay to get a better distance val
        moveVector = self.getVector(priorxy,xy)
        theata = math.atan(moveVector[1],moveVector[0])
        print(f"Theata: {theata}")      #This is angle from "East" between pylons 2,3 with origin at 0
        alpha = 0
        if moveVector[0] < 0:
            alpha = theata - math.pi*.5
        else:
            alpha - math.pi*.5 - theata
        print(f"Alpha: {alpha} ") #This is angle off of "North" from between pylons 1, 2




    def findxy(self):
        if self.quad == -1:
            print("--CANT FIND XY WHEN OUT OF BOUNDS---")
        temp = self.distances.copy()
        min = np.argmin(temp)
        temp.remove(temp[min])
        min2 = np.argmin(temp)

        X, Y = symbols('X Y')
        ldist2 = 3.0  # length of two squares in sensor val
        solutions = []

        match min:
            case 0:
                if min2 == 1:
                    equations = [
                        Eq(sympy.sqrt((X) ** 2 + (Y) ** 2), self.distances[0]),
                        Eq(sympy.sqrt((X) ** 2 + (Y - ldist2) ** 2), self.distances[1]),
                    ]
                    solutions = solve(equations)

                elif min2 == 3:
                    equations = [
                        Eq(sympy.sqrt((X) ** 2 + (Y) ** 2), self.distances[0]),
                        Eq(sympy.sqrt((X - ldist2) ** 2 + (Y) ** 2), self.distances[3])
                    ]
                    solutions = solve(equations)

            case 1:
                if min2 == 0:
                    equations = [
                        Eq(sympy.sqrt((X) ** 2 + (Y) ** 2), self.distances[0]),
                        Eq(sympy.sqrt((X) ** 2 + (Y - ldist2) ** 2), self.distances[1]),
                    ]
                    solutions = solve(equations)

                elif min2 == 2:
                    equations = [
                        Eq(sympy.sqrt((X) ** 2 + (Y - ldist2) ** 2), self.distances[1]),
                        Eq(sympy.sqrt((X - ldist2) ** 2 + (Y - ldist2) ** 2), self.distances[2]),
                    ]
                    solutions = solve(equations)

            case 2:
                if min2 == 1:
                    equations = [
                        Eq(sympy.sqrt((X) ** 2 + (Y - ldist2) ** 2), self.distances[1]),
                        Eq(sympy.sqrt((X - ldist2) ** 2 + (Y - ldist2) ** 2), self.distances[2]),
                    ]
                    solutions = solve(equations)

                elif min2 == 3:
                    equations = [
                        Eq(sympy.sqrt((X - ldist2) ** 2 + (Y - ldist2) ** 2), self.distances[2]),
                        Eq(sympy.sqrt((X - ldist2) ** 2 + (Y) ** 2), self.distances[3])
                    ]
                    solutions = solve(equations)

            case 3:
                if min2 == 2:
                    equations = [
                        Eq(sympy.sqrt((X - ldist2) ** 2 + (Y - ldist2) ** 2), self.distances[2]),
                        Eq(sympy.sqrt((X - ldist2) ** 2 + (Y) ** 2), self.distances[3])
                    ]
                    solutions = solve(equations)

                elif min2 == 0:
                    equations = [
                        Eq(sympy.sqrt((X) ** 2 + (Y) ** 2), self.distances[0]),
                        Eq(sympy.sqrt((X - ldist2) ** 2 + (Y) ** 2), self.distances[3])
                    ]
                solutions = solve(equations)

        if solutions == []:
            print("---No XY Solutions!---")
            return

        for sol in solutions:  # check every key-value for X,Y, and if they're less than 0 or greater than the side length of the large square then toss the data
            for key in sol.keys():
                if sol[key] < 0:
                    solutions.remove(sol)
                elif sol[key] > ldist2:
                    solutions.remove(sol)

        if len(solutions) == 1:                 #only one solution should remain, set the XY coordinates to it
            xy = [solutions[0].get("X"), solutions[0].get("Y")]
            return
        else:
            print("---ERR in findxy() return---")

    def findQuad(self):
        for d in self.distances:  # for check to see if the bot is out of bounds
            if d > 4:
                return -1
        return np.argmin(self.distances)

    def reportMap(self):
        print(
            f"Quad: {self.quad} __ Dist:: [{self.distances[0]},{self.distances[1]},{self.distances[2]},{self.distances[3]}] __  XY:: [{xy[0]},{xy[1]}]")

    def getVector(self, startList: list, endList: list):
        return [x - y for x, y in zip(endList, startList)]

    def getDistanceMoveVector(self):
        return [x - y for x, y in zip(self.distances, self.previous)]

    # findDistances modified to run on parrallel thread soas to constanstly update position of system
    def findDistances(self):

        while True:
            # print(">> findDist <<\n")
            try:
                # print("in try")
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

                confidenceInt = 0
                try:
                    while confidenceInt < 5:

                        # print("ConInt: ", confidenceInt)
                        temp = ser.readline()

                        dataentry = str(ser.readline()).split(",")
                        # print("Dataentry: ",dataentry)

                        data = [dataentry[1], dataentry[2], dataentry[3], dataentry[4]]
                        # print("Data: ", data)

                        if str(data[0]) == 'null' or str(data[1]) == 'null' or str(data[2]) == 'null' or str(
                                data[3]) == 'null':
                            # print("bad data1, trying again")
                            continue  # added by forrest, but unknown if needed
                        elif str(data[0]) == 'nan' or str(data[1]) == 'nan' or str(data[2]) == 'nan' or str(
                                data[3]) == 'nan':
                            # print("bad data2, trying again")
                            continue  # added by forrest, but unknown if needed
                        elif (data[0] == 0 or data[1] == 0 or data[2] == 0 or data[3] == 0):
                            # print("bad data3, zeros, trying again ")
                            continue  # added by forrest, but unknown if needed
                        else:
                            confidenceInt += 1
                            num1 += float(data[0])
                            num2 += float(data[1])
                            num3 += float(data[2])
                            num4 += float(data[3])
                            # 2nd data validation
                            # print(data[0])
                            # print(data[1])
                            # print(data[2])
                            # print(data[3])

                    num1 = num1 / 5
                    num2 = num2 / 5
                    num3 = num3 / 5
                    num4 = num4 / 5

                    # print("got data")
                    ser.close()
                except:
                    pass

                if num1 + num2 + num3 + num4 == 0:
                    self.distances = [num1, num2, num3, num4]
                else:
                    self.distances = [num1, num2, num3, num4]
                self.distances = [round(num, 2) for num in self.distances]
                # print("\nDist: ", self.distances)

                # self.locate()
                return [num1, num2, num3, num4]
            finally:
                # print("findDist() finally")
                ser.close()

    def stop(self):
        self.l_motors = 6000
        self.r_motors = 6000
        pass



if __name__ == "__main__":
    robot = Robot()
    mapThread = threading.Thread(target=robot.startmapping())
    mapThread.start()

    #TODO test heading2 and map data collection, then figure out motor mappings for rotation, etc
