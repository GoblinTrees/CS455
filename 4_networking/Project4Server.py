# Server.py
import socket
import sys
import time

# Define the host and port
host = 'localhost'
port = 5000

global token
token = 110


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))

s.listen(1)

c, addr = s.accept()
print("Connection from:", addr)

id = 0
next = 1

script = {0: [("send", "Hi", 1), ("send", "I was just going to say the same thing about you. Where are you from?", 1), ("send", "Me too. Bozeman, Montana", 1),
              ("send", "Me too, wow that is wild. What is your name?", 1), ("send", "You're not going to believe this, but my name is Tango also.", 1),
              ("send", "Looking around this room I'd say pretty high.", 1)],
          1: [("rec", "Hi, you look familiar", 0), ("rec", "I am from Montana, where are you from?", 0),
              ("rec", "Me too, I am from the room we are in currently in Bozeman, Montana", 0), ("rec", "Tango", 0),
              ("rec", "What are the odds. Two robots run into to each other from the same state,and the same town, and the same room, with the same name?", 0)]}

def receive_token():
    global token
    token = int.from_bytes(c.recv(3), 'big')

def send_token(token):
    c.send(token.to_bytes(3, 'big'))
    
def execute_script(scriptid, script):
    global token
    if scriptid in script:
        actions = script[scriptid]
        if actions:
            action, data, dest = actions[0]
            if token == 110:
                token = 111
                #never receiving token 110
                print("Server: ", data)
                send_token(111)
                #c.send(data.encode())
                actions.pop(0)
            elif token == 111:
                print("Client: ", data)
                token = 110
                send_token(110)
                actions.pop(0)

# Define a loop to run the program
while True:
    execute_script(0, script)
    if len(script[1]) == 0:
        time.sleep(5)
        break
    time.sleep(1)
    receive_token()
    #doesn't receive token during second loop
    execute_script(1, script)
    time.sleep(1)
    receive_token()
# Close the connection with the client
c.close()
