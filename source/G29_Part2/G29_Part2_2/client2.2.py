# Contributor B STUDENT_B , Contributor A STUDENT_A
import socket

def start_client():
    # define server address and port
    SERVER_ADDRESS = 'localhost'
    PORT = 2359  # Should match the server port

    # create a upd socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        # get user input
        message = input("Enter your message: ")

        # send message to the server
        client_socket.sendto(message.encode(), (SERVER_ADDRESS, PORT))

        # receive acknowledgement from the server
        ack, server = client_socket.recvfrom(1024)
        print(f"Server says: {ack.decode()}")

if __name__ == "__main__":
    start_client()
