import socket
def GetFromServer (port):
    # create new tcp socket by socket module
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to the local host
    server_socket.bind(('localhost', port))
    #  socket to listen for incoming connection
    server_socket.listen(1)
    print(f"Server listening on port '{port}' ")

    while True:
        # wait for a client to connect to the server
        conn, address = server_socket.accept()
        print(f"Connection from {address}")
        # receives data from the client
        data = conn.recv(1024).decode()
        # check if any data was received from the client
        if not data:
            break
        print(f"Received data: {data}")
        modified_data = change_vowels(data)
        # sends the modified data back to the client
        conn.send(modified_data.encode())
        print(f"Sent modified data: {modified_data}")
        conn.close()

# function to change the vowels to (#)
def change_vowels(data):
    vowels = 'AaEeIiOoUu'
    return ''.join('#' if char in vowels else char for char in data)

if __name__ == "__main__":
    GetFromServer (1115)
