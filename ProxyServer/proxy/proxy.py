# Include Python's Socket Library
from socket import *
from datetime import datetime
import time
import os

# Specify Server Port
serverPort = 9001

# Create TCP welcoming socket
serverSocket = socket(AF_INET,SOCK_STREAM)

ipAddress = input("Enter your current device's IPv4 address: ")
if(ipAddress == ""):
    ipAddress = '10.118.38.214'
# Bind the server port to the socket
serverSocket.bind((ipAddress,serverPort))

# Server begins listerning foor incoming TCP connections
serverSocket.listen(1)

print ('--- The PROXY server is ready to receive ---')

try:

    while True: # Loop forever
        # Server waits on accept for incoming requests.
        # New socket created on return
        connectionSocket, addr = serverSocket.accept()

        # Read from socket (but not address as in UDP)
        request = connectionSocket.recv(1024).decode()
        #get headers
        headers = request.split('\n')
        #get file path
        splitHeaders = headers[0].split()
        request_type = splitHeaders[0]
        currentTime = datetime.now()
        dateStr = currentTime.strftime("%c")

        #Varying logic based on request type
        if (request_type == 'GET'):
            try:
                filename = headers[0].split()[1]
                fin = open(filename[1:] + '.html')
                content = fin.read()
                fin.close()
                if ("If-modified-since:" in headers[2]):
                    modTimeEpoch = os.path.getmtime(filename[1:] + '.html')
                    modTime = time.strftime('%Y-%m-%d', time.localtime(modTimeEpoch))
                    fileMod = modTime.split('-')
                    fileDate = datetime(int(fileMod[0]), int(fileMod[1]), int(fileMod[2]))
                    length = str(len(content))
                    date = headers[2].split(':')[1]
                    modifiers = date.split('-')
                    dateObject = datetime(int(modifiers[0]), int(modifiers[1]), int(modifiers[2]))
                    if (fileDate < dateObject):
                        response = f"HTTP/1.1 304 NOT MODIFIED\r\nDate: {dateStr}"
                        print("Response: \n" + response)
                        connectionSocket.sendall(response.encode("utf-8"))
                    
                    else:
                        length = str(len(content))
                        response = f"HTTP/1.1 200 OK\r\nlength: {length}\r\nContent-Type: text/html\r\nDate: {dateStr}\r\n\r\n" + content
                        print("Response: \n" + response)
                        connectionSocket.sendall(response.encode("utf-8"))

                else:
                    length = str(len(content))
                    response = f"HTTP/1.1 200 OK\r\nlength: {length}\r\nContent-Type: text/html\r\nDate: {dateStr}\r\n\r\n" + content
                    print("Response: \n" + response)
                    connectionSocket.sendall(response.encode("utf-8"))
            except FileNotFoundError:
                clientSocket = socket(AF_INET, SOCK_STREAM)

                # Connect to TCP Server Socket
                try:
                    clientSocket.connect((ipAddress, 9000))
                    clientSocket.send(request.encode())
                    result = clientSocket.recv(1024)
                    clientSocket.close()
                    connectionSocket.sendall(result)
                    response = result.decode()
                    originServerHead = response.split('\n')[0]
                    filename = headers[0].split()[1]
                    a = response.split('\n')[5:]
                    b = ''.join(a)
                    file = open(filename[1:] + '.html', "w")
                    file.write(b)
                    file.close()

                except error:
                    errorResponse = f"HTTP/1.1 408 REQUEST TIMED OUT\r\nContent-Type: text/html\r\nDate: {dateStr}"
                    connectionSocket.sendall(errorResponse.encode())
                    print("error")
            
        elif (request_type == 'PUT' or request_type == 'DELETE' or request_type == 'POST'):

            file = open('error.html')
            content = file.read()
            file.close()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nDate: {dateStr}\r\n\r\n" + content
            print("Response: \n" + response)
            connectionSocket.sendall(response.encode("utf-8"))


        elif (request_type == 'HEAD'):
            try:
                filename = headers[0].split()[1]
                file = open(filename[1:] + '.html')
                content = file.read()
                file.close()
                length = str(len(content))
                response = f"HTTP/1.1 200 OK\r\nlength: {length}\r\nContent-Type: text/html\r\nDate: {dateStr}\r\n\r\n"
                print("Response: \n" + response)
                connectionSocket.sendall(response.encode("utf-8"))
            except FileNotFoundError:
                response = f'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\nDate: {dateStr}'
                print("Response: \n" + response)
                connectionSocket.sendall(response.encode("utf-8"))

        else:
            response = f'HTTP/1.1 400 BAD REQUEST\r\nDate: {dateStr}'
            print("Response: \n" + response)
            connectionSocket.sendall(response.encode("utf-8"))

        # Send the reply
        #capitalizedSentence = sentence.upper()
        #connectionSocket.send(msg.encode())
        
        # Close connectiion too client (but not welcoming socket)
        connectionSocket.close()

    
except KeyboardInterrupt:
    print('interrupted!')
    pass
