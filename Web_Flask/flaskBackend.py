from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/check")
def checkWorking():
    return "Hello from Flask"



@app.route("/wheels/<int:value>")
def getWheelsValue(value):
    print("v", str(value))
    #if value == 9:
        #value = "worked"
    return str(value)

#The user facing page for controlling the tango
@app.route('/')
def home():
   return render_template('index.html')

#the backend for updated values to be sent to
@app.route('/recieving', methods=['GET', 'POST'])
def parse_request():
    data = request.values  # data is empty


app.run(host="0.0.0.0", port=3245, debug=True)



