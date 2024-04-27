import threading
import time

from flask import Flask, render_template, request, abort
import pyttsx3
from maestro import Controller
from sys import version_info
import threadQ
import Pose_Lib as Pl
import random

app = Flask(__name__)


@app.route('/')
def home():
    print(request.host)
    ip_add = request.host

    # set default positions
    kore.update(kore.tango_default)

    return render_template('index.html', ip_address=ip_add)


@app.route('/control', methods=['POST'])
def control_robot():
    print("control input recieved...")
    # Retrieve data from the form
    HeadTilt = int(request.form['HeadTilt'])
    HeadTurn = int(request.form['HeadTurn'])
    LShoulder = int(request.form['LShoulder'])
    LBicep = int(request.form['LBicep'])
    Lelbow = int(request.form['Lelbow'])
    Lwrist = int(request.form['Lwrist'])
    Lclaw = int(request.form['Lclaw'])
    RShoulder = int(request.form['Rshoulder'])
    RBicep = int(request.form['RBicep'])
    Relbow = int(request.form['Relbow'])
    Rwrist = int(request.form['Rwrist'])
    Rclaw = int(request.form['Rclaw'])
    Waist = int(request.form['Waist'])
    L_Motors = int(request.form['L_Motors'])
    R_Motors = int(request.form['R_Motors'])
    Duration = int(request.form['duration'])
    Delay = int(request.form['delay'])
    Words = str(request.form['UserSpeech'])

    # finish duro/delay

    # Motor Mapping
    R_Motors = int(12000) - R_Motors

    body_dict = {
        "Headtilt": HeadTilt,
        "Headturn": HeadTurn,
        "Lshoulder": LShoulder,
        "Lbicep": LBicep,
        "Lelbow": Lelbow,
        "Lwrist": Lwrist,
        "Lclaw": Lclaw,
        "RShoulder": RShoulder,
        "Rbicep": RBicep,
        "Relbow": Relbow,
        "Rwrist": Rwrist,
        "Rclaw": Rclaw,
        "Waist": Waist,
        "L_Motors": L_Motors,
        "R_Motors": R_Motors,
        "Words": Words,

    }
    # print(body_dict)
    # Process the data (you can add your robot control logic here)
    print("updating values...")
    kore.update(body_dict)

    # You can send a response if needed
    # return "Received the control data successfully!"



@app.route('/setQue')
def setQue():
    print("Setting Que...")
    print(request.host)

    # set default positions
    kore.update(kore.tango_default)



@app.route("/gui", methods=['GET', 'POST'])
def gui():
    host_ip = request.host
    client_ip = request.remote_addrclient_ip
    print("Host ip: " + str(host_ip))
    print("Client ip: " + str(client_ip))

    if (str(host_ip) != str(client_ip)):
        print("::ERR, GUI RESPONSE NOT VALID -> CANNOT CALL FROM OUTSIDE TANGO")

    return render_template('GUI_Program.html', host_ip=host_ip)



@app.before_first_request
def initialize():
    # Perform initialization tasks here, for example:
    print("Initializing the application...")
    # print("Running tests::\n")
    testcode()


def testcode():
    pass


# End of FlaskIO---------------------------------------------------------


# Maestro ControllerIO---------------------------------------------------

PY2 = version_info[0] == 2  # Running Python 2.x?


# End of Mastro ControllerIO---------------------------------------------------------

