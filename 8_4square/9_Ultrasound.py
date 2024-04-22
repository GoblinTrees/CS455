import RPi.GPIO as GPIO
import time

# set GPIO mode
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
TRIG_PIN = 23
ECHO_PIN = 24

# set trig as output anc ECHO as input
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def getDistance():
    # set TRIG to LOW for a short time to ensure a clean signal
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)

    # send a 10us pulse to trigger
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # Measure the time it takes for the echo to return
    while GPIO.input(ECHO_PIN) == 0:
        if (time.time() - timeout) > 3:  # timeout after 1 sec
            print("Timeout occured while recieving ...")
            return None
    pulse_start = time.time()
    timeout = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        if (time.time() - timeout) > 3:  # timeout after 1 sec
            print("Timeout occured while recieving ...")
            return None
    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    #speed of sound is 343 m/s
    distance = pulse_duration * 17150
    distance = round(distance,2)
    return distance
    
print(getDistance())

