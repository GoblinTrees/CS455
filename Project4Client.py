import socket
import sys
import time

host = 'localhost'
port = 5000

global token
token = 110

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

id = 1
next = 0

script = {0: [("rec", "Hi", 1), ("rec", "I was just going to say the same thing about you. Where are you from?", 1), ("rec", "Me too. Bozeman, Montana", 1),
              ("rec", "Me too, wow that is wild. What is your name?", 1), ("rec", "You're not going to believe this, but my name is Tango also.", 1),
              ("rec", "Looking around this room I'd say pretty high.", 1)],
          1: [("send", "Hi, you look familiar", 0), ("send", "I am from Montana, where are you from?", 0),
              ("send", "Me too, I am from the room we are in currently in Bozeman, Montana", 0), ("send", "Tango", 0),
              ("send", "What are the odds. Two robots run into to each other from the same state,and the same town, and the same room, with the same name?", 0)]}

def receive_token():
    global token
    token = int.from_bytes(s.recv(3), 'big')    

def send_token(token):
    s.send(token.to_bytes(3, 'big'))

def execute_script(scriptid, script):
    global token
    if scriptid in script:
        actions = script[scriptid]
        if actions:
            action, data, dest = actions[0]
            if token == 111:
                #never receiving token 111
                token = 110
                print("Client: ", data)
                send_token(110)
                actions.pop(0)
            elif token == 110:
                print("Server: ", data)
                token = 111
                send_token(111)
                actions.pop(0)

# Define a loop to run the program
while True:
    #disconnect on start of second loop
    execute_script(0, script)
    if len(script[1]) == 0:
        time.sleep(5)
        break
    time.sleep(1)
    receive_token()
    execute_script(1, script)
    time.sleep(1)
    receive_token()
# Close the connection with the client
s.close()

