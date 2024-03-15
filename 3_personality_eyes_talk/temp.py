import time
import threading
import tkinter as tk
import pyttsx3

class Robot:
    def __init__(self, root):
        self.is_idle = True
        self.isDriving = False  # Flag to indicate if driving animation is active
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.engine = pyttsx3.init()
        self.L_MOTORS = 1
        self.R_MOTORS = 0
        self.r_motors = 6000
        self.l_motors = 6000

        root.bind('<Up>', self.handle_arrow_key)
        root.bind('<Left>', self.handle_arrow_key)
        root.bind('<Down>', self.handle_arrow_key)
        root.bind('<Right>', self.handle_arrow_key)
        root.bind('<space>', self.handle_arrow_key)

    def set_driving(self, status):
        self.isDriving = status

    def handle_arrow_key(self, event):
        if event.keysym == 'Up':
            self.move_forward()
        elif event.keysym == 'Down':
            self.move_backward()
        elif event.keysym == 'Left':
            self.turn_left()
        elif event.keysym == 'Right':
            self.turn_right()
        elif event.keysym == 'space':
            self.emergency_stop()

    def move_forward(self):
        # Implement logic to move forward
        if self.l_motors == 6000:
                    self.r_motors = 6600
                    self.l_motors = 5800
        else:
            self.l_motors -= 200
            if self.r_motors > 7900:
                self.r_motors = 7900
            # Increment speed by 200 in the forward direction
            self.r_motors += 200
        self.tango.setTarget(self.L_MOTORS, self.l_motors)
        self.tango.setTarget(self.R_MOTORS, self.r_motors)
        pass

    def move_backward(self):
        # Implement logic to move backward
        if self.l_motors == 6000:
                    self.r_motors = 5400
                    self.l_motors = 6200
        else:
            self.l_motors += 200
            if self.r_motors < 1510:
                self.r_motors = 1510
            # Increment speed by 200 in the reverse direction
            self.r_motors -= 200

        self.tango.setTarget(self.L_MOTORS, self.l_motors)
        self.tango.setTarget(self.R_MOTORS, self.r_motors)
        pass

    def turn_left(self):
        # Implement logic to turn left
        self.r_motors += 200
        if (self.r_motors > 7900):
            self.r_motors = 7900
        self.tango.setTarget(self.R_MOTORS, self.r_motors)
        pass

    def turn_right(self):
        # Implement logic to turn right
        self.l_motors -= 200
        if (self.l_motors < 2110):
            self.l_motors = 2110
        self.tango.setTarget(self.L_MOTORS, self.l_motors)
        pass

    def emergency_stop(self):
        self.l_motors = 6000
        self.r_motors = 6000
        # Implement logic for emergency stop
        self.tango.setTarget(self.L_MOTORS, self.l_motors)
        self.tango.setTarget(self.R_MOTORS, self.r_motors)
        pass

    def drive(self):
        # Animation for driving
        self.canvas.create_rectangle(0, 0, 800, 600, fill="lightgray")
        self.move_stick_figure()

    def move_stick_figure(self, x=100, y=200):
        # Clear canvas
        self.canvas.delete("stick_figure")
        # Draw stick figure
        self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="black", tags="stick_figure")
        self.canvas.create_line(x, y, x, y+30, fill="black", tags="stick_figure")
        self.canvas.create_line(x, y+30, x-20, y+50, fill="black", tags="stick_figure")
        self.canvas.create_line(x, y+30, x+20, y+50, fill="black", tags="stick_figure")
        self.canvas.create_line(x, y+10, x-10, y+20, fill="black", tags="stick_figure")
        self.canvas.create_line(x, y+10, x+10, y+20, fill="black", tags="stick_figure")

    def blink_eyes(self):
        # Draw head
        head = self.canvas.create_oval(70, 250, 230, 350, fill="lightgray")

        # Draw eyes
        eye_left = self.canvas.create_oval(90, 280, 110, 320, fill="white")
        eye_right = self.canvas.create_oval(190, 280, 210, 320, fill="white")

        # Draw pupils
        pupil_left = self.canvas.create_oval(95, 290, 105, 310, fill="black", tags="pupil_left")
        pupil_right = self.canvas.create_oval(195, 290, 205, 310, fill="black", tags="pupil_right")

        # Draw smile
        smile = self.canvas.create_arc(120, 320, 180, 340, start=0, extent=180, style=tk.ARC)

        # Blink animation
        time.sleep(0.3)  # Duration eyes are closed
        self.canvas.delete(eye_left, eye_right, pupil_left, pupil_right)
        self.root.update()
        time.sleep(0.2)  # Duration eyes are closed
        # Draw eyes
        eye_left = self.canvas.create_oval(90, 280, 110, 320, fill="white")
        eye_right = self.canvas.create_oval(190, 280, 210, 320, fill="white")

        # Draw pupils
        pupil_left = self.canvas.create_oval(95, 290, 105, 310, fill="black", tags="pupil_left")
        pupil_right = self.canvas.create_oval(195, 290, 205, 310, fill="black", tags="pupil_right")

    def perform_action(self, action, *args):
        if action == "drive":
            self.drive()
        elif action == "talk":
            self.talk(*args)
        else:
            print("Unknown action")

    def action_thread(self, action, *args):
        thread = threading.Thread(target=self.perform_action, args=(action, *args))
        thread.start()

    def run(self):
        while True:
            if self.is_idle and not self.isDriving:  # Display idle animation if not driving
                self.blink_eyes()  # Blink animation for eyes
                self.root.update()
                time.sleep(1)  # Adjust the idle animation duration as needed
            elif self.isDriving:  # Display driving animation if driving
                self.drive()
                self.root.update()
                time.sleep(0.1)  # Adjust the driving animation duration as needed

    def talk(self, words):
        # Animation for talking (you can customize this)
        self.canvas.create_text(200, 300, text=words, font=("Helvetica", 12))

        # Text-to-speech
        self.engine.say(words)
        self.engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    robot = Robot(root)
    thread = threading.Thread(target=robot.run)
    thread.start()
    root.mainloop()
