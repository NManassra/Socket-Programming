import os
from socket import *

# reserve port on the computer
serverPort = 1115
# create socket by IPv4  and TCP
serverSocket = socket(AF_INET, SOCK_STREAM)
# conecte the socket with local address, allow clients to connect to  server by that address
serverSocket.bind(("", serverPort))
# set the socket to listening mode, allowing one connection at a time
serverSocket.listen(1)
print("The Server is Ready!")

# infinite loop to continuously accept and handle incoming connections
while True:
    # accept incoming connection requests
    connectionSocket, address = serverSocket.accept()
    # Receive data from the client
    sentence = connectionSocket.recv(1024).decode()
    print(address)
    print(sentence)
    ip = address[0]
    port = address[1]
    words = sentence.split()

    if len(words) >= 2:
        request = words[1]
        request = request.lower()
        request = request.lstrip('/')
        # Handling various types of HTTP requests

        # Handling requests for specific HTML files
        if request == "" or request == "index.html" or request == "en" or request == "main_en.html":
            # Read and send the requested HTML file
            current_directory = os.path.dirname(os.path.abspath(__file__))
            requestedFile = open(os.path.join(current_directory, "main_en.html"))
            webPage = requestedFile.read()
            requestedFile.close()
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: text/html \r\n".encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.send(webPage.encode())

        # Handling requests for an Arabic HTML file
        elif request == 'ar' or request == 'main_ar.html':
            # Read and send the requested Arabic HTML file
            current_directory = os.path.dirname(os.path.abspath(__file__))
            requestedFile = open(os.path.join(current_directory, "main_ar.html"), encoding="utf-8")
            webPage = requestedFile.read()
            requestedFile.close()
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.send(webPage.encode('utf-8'))

        # Handling requests for CSS files
        elif request.endswith(".css"):
            # Read and send the requested CSS file
            current_directory = os.path.dirname(os.path.abspath(__file__))
            requestedFile = open(os.path.join(current_directory, request))
            webPage = requestedFile.read()
            requestedFile.close()
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: text/css \r\n".encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.send(webPage.encode())

        # Handling requests for other HTML files
        elif request.endswith(".html"):
            try:
                current_directory = os.path.dirname(os.path.abspath(__file__))
                requestedFile = open(os.path.join(current_directory, request), encoding="utf-8")
                webPage = requestedFile.read()
                requestedFile.close()
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Content-Type: text/html\r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.send(webPage.encode())
            except FileNotFoundError:
                connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
                connectionSocket.send("Content-Type: text/html\r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.send("""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Error 404</title>
                </head>
                <body style="color: blue;">
                    <h1>HTTP/1.1 404 Not Found</h1>
                    <p>The file is not found</p>
                    <b>Group Members: Your Names and IDs</b>
                    <p>Client IP: {}</p>
                    <p>Client Port: {}</p>
                </body>
                </html>
                """.format(ip, port).encode('utf-8'))

        # Handling requests for JPG images
        elif request.endswith(".jpg"):
            current_directory = os.path.dirname(os.path.abspath(__file__))
            try:
                requestedFile = open(os.path.join(current_directory, request), "rb")
                webPage = requestedFile.read()
                requestedFile.close()
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Content-Type: image/jpeg \r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.send(webPage)
            except FileNotFoundError:
                connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
                connectionSocket.send("Content-Type: text/html\r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.send("""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Error 404</title>
                </head>
                <body style="color: blue;">
                    <h1>HTTP/1.1 404 Not Found</h1>
                    <p>The file is not found</p>
                    <b>Group Members: Your Names and IDs</b>
                    <p>Client IP: {}</p>
                    <p>Client Port: {}</p>
                </body>
                </html>
                """.format(ip, port).encode('utf-8'))

        # Handling requests for PNG images
        elif request.endswith(".png"):
            current_directory = os.path.dirname(os.path.abspath(__file__))
            try:
                requestedFile = open(os.path.join(current_directory, request), "rb")
                webPage = requestedFile.read()
                requestedFile.close()
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Content-Type: image/png \r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.send(webPage)
            except FileNotFoundError:
                connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
                connectionSocket.send("Content-Type: text/html\r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.send("""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Error 404</title>
                </head>
                <body style="color: blue;">
                    <h1>HTTP/1.1 404 Not Found</h1>
                    <p>The file is not found</p>
                    <b>Group Members: Your Names and IDs</b>
                    <p>Client IP: {}</p>
                    <p>Client Port: {}</p>
                </body>
                </html>
                """.format(ip, port).encode('utf-8'))

        # Handling specific redirection requests
        elif request == "so":
            connectionSocket.send("HTTP/1.1 307 Temporary Redirect \r\n".encode())
            connectionSocket.send("Location: https://www.stackoverflow.com\r\n".encode())
            connectionSocket.send("\r\n".encode())
        elif request == "itc":
            connectionSocket.send("HTTP/1.1 307 Temporary Redirect \r\n".encode())
            connectionSocket.send("Location: https://itc.birzeit.edu\r\n".encode())
            connectionSocket.send("\r\n".encode())

        else:
            # Respond with a 404 Not Found error along with additional information
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
            connectionSocket.send("Content-Type: text/html \r\n".encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.send("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Error 404</title>
            </head>
            <body style="color: blue;">
                <h1>HTTP/1.1 404 Not Found</h1>
                <p>The file is not found</p>
                <b>Group Members: Your Names and IDs</b>
                <p>Client IP: {}</p>
                <p>Client Port: {}</p>
            </body>
            </html>
            """.format(ip, port).encode('utf-8'))

    # Close the connection
    connectionSocket.close()
