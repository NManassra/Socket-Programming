import os
from socket import *

serverPort = 1115
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
print("The Server is done, you can go ahead now!")

# Read Error404.html template
current_error_directory = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_error_directory, "Error404.html"), 'r', encoding="utf-8") as file:
    error_template = file.read()

while True:
    connectionSocket, address = serverSocket.accept()
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

        # Function to send a 404 Not Found response
        def send_404():
            error_page = error_template.format(ip, port)
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
            connectionSocket.send("Content-Type: text/html\r\n".encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.send(error_page.encode())

        # Handling requests for specific HTML files
        if request == "" or request == "index.html" or request == "en" or request == "main_en.html":
            # Read and send the requested HTML file
            current_directory = os.path.dirname(os.path.abspath(__file__))
            try:
                requestedFile = open(os.path.join(current_directory, "main_en.html"))
                webPage = requestedFile.read()
                requestedFile.close()
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Content-Type: text/html \r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.send(webPage.encode())
            except FileNotFoundError:
                send_404()

        # Handling requests for an Arabic HTML file
        elif request == 'ar' or request == 'main_ar.html':
            # Read and send the requested Arabic HTML file
            current_directory = os.path.dirname(os.path.abspath(__file__))
            try:
                requestedFile = open(os.path.join(current_directory, "main_ar.html"), encoding="utf-8")
                webPage = requestedFile.read()
                requestedFile.close()
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.send(webPage.encode('utf-8'))
            except FileNotFoundError:
                send_404()

        # Handling requests for CSS files
        elif request.endswith(".css"):
            css_path = os.path.join("additions/css", request.split('/')[-1])
            current_directory = os.path.dirname(os.path.abspath(__file__))
            try:
                requestedFile = open(os.path.join(current_directory, css_path))
                webPage = requestedFile.read()
                requestedFile.close()
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Content-Type: text/css \r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.send(webPage.encode())
            except FileNotFoundError:
                send_404()

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
                send_404()

        # Handling requests for JPG images
        elif request.endswith(".jpg"):
            # Ensure the request points to the additions/img/ directory
            img_path = os.path.join("additions/img", request.split('/')[-1])
            current_directory = os.path.dirname(os.path.abspath(__file__))
            try:
                requestedFile = open(os.path.join(current_directory, img_path), "rb")
                webPage = requestedFile.read()
                requestedFile.close()
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Content-Type: image/jpeg \r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.send(webPage)
            except FileNotFoundError:
                send_404()

        # Handling requests for PNG images
        elif request.endswith(".png"):
            # Ensure the request points to the additions/img/ directory
            img_path = os.path.join("additions/img", request.split('/')[-1])
            current_directory = os.path.dirname(os.path.abspath(__file__))
            try:
                requestedFile = open(os.path.join(current_directory, img_path), "rb")
                webPage = requestedFile.read()
                requestedFile.close()
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Content-Type: image/png \r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.send(webPage)
            except FileNotFoundError:
                send_404()

        # Handling specific redirection requests
        elif request == "so":
            connectionSocket.send("HTTP/1.1 307 Temporary Redirect \r\n".encode())
            connectionSocket.send("Location: https://www.stackoverflow.com\r\n".encode())
            connectionSocket.send("\r\n".encode())
        elif request == "itc":
            connectionSocket.send("HTTP/1.1 307 Temporary Redirect \r\n".encode())
            connectionSocket.send("Location: https://itc.birzeit.edu\r\n".encode())
            connectionSocket.send("\r\n".encode())

        # Handling the get_image request
        elif request.startswith("additions/img/") and (request.endswith(".jpg") or request.endswith(".png")):
            current_directory = os.path.dirname(os.path.abspath(__file__))
            try:
                requestedFile = open(os.path.join(current_directory, request), "rb")
                webPage = requestedFile.read()
                requestedFile.close()
                if request.endswith(".jpg"):
                    content_type = "image/jpeg"
                elif request.endswith(".png"):
                    content_type = "image/png"
                else:
                    raise FileNotFoundError
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send(f"Content-Type: {content_type} \r\n".encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.send(webPage)
            except FileNotFoundError:
                send_404()

        else:
            send_404()

    # Close the connection
    connectionSocket.close()
