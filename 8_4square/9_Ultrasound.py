import RPi.GPIO as GPIO
import time

# set GPIO mode
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
TRIG_PIN = 24
ECHO_PIN = 23

# set trig as output anc ECHO as input
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def getDistance():
    # set TRIG to LOW for a short time to ensure a clean signal
    GPIO.setmode(GPIO.BCM)
    trigPin = 14
    echoPin = 17
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
        if(time.time() - timeout) > 3:
            print("timeout while receiving echo")
            return None
    pulseEnd = t.time()
    pulseDuration = pulseEnd - pulseStart
    distance = pulseDuration * 17150
    distance = round(distance, 2)
    return distance
    
print("Diatance: ", getDistance())

