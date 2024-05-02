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
from sympy import symbols, Eq, solve

ldist: float;       #Placeholder for the length of the squares, need to update it with value
ldist2 = 2*ldist
pylon0 = [0,0]
pylon1 = [0,2l]
pylon2 = [2l,2l]
pylon3 = [2l,0]

r1 =[]
r2 =[]
r3 =[]
r4 =[]


class map():
    def __init__(self):
        self.distances = [-1.0,-1.0,-1.0,-1.0] #This holds most current data
        self.prior = [-999.1,-999.1,-999.1,-999.1]      #This holds previous location


    def locate(self)->list:
        #declare x,y as variables
        X, Y = symbols('X Y')

        #make a set of 4 equations of circles with XY variables,
        equations = [
            Eq(sympy.sqrt((X)**2 + (Y)**2), self.distances[0]),
            Eq(sympy.sqrt((X)**2 + (Y-ldist2)**2), self.distances[1]),
            Eq(sympy.sqrt((X-ldist2)**2 + (Y-ldist2)**2), self.distances[2]),
            Eq(sympy.sqrt((X-ldist2)**2 + (Y)**2), self.distances[3])
        ]


        #Using self.distances as radial distance of each circle, solve for X,Y
        solutions = solve(equations)

        print("Solutions:")
        if solutions == []:
            print("No Solutions!")
            return [-10,-10]
        #Converstion back to floats
        float_solutions = []
        for sol in solutions:
            float_solutions.append(float(sol[0]))
            float_solutions.append(float(sol[1]))
        print(f"{float_solutions[0]}:{float_solutions[1]}")

        #return the distance
        return [float_solutions[0],float_solutions[1]]


    def startmapping(self):
        mapThread = threading.Thread(target=self.findDistances(), args=(self,))
        mapThread.start()

    def getDistanceMoveVector(self):
        return [x - y for x, y in zip(self.distances, self.prior)]

    #findDistances modified to run on parrallel thread soas to constanstly update position of system
    def findDistances(self):
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

                    data = [dataentry[1],dataentry[2],dataentry[3],dataentry[4]]
                    # print("Data: ",data)


                    if str(data[0]) == 'null' or str(data[1]) == 'null' or str(data[2]) == 'null' or str(data[3]) == 'null':
                        print("bad data1, trying again")
                        continue    #added by forrest, but unknown if needed
                    elif str(data[0]) == 'nan' or str(data[1]) == 'nan' or str(data[2]) == 'nan' or str(data[3]) == 'nan':
                        print("bad data2, trying again")
                        continue    #added by forrest, but unknown if needed
                    elif (data[0] == 0 or data[1] == 0 or data[2] == 0 or data[3] == 0):
                        print("bad data3, zeros, trying again ")
                        continue    #added by forrest, but unknown if needed
                    else:
                        confidenceInt += 1
                        num1 += float(data[0])
                        num2 += float(data[1])
                        num3 += float(data[2])
                        num4 += float(data[3])
                        #2nd data validation
                        # print(data[0])
                        # print(data[1])
                        # print(data[2])
                        # print(data[3])

                num1 = num1 / 10
                num2 = num2 / 10
                num3 = num3 / 10
                num4 = num4 / 10


                # print("got data")
                ser.close()
            except:
                pass
            self.distances = [num1, num2, num3, num4]
            return [num1, num2, num3, num4]
        finally:
            print("findDist() finally")
            ser.close()