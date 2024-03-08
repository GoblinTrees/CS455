import time

from flask import Flask, render_template, request
import tkinter as tk
import pyttsx3
from tkinter import *
from maestro import Controller
from sys import version_info
from concurrent.futures import ThreadPoolExecutor
import threading



app = Flask(__name__)

@app.route("/check")
def checkWorking():
    return "Hello from Flask"


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

        # send the data to the vocals
        kore.exec.submit(kore.speak(text))

    # Submit data to the exec Executor
    return "Hello from Flask"


# End of FlaskIO---------------------------------------------------------


# Maestro ControllerIO---------------------------------------------------

PY2 = version_info[0] == 2  # Running Python 2.x?


# End of Mastro ControllerIO---------------------------------------------------------

# Class def for Kore Processies
class Kore():

    def __init__(self):
        # super().__init__(self,ttyStr='/dev/ttyACM0',device=0x0c)
        # The tango object to send data to the servo controller
        # <with super, i don't think we need to do the following line-FG>
        self.tango = Controller()

        # The taskmaster executor
        self.exec = ThreadPoolExecutor(max_workers=8)


        # vocals
        self.vocal_engine = pyttsx3.init()
        # the personality window
        self.win = tk.Tk()

        # the actual values to be manipultated for the system
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


    def getChan(self, key):
        return self.tango_channels.get(key)

    def getVal(self, key):
        return self.tango_values.get(key)

    def update(self, newVals):
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


    def ping(self):
        return print("Pinged Kore")

    # def execute(self, order):
    #     self.exec.submit(order)

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
    def boot(self):
        # This line boots the FlaskIO
        app.run(host="0.0.0.0", port=5245, debug=True)

    def start_tkinter(self):
        print("...starting tkinter...")
        self.win.mainloop()

def PersonalityRun(bot: Kore):
    while True:
        animation_window.update()
        look(bot)

    print("Task ended")



#Personality stuff
def create_animation_window():
    window = tk.Tk()
    window.title("I'm awake")
    # Uses python 3.6+ string interpolation
    window.geometry(f'{animation_window_width}x{animation_window_height}')
    return window

def create_animation_canvas(window):
    canvas = tk.Canvas(window)
    canvas.configure(bg="gray")
    canvas.pack(fill="both", expand=True)
    global captions
    captions = Text(window, height=1, width=30, font=('Arial', 16, 'bold'))
    captions.place(x=200, y=510)
    head = canvas.create_oval(50, 50, 700, 500, width=5, fill="lightgray")
    eye_L = canvas.create_oval(150, 150, 350, 350, width=3, fill="white")
    eye_R = canvas.create_oval(400, 150, 600, 350, width=3, fill="white")
    global pupil_L
    pupil_L = canvas.create_oval(LLstart, LUstart, LRstart, LBstart, width=3, fill="black")
    global pupil_R
    pupil_R = canvas.create_oval(RLstart, RUstart, RRstart, RBstart, width=3, fill="black")
    return canvas

def speakThread(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def look_left(window, canvas):
    canvas.coords(pupil_L, LLcap, LUstart, LRstart, LBstart)
    canvas.coords(pupil_R, RLcap, RUstart, RRstart, RBstart)

def look_right(window, canvas):
    canvas.coords(pupil_L, LLstart, LUstart, LRcap, LBstart)
    canvas.coords(pupil_R, RLstart, RUstart, RRcap, RBstart)

def look_up(window, canvas):
    canvas.coords(pupil_L, LLstart, LUcap, LRstart, LBstart)
    canvas.coords(pupil_R, RLstart, RUcap, RRstart, RBstart)

def look_down(window, canvas):
    canvas.coords(pupil_L, LLstart, LUstart, LRstart, LBcap)
    canvas.coords(pupil_R, RLstart, RUstart, RRstart, RBcap)

def reset(window, canvas):
    canvas.coords(pupil_L, LLstart, LUstart, LRstart, LBstart)
    canvas.coords(pupil_R, RLstart, RUstart, RRstart, RBstart)


def look(bot: Kore):
    # get the bot values and decide what to do
    try:
        headTurn = bot.tango_values.get("Headturn")
        headTilt = bot.tango_values.get("Headtilt")
    except:
        print("An exception occurred:" + str(EXCEPTION))
        print("***Check look function in Project3Personality, get dict funcs***")
        return

    # normalize values by subtracting 6000->positive implies "up" from normal
    headTilt -= 6000
    headTurn -= 6000

    # rough impliment of angle dependent movement
    if (headTilt > 1500):  # Upwards looking
        look_up(animation_window, animation_canvas)

    if (headTilt < -1500):  # Down looking
        look_down(animation_window, animation_canvas)

    if (headTurn > 1500):  # Right looking
        look_right(animation_window, animation_canvas)

    if (headTurn < -1500):  # Left looking
        look_left(animation_window, animation_canvas)

    else:
        reset(animation_window, animation_canvas)

# width of the animation window
animation_window_width=800
# height of the animation window
animation_window_height=600
LLcap = 100
LRcap = 400
LLstart = 225
LRstart = 275
LUcap = 100
LBcap = 400
LUstart = 225
LBstart = 275

RLcap = 350
RRcap = 650
RLstart = 475
RRstart = 525
RUcap = 100
RBcap = 400
RUstart = 225
RBstart = 275

pupil_L = None
pupil_R = None

captions = None
command1 = 'test one'
command2 = 'test 2'
command3 = 'test3'
language = 'en'
# delay between successive frames in seconds
animation_refresh_seconds = 0.01

# main executable funtion
if __name__ == "__main__":
    animation_window = create_animation_window()
    animation_canvas = create_animation_canvas(animation_window)
    kore = Kore()

    # Create threads for Flask and Tkinter
    flask_thread = threading.Thread(target=kore.boot)
    tkinter_thread = threading.Thread(target=kore.start_tkinter)

    # Start both threads
    flask_thread.start()
    tkinter_thread.start()

    # Wait for both threads to finish
    flask_thread.join()
    tkinter_thread.join()


