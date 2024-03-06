import tkinter as tk
from itertools import cycle
import time
#import keyboard
import pyttsx3
from random import uniform
from tkinter import *
from time import sleep
import threading


# width of the animation window
animation_window_width=800
# height of the animation window
animation_window_height=600
LLcap = 100
LRcap = 400
LLstart = 225
LRstart = 275
LUcap = 100
LBcap = 400
LUstart = 225
LBstart = 275

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

captions = None
command1 = 'test one'
command2 = 'test 2'
command3 = 'test3'
language = 'en'
# delay between successive frames in seconds
animation_refresh_seconds = 0.01

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
# method calls to actually make it run
# spin()
# root.mainloop()

# Example usage:
spin_text("Hello, spinning text!")

def create_animation_window():
  window = tkinter.Tk()
  window.title("I'm awake")
  # Uses python 3.6+ string interpolation
  window.geometry(f'{animation_window_width}x{animation_window_height}')
  return window

def create_animation_canvas(window):
  canvas = tkinter.Canvas(window)
  canvas.configure(bg="gray")
  canvas.pack(fill="both", expand=True)
  global captions
  captions = Text(window, height=1,width=30, font=('Arial',16,'bold'))
  captions.place(x=200,y=510)
  head = canvas.create_oval(50, 50, 700, 500, width=5,fill="lightgray")
  eye_L = canvas.create_oval(150, 150, 350,350,width=3,fill="white")
  eye_R = canvas.create_oval(400,150,600,350,width=3,fill="white")
  global pupil_L
  pupil_L = canvas.create_oval(LLstart,LUstart,LRstart,LBstart,width=3,fill="black")
  global pupil_R
  pupil_R = canvas.create_oval(RLstart,RUstart,RRstart,RBstart,width=3,fill="black")
  return canvas

def speakThread(command):
  engine = pyttsx3.init()
  engine.say(command)
  engine.runAndWait()
def speak():
  #engine = pyttsx3.init()
  for x in (command1, command2, command3):
    temp = ''
    t1 = threading.Thread(target=speakThread, args=(x,))
    t1.start()
    for y in x:
      temp = temp + y
      captions.delete("1.0", "end")
      captions.insert(END,temp)
      captions.update()
      sleep(uniform(0.1, 0.4))
    t1.join()
    #engine.say(x)
    #engine.runAndWait()
##    if x != command3:
##      sleep(1)

def look_left(window,canvas):
  canvas.coords(pupil_L, LLcap, LUstart, LRstart, LBstart)
  canvas.coords(pupil_R, RLcap, RUstart, RRstart, RBstart)
def look_right(window,canvas):
  canvas.coords(pupil_L, LLstart, LUstart, LRcap, LBstart)
  canvas.coords(pupil_R, RLstart, RUstart, RRcap, RBstart)
def look_up(window,canvas):
  canvas.coords(pupil_L, LLstart, LUcap, LRstart, LBstart)
  canvas.coords(pupil_R, RLstart, RUcap, RRstart, RBstart)
def look_down(window,canvas):
  canvas.coords(pupil_L, LLstart, LUstart, LRstart, LBcap)
  canvas.coords(pupil_R, RLstart, RUstart, RRstart, RBcap)
def reset(window, canvas):
  canvas.coords(pupil_L, LLstart, LUstart, LRstart, LBstart)
  canvas.coords(pupil_R, RLstart, RUstart, RRstart, RBstart)


animation_window = create_animation_window()
animation_canvas = create_animation_canvas(animation_window)

while True:
    animation_window.update()
    if keyboard.is_pressed("a"):
      look_left(animation_window, animation_canvas)
    elif keyboard.is_pressed("w"):
      look_up(animation_window, animation_canvas)
    elif keyboard.is_pressed("d"):
      look_right(animation_window, animation_canvas)
    elif keyboard.is_pressed("s"):
      look_down(animation_window, animation_canvas)
    elif keyboard.is_pressed("left"):
      look_left(animation_window, animation_canvas)
    elif keyboard.is_pressed("right"):
      look_right(animation_window, animation_canvas)
    elif keyboard.is_pressed("ESC"):
      animation_window.destroy()
      break
    elif keyboard.is_pressed("space"):
      speak()
    else: reset(animation_window, animation_canvas)
print("Task ended")
