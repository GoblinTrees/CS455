import time
import serial
import time as t
import numpy as np
import pyttsx3
import sympy
from maestro import Controller

from maestro import Controller
import math
# import RPi.GPIO as GPIO
import threading
from sympy import symbols, Eq, solve

ldist: float = 1.0  # Placeholder for the length of the squares, calling it 5 ft to the length
ldist2 = 2 * ldist

pylonDict = {
    "0": [0, 0],
    "1": [0, ldist2],
    "2": [ldist2, ldist2],
    "3": [ldist2, 0],
}


# This works by making an instance of the map class, then starting the startloop to get things going
# The distances constantly updates, TODO add update() to figure out heading and directions to pylons
# #This will work for straight lines, but not curves

class map():
    def __init__(self):
        self.distances = [-1.0, -1.0, -1.0, -1.0]  # This holds most current location data
        self.previous = [-999.1, -999.1, -999.1, -999.1]  # This holds previous location
        self.quad = -1
        self.xy = [-1, -1]

    def startmapping(self):
        while True:
            self.findDistances()
            self.findQuad()
            self.reportMap()

    def findxy(self):
        if self.quad == -1:
            print("--CANT FIND XY WHEN OUT OF BOUNDS---")
        temp = self.distances.copy()
        min = np.argmin(self.distances)
        temp.remove(min)
        min2 = np.argmin(self.distances)

        X, Y = symbols('X Y')
        ldist2 = 3.0        #length of two squares in sensor val

        match min:
            case 0:
                if min2 == 1:
                    equations = [
                        Eq(sympy.sqrt((X) ** 2 + (Y) ** 2), self.distances[0]),
                        Eq(sympy.sqrt((X) ** 2 + (Y - ldist2) ** 2), self.distances[1]),
                    ]
                elif min2 == 3:
                    equations = [
                        Eq(sympy.sqrt((X) ** 2 + (Y) ** 2), self.distances[0]),
                        Eq(sympy.sqrt((X - ldist2) ** 2 + (Y) ** 2), self.distances[3])
                    ]
            case 1:
                if min2 == 0:
                    equations = [
                        Eq(sympy.sqrt((X) ** 2 + (Y) ** 2), self.distances[0]),
                        Eq(sympy.sqrt((X) ** 2 + (Y - ldist2) ** 2), self.distances[1]),
                    ]
                elif min2 == 2:
                    equations = [
                        Eq(sympy.sqrt((X) ** 2 + (Y - ldist2) ** 2), self.distances[1]),
                        Eq(sympy.sqrt((X - ldist2) ** 2 + (Y - ldist2) ** 2), self.distances[2]),
                    ]
            case 2:
                if min2 == 1:
                    equations = [
                        Eq(sympy.sqrt((X) ** 2 + (Y - ldist2) ** 2), self.distances[1]),
                        Eq(sympy.sqrt((X - ldist2) ** 2 + (Y - ldist2) ** 2), self.distances[2]),
                    ]
                elif min2 == 3:
                    equations = [
                        Eq(sympy.sqrt((X - ldist2) ** 2 + (Y - ldist2) ** 2), self.distances[2]),
                        Eq(sympy.sqrt((X - ldist2) ** 2 + (Y) ** 2), self.distances[3])
                    ]
            case 3:
                if min2 == 2:
                    equations = [
                        Eq(sympy.sqrt((X - ldist2) ** 2 + (Y - ldist2) ** 2), self.distances[2]),
                        Eq(sympy.sqrt((X - ldist2) ** 2 + (Y) ** 2), self.distances[3])
                    ]
                elif min2 == 0:
                    equations = [
                        Eq(sympy.sqrt((X) ** 2 + (Y) ** 2), self.distances[0]),
                        Eq(sympy.sqrt((X - ldist2) ** 2 + (Y) ** 2), self.distances[3])
                    ]

        solutions = solve(equations)
        if solutions == []:
            print("---No XY Solutions!---")
            return [-10,-10]

        for sol in solutions:       #check every key-value for X,Y, and if they're less than 0 or greater than the side length of the large square then toss the data
            for key in sol.keys():
                if sol[key] < 0:
                    solutions.remove(sol)
                elif sol[key] > ldist2:
                    solutions.remove(sol)


        if len(solutions) == 1:
            self.xy = [solutions[0].get("X"),solutions[0].get("Y")]
            return
        else:
            print("---ERR in findxy() return---")




    def findQuad(self):
        for d in self.distances:  # for check to see if the bot is out of bounds
            if d > 3.1:
                return -1
        return np.argmin(self.distances)

    def reportMap(self):
        print(
            f"Quad: {self.quad} :: Dist-> [{self.distances[0]},{self.distances[1]},{self.distances[2]},{self.distances[3]}]")

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

                self.distances = [num1, num2, num3, num4]
                self.distances = [round(num, 2) for num in self.distances]
                # print("\nDist: ", self.distances)

                self.locate()
                return [num1, num2, num3, num4]
            finally:
                # print("findDist() finally")
                ser.close()


if __name__ == "__main__":
    pass
    # Map = map()
    # mapThread = threading.Thread(target=Map.startmapping)
    # mapThread.start()
