import tkinter
import pyttsx3
from random import uniform
from tkinter import *
from time import sleep
import threading
import Kore

# I'd recommend putting this on a button similar to the say command you currently have and utilizing the text box as the input
# I believe you just need to call spin_text with the text input then call spin to make it start spinning
def spin_text(text):
    root = tk.Tk()
    root.title("Spinning Text")
    canvas = tk.Canvas(root, width=400, height=200)
    canvas.pack()
    text_obj = canvas.create_text(200, 100, text=text, font=("Helvetica", 20))
    angles = cycle(range(0, 360, 10))

def spin():
    angle = next(angles)
    canvas.coords(text_obj, 200, 100)
    canvas.after(100, spin)
    canvas.move(text_obj, 2 * angle, 0)

# Use this code when initializing the movement (specifically needs to be used whenever the motors are not set to 6000)
# Create the stick figure put this in the
def walkingAnimation():
  head = canvas.create_oval(180, 50, 220, 90, fill="black")
  body = canvas.create_line(200, 90, 200, 200, fill="black")
  left_arm = canvas.create_line(200, 120, 150, 150, fill="black")
  right_arm = canvas.create_line(200, 120, 250, 150, fill="black")
  left_leg = canvas.create_line(200, 200, 150, 250, fill="black")
  right_leg = canvas.create_line(200, 200, 250, 250, fill="black")
    
  # Initial movement direction
  direction = "right"
    
  # Define movement deltas
  x_delta = 5
  y_delta = 0
  animate()
    
# Actually calls the movement command and will keep it running (double check the break out of the loop part works)
def animate():
    nonlocal direction
    direction = move_stick_figure(canvas, head, x_delta, y_delta, direction)
    if left_motor.value != 6000 && right_motor.value != 6000: # Will need to update these names to be what is in the Kore file. (basically just grabbing the speed of the motors)
      root.after(50, animate)  # Call this function again after 50 milliseconds

def move_stick_figure(canvas, stick_figure, x_delta, y_delta, direction):
    # Get the current coordinates of the stick figure
    x0, y0, x1, y1 = canvas.coords(stick_figure)
    
    # Check if the stick figure has reached the edge of the canvas
    if direction == "right" and x1 >= canvas.winfo_width():
        direction = "left"
    elif direction == "left" and x0 <= 0:
        direction = "right"
    
    # Move the stick figure by the given deltas
    canvas.move(stick_figure, x_delta, y_delta)
    
    # Update the direction
    return direction

