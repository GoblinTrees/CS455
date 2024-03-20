import socket
import random
import time

token = b"your turn"

msg = [
        "Hi.",
        "I was just going to say the same thing about you. Where are you from?",
        "Me too. Bozeman, Montana",
        "Me too, wow that is wild. What is your name?",
        "Your not going to believe this, but my name is Tango also.",
        "Looking around this room I'd say pretty high."
    ]
def random_delay() -> int:
    return random.uniform(1, 3)

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

    for x in range(len(msg)):
        # print line
        print(msg[x])
        # time.sleep(random_delay())
        # send data
        conn.send(token)
        time.sleep(random_delay())  # Small delay
        # wait till token returned
        data = conn.recv(1024)
        # print("Server received token:", data)



        # receive data, say the next line
        continue


if __name__ == "__main__":
    server()
    # time.sleep(random_delay())  # Small delay