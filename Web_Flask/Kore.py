from flask import Flask, render_template, request
import serial

#import maestro
from maestro import Controller
from sys import version_info
from concurrent.futures import ThreadPoolExecutor


#FlaskIO code-----------------------------------------------------------
app = Flask(__name__)

@app.route("/check")
def checkWorking():
    return "Hello from Flask"

@app.route('/')
def home():
    print(request.host)
    ip_add = request.host
    return render_template('index.html', ip_address=ip_add)

@app.route('/control', methods=['POST'])
def control_robot():
    print("control input recieved...")
    # Retrieve data from the form
    HeadTilt = int(request.form['slider1'])
    HeadTurn = int(request.form['slider2'])
    LShoulder = int(request.form['slider3'])
    LBicep= int(request.form['slider4'])
    Lelbow = int(request.form['slider5'])
    Lwrist = int(request.form['slider6'])
    Lclaw = int(request.form['slider7'])
    RShoulder = int(request.form['slider8'])
    RBicep = int(request.form['slider9'])
    Relbow = int(request.form['slider10'])
    Rwrist = int(request.form['slider11'])
    Rclaw = int(request.form['slider12'])
    Waist = int(request.form['slider13'])
    XJoy = int(request.form['joystickX'])
    YJoy = int(request.form['joystickY'])



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
        "XJoy": XJoy,
        "YJoy": YJoy
    }
    #print(body_dict)

    # Process the data (you can add your robot control logic here)
    print("updating values...")
    kore.update(body_dict)

    # You can send a response if needed
    return "Received the control data successfully!"
#End of FlaskIO---------------------------------------------------------





#Maestro ControllerIO---------------------------------------------------

PY2 = version_info[0] == 2   #Running Python 2.x?

#End of Mastro ControllerIO---------------------------------------------------------

#Class def for Kore Processies
class Kore():

    def __init__(self):
        #super().__init__(self,ttyStr='/dev/ttyACM0',device=0x0c)
        #The tango object to send data to the servo controller
        #<with super, i don't think we need to do the following line-FG>
        self.tango = Controller()

        #The taskmaster executor
        exec = ThreadPoolExecutor(max_workers=8)

        #the actual values to be manipultated for the system
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
        "XJoy": 0,
        "YJoy": 0,
        }

        #default values reference
        self.tango_default = {
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
            "XJoy": 0,
            "YJoy": 0,
        }

        #mapping for the channels of the maestro->copied from keyboard controls
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
        #Need to add the values for Motors later
        "XJoy": 0,
        "YJoy": 1,
        }

    def getChan(self,key):
        return self.tango_channels.get(key)

    def getVal(self,key):
        return self.tango_values.get(key)

    def update(self,newVals):
        #Arg type catch to ensure arg is a dict
        if (type(newVals) != dict):
            print("Err: update()-> function arg passed to update() is not a dictionary")
            try:
                print("Arg type: " + type(newVals))
                print("Arg passed: " + str(newVals))
            except:
                print("Cannot rep. arg as string.")
            finally: return
        #Dict format catch to ensure proper format->length and keys
        if (len(newVals.keys()) != len(self.tango_values.keys())):
            print("Err: update()-> LENGTH of tango values and update values don't match")
            print("len newVals keys: " + str(len(newVals)))
            print("len tangoVals keys: " +str(len(self.tango_values.keys())))
            print("newVals keys: " +str(newVals.keys()))
            print("tangoVals keys: " +str(self.tango_values.keys()))

            return
        if (newVals.keys() != self.tango.keys):
            print("Err: update()-> KEYS of tango values and update values don't match")
            return

        #Passed parameter testing -> compare and test vals, then update
        for key in self.tango_values:
            if (self.tango_values.get(key) != newVals.get(key)):
                print("Updating " + key + " from " +self.tango_values.get(key) + " to " + newVals.get(key))
                self.tango_values[key] = newVals.get(key)
                self.tango.setTarget(self.getChan(key), self.getVal(key))
                print("Updated Key-Value:" + key + "-" + self.getVal(key))


    def ping(self):
        return print("Pinged Kore")







#Bootup function----------------------------------------------------------



#End of Bootup function




#main executable funtion
if __name__ == "__main__":
    kore = Kore()
    app.run(host="0.0.0.0", port=5245, debug=True)
