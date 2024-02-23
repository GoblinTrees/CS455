import tkinter
import time
import pyttsx3
from random import uniform
from tkinter import *
from time import sleep
from maestro import Controller

class KeyControl():
   def __init__(self,win):
      self.headTurn = 6000
      self.headTilt = 6000

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

def speak(window,canvas):
  engine = pyttsx3.init()
  for x in (command1, command2, command3):
    temp = ''
    for y in x:
      temp = temp + y
      captions.delete("1.0", "end")
      captions.insert(END,temp)
      captions.update()
      sleep(uniform(0.1, 0.4))
    engine.say(x)
    engine.runAndWait()
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

win = tk.Tk()
keys = KeyControl(win)
win.mainloop()

#Initialize Ports
HEADTURN = 3
HEADTILT = 4

# Head
win.bind('<w>', keys.head)
win.bind('<s>', keys.head)
win.bind('<a>', keys.head)
win.bind('<d>', keys.head)
win.bind('<Escape>', keys.head)
win.bind('<space>', keys.head) # currently unbound to a function


def head(self, key):
        print(key.keycode)
        print(key.keysym)
        while true:
          match key:
            # a 
              case 38:
                  self.headTurn += 200
                  if self.headTurn > 7900:
                      self.headTurn = 7900
                  self.tango.setTarget(HEADTURN, self.headTurn)
                  look_left(animation_window, animation_canvas)
              # d
              case 40:
                  self.headTurn -= 200
                  if self.headTurn < 1510:
                      self.headTurn = 1510
                  self.tango.setTarget(HEADTURN, self.headTurn)
                  look_right(animation_window, animation_canvas)
              # w
              case 25:
                  self.headTilt += 200
                  if self.headTilt > 7900:
                      self.headTilt = 7900
                  self.tango.setTarget(HEADTILT, self.headTilt)
                  look_up(animation_window, animation_canvas)
              # s
              case 39:
                  self.headTilt -= 200
                  if self.headTilt < 1510:
                      self.headTilt = 1510
                  self.tango.setTarget(HEADTILT, self.headTilt)
                  look_down(animation_window, animation_canvas)
              case 9: 
                self.headTilt = 6000
                self.tango.setTarget(HEADTILT, self.headTilt)
                animation_window.destroy()
                break
             # Space Bar is to speak
              case 21:
                speak(animation_window, animation_canvas)
             # base case
              case _:
                reset(animation_window, animation_canvas)
   
      

