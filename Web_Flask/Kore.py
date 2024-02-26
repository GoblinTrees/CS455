from flask import Flask, render_template, request

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

    #set default positions
    kore.update(kore.tango_default)

    return render_template('index.html', ip_address=ip_add)

@app.route('/control', methods=['POST'])
def control_robot():
    print("control input recieved...")
    # Retrieve data from the form
    HeadTilt = int(request.form['HeadTilt'])
    HeadTurn = int(request.form['HeadTurn'])
    LShoulder = int(request.form['LShoulder'])
    LBicep= int(request.form['LBicep'])
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

    #Motor Mapping
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
    #print(body_dict)
    # Process the data (you can add your robot control logic here)
    print("updating values...")
    kore.update(body_dict)

    # You can send a response if needed
    return "Received the control data successfully!"

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    #send the data by form request in the dashboard
    if request.method == 'POST':
        # Retrieve the data from the request
        data = request.get_json()

        # Extract the text from the received data
        text = data.get('text')

        #send the data to the vocals


    #Submit data to the exec Executor
    exec.map()
    return "Hello from Flask"


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
        self.exec = ThreadPoolExecutor(max_workers=8)

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
        "L_Motors": 6000,
        "R_Motors": 6000,
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
            "Rbicep": 6600,
            "Relbow": 6000,
            "Rwrist": 6000,
            "Rclaw": 6000,
            "Waist": 6000,
            "L_Motors": 6000,
            "R_Motors": 6000,
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
        "L_Motors": 0,
        "R_Motors": 1,
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
        if (newVals.keys() != self.tango_values.keys()):
            print("Err: update()-> KEYS of tango values and update values don't match")
            return

        #Passed parameter testing -> compare and test vals, then update

        for key in self.tango_values:
            if (self.tango_values.get(key) != newVals.get(key)):
                print("Updating " + str(key) + " from " + str(self.tango_values.get(key)) + " to " + str(newVals.get(key)))
                self.tango_values[key] = newVals.get(key)
                self.tango.setTarget(self.getChan(key), self.getVal(key))
                print("Updated Key-Value:" + str(key) + "-" + str(self.getVal(key)))



    def ping(self):
        return print("Pinged Kore")

    # def execute(self, order):
    #     self.exec.submit(order)

    def speak(self, text):
        pass






#Bootup function----------------------------------------------------------
    def boot(self):
        self.exec.submit(app.run(host="0.0.0.0", port=5245, debug=True))



#End of Bootup function




#main executable funtion
if __name__ == "__main__":
    kore = Kore()
    kore.boot()
    #app.run(host="0.0.0.0", port=5245, debug=True)

    #TODO need to add control logic to wheels so as to accelerate correctly -> no L/R function, same speed each
    #TODO need to fill out exec branches: update function, and template for voice protocols
    #TODO make joystick for index page (there, but needs to be connected right
    #TODO general purpose I/O page
