from flask import Flask, render_template, request, jsonify

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
    print(body_dict)

    # Process the data (you can add your robot control logic here)



    # You can send a response if needed
    return "Received the control data successfully!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5245, debug=True)
