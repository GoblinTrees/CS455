import time
import threading
import tkinter as tk
import pyttsx3

class Robot:
    def __init__(self, root):
        self.is_idle = True
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.engine = pyttsx3.init()
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

    def move_stick_figure(self, x, y):
        # Clear canvas
        self.canvas.delete("stick_figure")
        # Draw stick figure
        self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="black", tags="stick_figure")
        self.canvas.create_line(x, y, x, y+30, fill="black", tags="stick_figure")
        self.canvas.create_line(x, y+30, x-20, y+50, fill="black", tags="stick_figure")
        self.canvas.create_line(x, y+30, x+20, y+50, fill="black", tags="stick_figure")
        self.canvas.create_line(x, y+10, x-10, y+20, fill="black", tags="stick_figure")
        self.canvas.create_line(x, y+10, x+10, y+20, fill="black", tags="stick_figure")

    def move_arm(self):
        # Animation for moving arm on canvas
        pass

    def turn_wheels(self):
        # Animation for turning wheels on canvas
        self.move_stick_figure(50, 200)
        for _ in range(20):
            self.move_stick_figure(50, 200)
            self.root.update()
            time.sleep(0.1)
            self.move_stick_figure(150, 200)
            self.root.update()
            time.sleep(0.1)

    def talk(self, words):
        # Animation for talking (you can customize this)
        self.canvas.create_text(200, 200, text=words)

        # Text-to-speech
        self.engine.say(words)
        self.engine.runAndWait()

    def idle_animation(self):
        self.canvas.configure(bg="gray")
        self.canvas.pack(fill="both", expand=True)
        head = self.canvas.create_oval(50, 50, 700, 500, width=5, fill="lightgray")
        eye_L = self.canvas.create_oval(150, 150, 350, 350, width=3, fill="white")
        eye_R = self.canvas.create_oval(400, 150, 600, 350, width=3, fill="white")
        global pupil_L
        pupil_L = self.canvas.create_oval(self.LLstart, self.LUstart, self.LRstart, self.LBstart, width=3, fill="black")
        global pupil_R
        pupil_R = self.canvas.create_oval(self.RLstart, self.RUstart, self.RRstart, self.RBstart, width=3, fill="black")

    def perform_action(self, action, *args):
        if action == "move_arm":
            self.move_arm()
        elif action == "turn_wheels":
            self.turn_wheels()
        elif action == "talk":
            self.talk(*args)
        else:
            print("Unknown action")

    def action_thread(self, action, *args):
        thread = threading.Thread(target=self.perform_action, args=(action, *args))
        thread.start()

    def run(self):
        while True:
            if self.is_idle:
                self.idle_animation()
                self.root.update()
                time.sleep(2)  # Adjust the idle animation duration as needed
            else:
                # Example: Robot is asked to move arm and talk simultaneously
                self.action_thread("turn_wheels")
                self.action_thread("talk", "I'm turning the wheels!")
                time.sleep(2)  # Adjust the duration between actions as needed
                self.is_idle = True  # Set robot to idle state after actions

if __name__ == "__main__":
    root = tk.Tk()
    robot = Robot(root)
    robot.run()
