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


        while True:
            temp = ser.readline()
            dataentry = str(ser.readline()).split(",")
            print("Dataentry:\n")
            print(dataentry)
    finally:
        print("HI")


if __name__ == "__main__":
    while (True):
        findDistances()