# Class def for Kore Processes
class Kore():

    def __init__(self):
        # super().__init__(self,ttyStr='/dev/ttyACM0',device=0x0c)
        # The tango object to send data to the servo controller
        self.tango = Controller()

        # vocals
        self.vocal_engine = pyttsx3.init()

        # the actual values to be manipulated for the system
        self.tango_values = {
            "Headtilt": 6000,
            "Headturn": 6000,
            "Lshoulder": 6000,
            "Lbicep": 6000,
            "Lelbow": 6000,
            "Lwrist": 6000,
            "Lclaw": 6000,
            "RShoulder": 6000,
            "Rbicep": 6000,
            "Relbow": 6000,
            "Rwrist": 6000,
            "Rclaw": 6000,
            "Waist": 6000,
            "L_Motors": 6000,
            "R_Motors": 6000,
            "Duration": 1,
            "Delay": 0,
            "Words": "~~~",

        }

        # default values reference
        self.tango_default = {
            "Headtilt": 6000,
            "Headturn": 6000,
            "Lshoulder": 6000,
            "Lbicep": 6000,
            "Lelbow": 6000,
            "Lwrist": 6000,
            "Lclaw": 6000,
            "RShoulder": 6000,
            "Rbicep": 6600,
            "Relbow": 6000,
            "Rwrist": 6000,
            "Rclaw": 6000,
            "Waist": 6000,
            "L_Motors": 6000,
            "R_Motors": 6000,
            "Duration": 1,
            "Delay": 0,
            "Words": "~~~",

        }

        # mapping for the channels of the maestro->copied from keyboard controls
        self.tango_channels = {
            "Headtilt": 4,
            "Headturn": 3,
            "Lshoulder": 11,
            "Lbicep": 12,
            "Lelbow": 13,
            "Lwrist": 15,
            "Lclaw": 16,
            "RShoulder": 5,
            "Rbicep": 6,
            "Relbow": 7,
            "Rwrist": 9,
            "Rclaw": 10,
            "Waist": 2,
            "L_Motors": 1,
            "R_Motors": 0,
            "Duration": 22,
            "Delay": 23,
            "Words": 21,

        }

        # the threading Queue-> uses Queue methods to add, then use procQ to go through all functions
        self.ComQue = threadQ.ThreadedQueue()

    def getChan(self, key):
        return self.tango_channels.get(key)

    def getVal(self, key):
        return self.tango_values.get(key)

    def updateList(self, actions: list):
        for newVals in actions:
            self.update(newVals)
            time.sleep(.3)

    def update(self, newVals):
        if self.tango_values.get("Delay") != 0:  # Delay for whatever time was preset
            time.sleep(self.tango_values.get("Delay"))

        # Arg type catch to ensure arg is a dict
        if (type(newVals) != dict):
            print("Err: update()-> function arg passed to update() is not a dictionary")
            try:
                print("Arg type: " + type(newVals))
                print("Arg passed: " + str(newVals))
            except:
                print("Cannot rep. arg as string.")
            finally:
                return
        # Dict format catch to ensure proper format->length and keys
        if (len(newVals.keys()) != len(self.tango_values.keys())):
            print("Err: update()-> LENGTH of tango values and update values don't match")
            print("len newVals keys: " + str(len(newVals)))
            print("len tangoVals keys: " + str(len(self.tango_values.keys())))
            print("newVals keys: " + str(newVals.keys()))
            print("tangoVals keys: " + str(self.tango_values.keys()))

            return
        if (newVals.keys() != self.tango_values.keys()):
            print("Err: update()-> KEYS of tango values and update values don't match")
            return

        # Passed parameter testing -> compare and test vals, then update

        for key in self.tango_values:
            if (self.tango_values.get(key) != newVals.get(key)):
                # print("Updating " + str(key) + " from " + str(self.tango_values.get(key)) + " to " + str(
                #     newVals.get(key)))
                self.tango_values[key] = newVals.get(key)
                if self.getChan(key) == 21:  # skip for words update based on channel
                    print("New Words-> " + str(self.tango_values[key]))  # print the updated words
                    continue
                elif self.getChan(key) == 22:  # Set Duration
                    print("Duration-> " + str(self.tango_values[key]))  # print the updated words
                    continue
                elif self.getChan(key) == 23:  # Set Delay
                    print("Delay-> " + str(self.tango_values[key]))  # print the updated words
                    continue
                else:
                    self.tango.setTarget(self.getChan(key), self.getVal(key))
                    print("New Motor Key-Value:" + str(key) + "-" + str(self.getVal(key)))

        time.sleep(self.tango_values.get("Duration"))  # Apply the changes for however long duration lasts

    def ping(self):
        return print("Pinged Kore")

    def speak(self, gram=None):
        if gram is not None:
            self.words = gram
        # Pass the text into the vocals (engine)
        self.vocal_engine.say(self.tango_values.get("Words"))
        # self.vocal_engine.runAndWait()

    def send_values(self):
        return self.tango_values

    # Bootup function----------------------------------------------------------
    def boot(self):
        # This line boots the FlaskIO
        app.run(host="0.0.0.0", port=5245, debug=True)

    def pose(self):
        random_pose_key = Pl.get_random_pose_key(Pl.all_poses)
        # print("Random starter pose from 'all_poses': ", random_pose_key)
        startpose = Pl.all_poses.get(random_pose_key)
        self.update(startpose)
        time.sleep(4)
        while True:
            random_pose_key2 = Pl.get_random_pose_key(Pl.all_poses)
            # print("Random starter pose from 'all_poses': ", random_pose_key2)
            endpose = Pl.all_poses.get(random_pose_key2)

            # random choice of transition
            random_number = random.randint(1, 4)
            if random_number == 1:  # Go direct
                self.update(endpose)
                time.sleep(random.randint(1000, 3000))
                startpose = self.send_values()
                continue
            elif random_number == 2:  # Go fivesteps
                steps: list = Pl.fiveStep(startpose, endpose)
                for s in steps:
                    self.update(s)
                    time.sleep(50)
                    startpose = self.send_values()
                continue
            elif random_number == 3:  # Go back after a random amount of time
                self.update(endpose)
                time.sleep(random.randint(1000, 5000))
                self.update(startpose)
                continue
            elif random_number == 4:  # stop moving and move on
                break;
            else:
                continue


# End of Bootup function


# main executable funtion
if __name__ == "__main__":
    kore = Kore()
    print(">>EXECUTUING MAIN<<")

    kore.update(kore.tango_default)

    kore.boot()

    # safety crash into default position
    kore.update(kore.tango_default)
    time.sleep(1)
    kore.update(kore.tango_default)
