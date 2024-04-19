import time
import serial
import time as t
import numpy as np
import pyttsx3
from maestro import Controller
import math

class Robot:
    def __init__(self):
        self.L_MOTORS = 1
        self.R_MOTORS = 0
        self.r_motors = 6000
        self.l_motors = 6000
        self.tango = Controller()
        self.engine = pyttsx3.init()

    def speak(self, words: str):
        self.engine.say(words)
        self.engine.runAndWait()

robot = Robot()
count = 0
quadNum = 5

def findDistances():
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
        while confidenceInt < 10:
            print("ConInt: ", confidenceInt)
            temp = ser.readline()
            dataentry = ser.readline()
            data = [dataentry[1],dataentry[2],dataentry[3],dataentry[4]]
            print("Data: ",data)
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
                #2nd data validation
                # print(data[0])
                # print(data[1])
                # print(data[2])
                # print(data[3])

        num1 = num1 / 1000
        num2 = num2 / 1000
        num3 = num3 / 1000
        num4 = num4 / 1000


        print("got data")
        ser.close()
        return [num1, num2, num3, num4]
    finally:
        print("finally")
        ser.close()

def find_closest_corner_angle(distances, current_orientation):
    # Check if the input list contains 4 distances
    if len(distances) != 4:
        raise ValueError("Input list must contain 4 distances")

    # Calculate the distances squared
    dist_sq = [d ** 2 for d in distances]

    # Calculate the angles using the law of cosines
    angles = [math.acos((dist_sq[(i + 1) % 4] + dist_sq[(i + 3) % 4] - dist_sq[i]) / (2 * distances[(i + 1) % 4] * distances[(i + 3) % 4])) for i in range(4)]

    # Find the index of the smallest angle
    min_angle_index = angles.index(min(angles))

    # Calculate the angle between the current heading and the closest corner
    closest_corner_angle = min_angle_index * (math.pi / 2)

    # Calculate the difference between current orientation and closest corner angle
    angle_difference = closest_corner_angle - current_orientation

    # Normalize angle difference to be between -pi and pi
    angle_difference = (angle_difference + math.pi) % (2 * math.pi) - math.pi

    # Determine the direction to turn
    if abs(angle_difference) < math.pi:
        # Turn in the direction that minimizes the angle difference
        if angle_difference > 0:
            turn_direction = "right"
        else:
            turn_direction = "left"
    else:
        # Turn in the opposite direction
        if angle_difference > 0:
            turn_direction = "left"
        else:
            turn_direction = "right"

    return turn_direction, abs(angle_difference)

# Orientation method, starts with 0 degrees pointing at the right side of the square
def estimate_orientation_with_error(distances, error_bounds):
    # Check if the input lists contain 4 distances and 4 error bounds
    if len(distances) != 4 or len(error_bounds) != 4:
        raise ValueError("Input lists must contain 4 elements")

    # Calculate the ranges of distances considering error bounds
    distance_ranges = [(dist - error, dist + error) for dist, error in zip(distances, error_bounds)]

    # Calculate the differences between opposite sensors' ranges
    opposite_differences = [abs(dist_range[0] - dist_range[1]) for dist_range in distance_ranges]

    # Find the sensor pair with the smallest difference
    min_difference_index = np.argmin(opposite_differences)

    # Find the sensor pair with the largest difference
    max_difference_index = np.argmax(opposite_differences)

    # Estimate orientation based on differences
    if max_difference_index == min_difference_index:
        # The robot is likely oriented diagonally relative to the square
        orientation = (max_difference_index * np.pi / 2 + np.pi) % (2 * np.pi)
    else:
        # The robot is likely oriented facing one of the sides of the square
        orientation = (min_difference_index * np.pi / 2) % (2 * np.pi)

    return orientation

# uncertain about these motor values for if they will turn the robot in the correct direction
def turnLeft(angle):
    #.01 sec per degree
    l_motors = 5000
    robot.tango.setTarget(robot.L_MOTORS, l_motors)
    t.sleep(.01 * angle)
    l_motors = 6000
    robot.tango.setTarget(robot.L_MOTORS, l_motors)

def turnRight(angle):
    #.01 sec per degree
    r_motors = 7000
    robot.tango.setTarget(robot.R_MOTORS, r_motors)
    t.sleep(.01 * angle)
    r_motors = 6000
    robot.tango.setTarget(robot.R_MOTORS, r_motors)

def leaveSquare(distance):
    # parametrized distance, uses the distance to the pylon instead of nominal distance so it should be an overestimate.
    exitTime = distance/.347
    l_motors = 5400
    r_motors = 7000
    robot.tango.setTarget(robot.L_MOTORS, l_motors)
    robot.tango.setTarget(robot.R_MOTORS, r_motors)
    t.sleep(exitTime)
    motors = 6000
    robot.tango.setTarget(robot.L_MOTORS, motors)
    robot.tango.setTarget(robot.R_MOTORS, motors)
    print("exited")
    robot.speak("Exited")

def findQuadrant():
    data = findDistances()
    min = np.argmin(data)
    print("Min Quad: "+ str(min))
    robot.speak("In quadrant "+ str(min))
    return min

# Code that runs
def main():
    quadNum = findQuadrant()
    # Inputs: distance and acceptable error bounds
    distances = findDistances() # finds the average distance to the sensors after 10 data points
    error_bounds = [.5, .5, .5, .5]  # assuming the two closest sensor distances will be within .5 meters of one another

    estimated_orientation = estimate_orientation_with_error(distances, error_bounds)
    print("Estimated orientation:", np.degrees(estimated_orientation), "degrees")

    direction, angle = find_closest_corner_angle(distances, estimated_orientation)
    print("Turn", direction, "to face closest corner, angle:", math.degrees(angle), "degrees")

    if direction == "left":
        turnLeft(angle)
        leaveSquare(distances[quadNum])
    elif direction == "right":
        turnRight(angle)
        leaveSquare(distances[quadNum])
    else:
        robot.speak("I'm lost")
        print("No direction found")

main()