import serial
import time as t
import numpy as np
import pyttsx3
from maestro import Controller
import math


def findDistances():
    # print("in function")
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
        while confidenceInt < 10:
            print("ConInt: ", confidenceInt)
            temp = ser.readline()
            dataentry = ser.readline().split(",")
            print("Dataentry:\n")
            print(dataentry)

            data = [dataentry[1], dataentry[2], dataentry[3], dataentry[4]]
            # print("Data1: ",data[1])
            if str(data[0]) == 'null' or str(data[1]) == 'null' or str(data[2]) == 'null' or str(data[3]) == 'null':
                print("bad data1, trying again")
            elif str(data[0]) == 'nan' or str(data[1]) == 'nan' or str(data[2]) == 'nan' or str(data[3]) == 'nan':
                print("bad data2, trying again")
            elif (data[0] == 0 or data[1] == 0 or data[2] == 0 or data[3] == 0):
                print("baddata3")

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
        print(data)
    finally:
        print("HI")

    # num1 = num1 / 1000
    # num2 = num2 / 1000
    # num3 = num3 / 1000
    # num4 = num4 / 1000
    #
    #
    # print("got data")
    # ser.close()
    # return [num1, num2, num3, num4]


if __name__ == "__main__":
    while (True):
        findDistances()
