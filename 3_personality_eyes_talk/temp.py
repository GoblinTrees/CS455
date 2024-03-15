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

    def driving(self):
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
        self.canvas.delete(eye_left, eye_right, pupil_left, pupil_right, head, smile)
        self.canvas.create_rectangle(90, 280, 110, 320, fill="lightgray")  # Closed eyes
        self.root.update()
        time.sleep(0.2)  # Duration eyes are closed

    def perform_action(self, action, *args):
        if action == "drive":
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
                self.blink_eyes()  # Blink animation for eyes
                self.driving()  # Driving animation for the stick figure
                self.root.update()
                time.sleep(1)  # Adjust the idle animation duration as needed

    def talk(self, words):
        # Animation for talking (you can customize this)
        self.canvas.create_text(200, 300, text=words, font=("Helvetica", 12))

        # Text-to-speech
        self.engine.say(words)
        self.engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    robot = Robot(root)
    robot.run()
