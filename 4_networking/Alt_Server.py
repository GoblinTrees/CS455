import socket
import random
import time

def random_delay():
    return random.uniform(0.5, 4)

delay = random_delay()

def server():
    host = '0.0.0.0'  # Listen on all network interfaces
    port = 12345

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print("Server listening...")

    # Accept a connection
    conn, addr = server_socket.accept()
    print("Connection from:", addr)

    # Exchange messages
    exchange_messages(conn)

    # Close the connection
    conn.close()

def exchange_messages(conn):
    messages = [
        "Hi.",
        "I was just going to say the same thing about you. Where are you from?",
        "Me too. Bozeman, Montana",
        "Me too, I am from the room we are in currently in Bozeman, Montana.",
        "Me too, wow that is wild. What is your name?",
        "Your not going to believe this, but my name is Tango also.",
        "Looking around this room I'd say pretty high."
    ]

    for msg in messages:
        conn.send(msg.encode())
        data = conn.recv(1024).decode()
        time.sleep(delay)
        print("Server_received: ", data)

if __name__ == "__main__":
    server()
