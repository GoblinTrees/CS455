import socket
import random
import time

msg = [
    "Hi, you look familiar.",
    "I am from Montana, where are you from?",
    "Me too, I am from the room we are in currently in Bozeman, Montana.",
    "Tango.",
    "What are the odds. Two robots run into to each other from the same state, and the same town, and the same room, with the same name?",
]


def random_delay():
    return random.uniform(1, 3)

def client():
    host = '192.168.88.20'  # Replace with the Raspberry Pi's IP address
    port = 12345

    # Create a socket object
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    conn.connect((host, port))

    # Exchange messages
    exchange_messages(conn)

    # Close the connection
    conn.close()


def exchange_messages(conn):
    for x in range(len(msg)):
        # Wait for token from server
        token = conn.recv(1024)

        #print message
        print(msg[x])
        time.sleep(random_delay())  # Small delay
        # Send message to server
        conn.send(token)
        # print("Client sent token")


if __name__ == "__main__":
    client()
