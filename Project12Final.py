
import time
import serial
import time as t
import numpy as np
import pyttsx3
from maestro import Controller
import math
import RPi.GPIO as GPIO
import threading
import openai
import pyttsx3
import speech_recognition as sr


from openai import OpenAI

# client = OpenAI()  # Automatically uses API key from environment variables
client = OpenAI()

engine = pyttsx3.init()



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
        self.quad = -1      #Holds Quadrant info
        self.startmapping()         #Function call to start the multithreading to update the distances and quad in parrallel

    def speak(self,words:str):
        self.engine.say(words)
        self.engine.runAndWait()

    def startmapping(self):
        while True:
            self.findDistances()
            self.findQuad()
            self.reportMap()

    def findQuad(self):
        for d in self.distances:        #for check to see if the bot is out of bounds
            if d > 3.1:
                return -1
        return np.argmin(self.distances)

    def reportMap(self):
        print(f"Quad: {self.quad} :: Dist-> [{self.distances[0]},{self.distances[1]},{self.distances[2]},{self.distances[3]}]")

    def getVector(self,startList:list, endList:list):
        return [x - y for x, y in zip(endList, startList)]

    def getDistanceMoveVector(self):
        return [x - y for x, y in zip(self.distances, self.previous)]

    #findDistances modified to run on parrallel thread soas to constanstly update position of system
    def findDistances(self):

        while True:
            # print(">> findDist <<\n")
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
                        # print("Data: ", data)

                        if str(data[0]) == 'null' or str(data[1]) == 'null' or str(data[2]) == 'null' or str(data[3]) == 'null':
                            # print("bad data1, trying again")
                            continue    #added by forrest, but unknown if needed
                        elif str(data[0]) == 'nan' or str(data[1]) == 'nan' or str(data[2]) == 'nan' or str(data[3]) == 'nan':
                            # print("bad data2, trying again")
                            continue    #added by forrest, but unknown if needed
                        elif (data[0] == 0 or data[1] == 0 or data[2] == 0 or data[3] == 0):
                            # print("bad data3, zeros, trying again ")
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


def interrupt():
    global allStop
    global notExited
    global runcount
    global disSet
    disSet = 50

    while True:
        dist = getObject()
        if dist < disSet:
            inquiry()
            break

def getObject():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    trigPin = 24
    echoPin = 23
    GPIO.setup(trigPin, GPIO.OUT)
    GPIO.setup(echoPin, GPIO.IN)
    GPIO.output(trigPin, False)
    t.sleep(.1)
    GPIO.output(trigPin, True)
    t.sleep(.00001)
    GPIO.output(trigPin, False)
    timeout = t.time()
    while GPIO.input(echoPin) == 0:
        if (t.time() - timeout) > 3:
            print("timeout during echo")
            return None
    pulseStart = t.time()
    timeout = t.time()
    while(GPIO.input(echoPin) == 1):
        if(time.time() - timeout > 3):
            print("timeout while receiving echo")
            return None
    pulseEnd = t.time()
    pulseDuration = pulseEnd - pulseStart
    distance = pulseDuration * 17150
    distance = float(round(distance, 2))
    return distance

def inquiry():
    user_input = talk_to()
    # add dialog engine script here
    inp = {"role": "user", "content": user_input}
            # response setup for the chat
    set_personality(personality)
    response = chat_with_openai(personality, inp)

    words = response.split()  # Split the text into words
    cleaned_words = [word.strip() for word in words]  # Remove extra spaces from each word
    response_cleaned = ' '.join(cleaned_words)  # Join the cleaned words back together
            
    robot.speak(response_cleaned)

    if ("go to"):
        #get quadrant
        drive_by(desiredQuadrant)

def drive_by(quadrant):
    print("f")
    
def talk_to() -> str:
    with sr.Microphone() as source:
        r = sr.Recognizer()
        # Adjust for backround -> maybe can use speaker for ready ambient?
        r.adjust_for_ambient_noise(source)
        # Adjust for basic control
        r.dyanmic_energythreshhold = 4000
        try:
            print("***listening***")
            # this is the recorded sound
            audio = r.listen(source)
            print("***Got audio***")
            # this is what the robot hears
            word = r.recognize_google(audio)
            print(word)
            return str(word)
        except sr.UnknownValueError:
            print("***Don't know that word***")
            return "*Indecipherable*"
            # return str(Exception)
        print(":: ERR- FUNCTION OUT OF BOUNDS IN TALK_TO() ::")
        return "ERR"

#change to not require personality?
def chat_with_openai(personality, input: dict):
    #getStarter(personality).append(input)
    # print("getstarter\n")
    # print(getStarter(personality))
    # print("->Typeof: " +str(type(getStarter(personality)[0])))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        #messages=getStarter(personality),
        temperature=0.7,
        max_tokens=40
        # learning example
        # messages=[
        #     {
        #         "role": "user",
        #         "content": "Say this is a test",
        #     }
        # ],
        # model="gpt-3.5-turbo",
    )
    # Check if response is not empty and choices are available
    if response.choices and len(response.choices) > 0:
        # Return the text of the first choice
        # return response.choices[0].get("message", {}).get("content", "").strip()
        # This is current method : response.choices[0].message.content.strip()
        return response.choices[0].message.content.strip()
    else:
        return "No response from AI"  # Handle the case where there's no response

def getStarter(personality) -> list:
    # print("Personality starter:\n")
    # print(per_starters.get(personality))
    return per_starters.get(personality)



##Get direction
##wait for person to be detected by ultrasonic
##speak, then wait for human response, reply with chat gpt (detect "go to" with speech recognition, send to function instead of ai)
##if triggered "go to", drive to designated quadrant
##say goodbye, then return to start quadrant
##announce charging time, then drive to charging station
##announce charging activated, end
