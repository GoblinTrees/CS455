import time
# YOUR EXPECTED DUTIES:
# Each team will need to create your own GUI to program the robot with the touch screen. You will need
# to be able to implement a timeline that holds 8 instructions for full credit. The instructions (icons you
# will place on your timeline) you will need are
#TODO
# 1. Motors with speed, distance and direction. (practice with time instead of distance until you get
# UWB radar working, or if you are out in the hallway).
def motorSpeed(speed, self):
    self.r_motors = speed + 600
    temp = speed - 6000
    self.l_motors = temp
    time.sleep(1)
    # Not sure if this belongs, should we be stopping them here or is there something else that takes care of duration? 
    self.tango.setTarget(self.L_MOTORS, self.l_motors)
    self.tango.setTarget(self.R_MOTORS, self.r_motors)

# TODO: 
def motorDirection(direction, self):
    # turn right
    if direction == "right":
        l_motors = 5000
        self.tango.setTarget(getChan(L_Motors), l_motors)
        time.sleep(.87)
        l_motors = 6000
        self.tango.setTarget(getChan(L_Motors), l_motors)
    # turn left
    elif direction == "left":
        l_motors = 7000
        self.tango.setTarget(getChan(L_Motors), l_motors)
        time.sleep(.87)
        l_motors = 6000
        self.tango.setTarget(getChan(L_Motors), l_motors)
    # drive forward
    elif direction == "forward":
        l_motors = 5400
        r_motors = 7000
        self.tango.setTarget(getChan(L_Motors), l_motors)
        self.tango.setTarget(self.R_MOTORS, r_motors)
        time.sleep(.5)
        motors = 6000
        self.tango.setTarget(getChan(L_Motors), motors)
        self.tango.setTarget(self.R_MOTORS, motors)
    # drive backwards
    elif direction == "backward":
        l_motors = 6600
        r_motors = 5000
        self.tango.setTarget(getChan(L_Motors), l_motors)
        self.tango.setTarget(self.R_MOTORS, r_motors)
        time.sleep(.5)
        motors = 6000
        self.tango.setTarget(self.L_MOTORS, motors)
        self.tango.setTarget(self.R_MOTORS, motors)
    else:
        print(direction, " is not a recognized direction.")

def motorDistance(self, distance):
    print("TODO")


# 2. Motors turn robot left, or right for x amount of seconds.
def turnLeft(self, time):
    l_motors = 7000
    self.tango.setTarget(self.L_MOTORS, l_motors)
    time.sleep(time)
    l_motors = 6000
    self.tango.setTarget(self.L_MOTORS, l_motors)

def turnLeft(self, time):
    l_motors = 5000
    self.tango.setTarget(self.L_MOTORS, l_motors)
    time.sleep(time)
    l_motors = 6000
    self.tango.setTarget(self.L_MOTORS, l_motors)
# 3. Head tilt both directions

def tiltHeadUp():
    print("TODO")

def tiltHeadDown():
    print("TODO")

# 4. Head pan both directions
def panHeadLeft():
    print("TODO")

def panHeadRight():
    print("TODO")

# 5. Waist turn both directions
# 6. A wait for human speech input
# 7. Talking, be able to type in what sentence you want to say and the robot says it. Have about four
# pre-built in sayings for a
# That is seven icons and your timeline must take 8 instructions.
# No multithreading (multiple instructions at once) need to be done.
# Full credit will be 40 points.
# 1. Being able to complete my set of commands 16 points, each command you can pull off is 2
# points ....... Example: Go forward 5 feet, turn right, go forward 7 feet, stop, look right, look
# left, turn 90 degrees left, say hello, go forward 2 feet, back up 2 feet, twist body full to
# right......etc. etc.
# a. I’ll set up an obstacle course for you to attempt to complete.
# 2. 12 points is for your GUI look and feel, ease of use and no errors on just using the GUI. There
# must be a play/start button of some kind that will run through the commands that have been
# programmed in order. For full credit you must be able to delete and clear programs or pieces of
# programs the user has developed.
# 3. 5 points is for an animation you develop while the bot is running the program. It can be
# whatever makes sense that a user might like, it can be letting the user know where you are in
# the program, or just something that makes sense.......has to be an animation, and gives your
# robot a little personality.
# This is for the people that just can’t get the 8 steps working in the step one above........
# 4. The last 7 points is if you can get the robot to dynamically any set of two commands you
# have.....this is not the real dynamic plans I give you, but just any commands that can vary
# slightly.......”a single icon that allows you to move forward x amount of seconds, and then back
# up y amount of seconds” as long as the values for x and y can dynamically be input.
# These next two rules are so you get creative with your touch screen input.....
# • If you must use a mouse to program the robot you lose 5 points. You should use the
# touchscreen if you can. Design of the GUI should allow, but it’s tough, design creatively.
# • If you must use a keyboard to program (set the icon parameters) the robot you lose 10 points.
# All executable commands must be activated


#TODO
"""
-> Make Kore.py responsive to screen size
-> add function timer slider to Kore.py
-> add delay timer slider to Kore.py
-> add Queue to Kore.py
-> add animation to webpage on Kore.py during Queue execution
-> add prebuilt sayings into Kore.py
-> add multithreading potential to Queue
"""
