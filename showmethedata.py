import threading
import serial
import numpy as np
import sympy
import math
from sympy import symbols, Eq, solve

ldist1 = 1.5  # length of one square in sensor val
ldist2 = 2 * ldist1  # length of two squares in sensor val

quadVectors = {0: [ldist2 * .25, ldist2 * .25], 1: [ldist2 * .25, ldist2 * .75], 2: [ldist2 * .75, ldist2 * .75],
               3: [ldist2 * .75, ldist2 * .25]}

distances = [-1.0, -1.0, -1.0, -1.0]  # This holds most current location data
previous = [-999.1, -999.1, -999.1, -999.1]  # This holds previous location
quad = -1  # Holds Quadrant info
xy = [-1, -1]
heading = [0, 0]


def startmapping():
    while True:
        findDistances()
        findQuad()
        findxy()
        reportMap()


def findDistances():
    try:
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
                temp = ser.readline()
                dataentry = str(ser.readline()).split(",")
                data = [dataentry[1], dataentry[2], dataentry[3], dataentry[4]]

                if str(data[0]) == 'null' or str(data[1]) == 'null' or str(data[2]) == 'null' or str(
                        data[3]) == 'null':
                    continue
                elif str(data[0]) == 'nan' or str(data[1]) == 'nan' or str(data[2]) == 'nan' or str(
                        data[3]) == 'nan':
                    continue
                elif (data[0] == 0 or data[1] == 0 or data[2] == 0 or data[3] == 0):
                    continue
                else:
                    confidenceInt += 1
                    num1 += float(data[0])
                    num2 += float(data[1])
                    num3 += float(data[2])
                    num4 += float(data[3])

            num1 = num1 / 5
            num2 = num2 / 5
            num3 = num3 / 5
            num4 = num4 / 5

            ser.close()
        except:
            pass

        if num1 + num2 + num3 + num4 == 0:
            distances = [num1, num2, num3, num4]
        else:
            distances = [num1, num2, num3, num4]
        distances = [round(num, 2) for num in distances]

        return distances
    finally:
        ser.close()


def findQuad():
    global quad
    for d in distances:  # for check to see if the bot is out of bounds
        if d > math.sqrt(2) * ldist2:
            quad = -1
            return -1
    quad = np.argmin(distances)
    return quad


def findxy():
    global quad
    if quad == -1:
        print("--CANT FIND XY WHEN OUT OF BOUNDS---")
        return
    temp = distances.copy()
    min = np.argmin(temp)
    temp[min] = 9999.99
    min2 = np.argmin(temp)

    X, Y = symbols('X Y')

    match min:
        case 0:
            if min2 == 1:
                equations = [
                    Eq(sympy.sqrt((X) ** 2 + (Y) ** 2), distances[0]),
                    Eq(sympy.sqrt((X) ** 2 + (Y - ldist2) ** 2), distances[1]),
                ]
            elif min2 == 3:
                equations = [
                    Eq(sympy.sqrt((X) ** 2 + (Y) ** 2), distances[0]),
                    Eq(sympy.sqrt((X - ldist2) ** 2 + (Y) ** 2), distances[3])
                ]
        case 1:
            if min2 == 0:
                equations = [
                    Eq(sympy.sqrt((X) ** 2 + (Y - ldist2) ** 2), distances[1]),
                    Eq(sympy.sqrt((X) ** 2 + (Y) ** 2), distances[0]),
                ]
            elif min2 == 2:
                equations = [
                    Eq(sympy.sqrt((X) ** 2 + (Y - ldist2) ** 2), distances[1]),
                    Eq(sympy.sqrt((X - ldist2) ** 2 + (Y - ldist2) ** 2), distances[2]),
                ]
        case 2:
            if min2 == 1:
                equations = [
                    Eq(sympy.sqrt((X) ** 2 + (Y - ldist2) ** 2), distances[1]),
                    Eq(sympy.sqrt((X - ldist2) ** 2 + (Y - ldist2) ** 2), distances[2]),
                ]
            elif min2 == 3:
                equations = [
                    Eq(sympy.sqrt((X - ldist2) ** 2 + (Y - ldist2) ** 2), distances[2]),
                    Eq(sympy.sqrt((X - ldist2) ** 2 + (Y) ** 2), distances[3])
                ]
        case 3:
            if min2 == 2:
                equations = [
                    Eq(sympy.sqrt((X - ldist2) ** 2 + (Y - ldist2) ** 2), distances[2]),
                    Eq(sympy.sqrt((X - ldist2) ** 2 + (Y) ** 2), distances[3])
                ]
            elif min2 == 0:
                equations = [
                    Eq(sympy.sqrt((X) ** 2 + (Y) ** 2), distances[0]),
                    Eq(sympy.sqrt((X - ldist2) ** 2 + (Y) ** 2), distances[3])
                ]

    solutions = solve(equations)
    if solutions == []:
        print("---No XY Solutions!---")
        return

    for sol in solutions:
        for key in sol.keys():
            if sol[key] < 0:
                solutions.remove(sol)
            elif sol[key] > ldist2:
                solutions.remove(sol)

    if len(solutions) == 1:
        xy = [solutions[0].get("X"), solutions[0].get("Y")]
        return xy
    else:
        print("---ERR in findxy() return, xy unchanged---")


def reportMap():
    print(f"Quad: {quad} :: Dist-> [{distances[0]},{distances[1]},{distances[2]},{distances[3]}]")


if __name__ == "__main__":
    mapThread = threading.Thread(target=startmapping)
    mapThread.start()
