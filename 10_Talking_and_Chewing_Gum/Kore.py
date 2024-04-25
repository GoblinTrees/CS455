import time

from flask import Flask, render_template, request, abort
import pyttsx3
from maestro import Controller
from sys import version_info
import threadQ
import Pose_Lib

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
    L_motors = int(request.form['L_Motors'])
    R_motors = int(request.form['R_Motors'])
    Duration = int(request.form['duration'])
    Delay = int(request.form['delay'])

    # TODO finish using duration/delay

    # Motor Mapping
    R_motors = int(12000) - R_motors

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
        "L_Motors": L_motors,
        "R_Motors": R_motors,
    }
    # print(body_dict)
    # Process the data (you can add your robot control logic here)
    print("updating values...")
    kore.update(body_dict)

    # You can send a response if needed
    return "Received the control data successfully!"


@app.route("/voice", methods=['GET', 'POST'])
def voice():
    # send the data by form request in the dashboard
    if request.method == 'POST':
        # Retrieve the data from the request
        data = request.get_json()

        # Extract the text from the received data
        text = data.get('text')

        # send the data to the vocals OPTION 1
        kore.speak(text)

    return "Hello from Flask"


@app.route("/gui", methods=['GET', 'POST'])
def gui():
    host_ip = request.host
    client_ip = request.remote_addrclient_ip = request.remote_addr
    print("Host ip: " + str(host_ip))
    print("Client ip: " + str(client_ip))

    if (str(host_ip) != str(client_ip)):
        print("::ERR, GUI RESPONSE NOT VALID -> CANNOT CALL FROM OUTSIDE TANGO")
        abort(403)  # Forbidden

    # Passed forbidden zone: show gui interface


# End of FlaskIO---------------------------------------------------------


# Maestro ControllerIO---------------------------------------------------

PY2 = version_info[0] == 2  # Running Python 2.x?


# End of Mastro ControllerIO---------------------------------------------------------

# Class def for Kore Processies
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
        }

        # the threading Queue-> uses Queue methods to add, then use procQ to go through all functions
        self.threadQ = threadQ.ThreadedQueue()

    def getChan(self, key):
        return self.tango_channels.get(key)

    def getVal(self, key):
        return self.tango_values.get(key)

    def update(self, newVals: dict):
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
                print("Updating " + str(key) + " from " + str(self.tango_values.get(key)) + " to " + str(
                    newVals.get(key)))
                self.tango_values[key] = newVals.get(key)
                self.tango.setTarget(self.getChan(key), self.getVal(key))
                print("Updated Key-Value:" + str(key) + "-" + str(self.getVal(key)))

    def update_List(self, newVals: list):
        if not newVals:
            print("Warning: Empty list passed to update_List()")
            return
        # Arg type catch to ensure arg is a dict
        if (type(newVals[0]) != dict):
            print("Err: update()-> function arg passed to update() INSIDE LIST is not a dictionary")
            try:
                print("Arg type: " + type(newVals[0]))
                print("Arg passed: " + str(newVals[0]))
            except:
                print("Cannot rep. arg as string IN LIST")
            finally:
                return

        # Passed parameter testing -> compare and test vals, then update
        for pose in newVals:
            if not isinstance(pose, dict):
                print("Error: Element inside the list is not a dictionary")
                continue
            for key in pose:
                if key not in self.tango_values:
                    print("Warning: Key '{}' not found in Tango values".format(key))
                    continue
                    #actually do something here
                if (self.tango_values.get(key) != pose.get(key)):
                    print("Updating " + str(key) + " from " + str(self.tango_values.get(key)) + " to " + str(
                        pose.get(key)))
                    self.tango_values[key] = pose.get(key)
                    self.tango.setTarget(self.getChan(key), self.getVal(key))
                    print("Updated Key-Value:" + str(key) + "-" + str(self.getVal(key)))
        time.sleep(500)

    def ping(self):
        return print("Pinged Kore")

    def speak(self, text):
        # Pass the text into the vocals (engine)
        self.vocal_engine.say(text)
        self.vocal_engine.runAndWait()

    def send_values(self):
        return self.tango_values

    # Bootup function----------------------------------------------------------
    def boot(self):
        # This line boots the FlaskIO
        app.run(host="0.0.0.0", port=5245, debug=True)


# End of Bootup function


# main executable funtion
if __name__ == "__main__":
    kore = Kore()

    # Create threads for Flask and Tkinter
    # flask_thread = threading.Thread(target=kore.boot)

    # Start both threads
    # flask_thread.start()
    #
    # fordict = kore.tango_default
    # fordict.update({"L_Motors": 5400})
    # fordict.update({"R_Motors": 7000})
    #
    # kore.update(fordict)
    # time.sleep(1)
    #
    # fordict.update({"L_Motors": 6000})
    # fordict.update({"R_Motors": 6000})
    # kore.update(fordict)