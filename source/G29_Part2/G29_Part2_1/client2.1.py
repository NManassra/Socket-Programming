import socket

def SendDataToserver(data, port):
    # create a new tcp socket using the socket module
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connects the client socket to the server running on the local host
    client_socket.connect(('localhost', port))
    # sends the data to the server
    client_socket.send(data.encode())
    # receives the modified data from the server
    modified_data = client_socket.recv(1024).decode()
    print(f"Received modified data: {modified_data}")
    # closes the connection to the server
    client_socket.close()

if __name__ == "__main__":
    data = input("Enter data to send: ")
    SendDataToserver(data, 1115)
