
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

    def speak(self,words:str):
        self.engine.say(words)
        self.engine.runAndWait()

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
