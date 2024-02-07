from flask import Flask

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

app.run(host="0.0.0.0")

