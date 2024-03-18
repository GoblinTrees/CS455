import socket
import random
import time

def random_delay():
    return random.uniform(0.5, 4)

delay = random_delay()

def client():
    host = '192.168.88.20'  # Replace with the Raspberry Pi's IP address
    port = 12345

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))

    # Wait for the initial message from the server
    initial_message = client_socket.recv(1024).decode()
    print("Received:", initial_message)
    time.sleep(delay)

    # Define messages to send
    messages = [
        "Hi, you look familiar.",
        "I was just going to say the same thing about you. Where are you from?",
        "I am from Montana, where are you from?",
        "Me too. Bozeman, Montana",
        "Me too, I am from the room we are in currently in Bozeman, Montana.",
        "Tango.",
        "Your not going to believe this, but my name is Tango also.",
        "What are the odds. Two robots run into to each other from the same state, and the same town, and the same room, with the same name?",
        "Looking around this room I'd say pretty high."
    ]

    # Exchange messages
    exchange_messages(client_socket, messages)

    # Close the connection
    client_socket.close()

def exchange_messages(client_socket, messages):
    for msg in messages:
        # Send message to server
        client_socket.send(msg.encode())
        print("Sent:", msg)
        time.sleep(delay)

        # Receive response from server
        data = client_socket.recv(1024).decode()
        print("Received:", data)
        time.sleep(delay)

if __name__ == "__main__":
    client()
