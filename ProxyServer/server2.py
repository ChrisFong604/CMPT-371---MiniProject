# Include Python's Socket Library
from socket import *
from datetime import datetime
import time
import os
import threading

#initialize threads
threads = []
# Specify Server Port
serverPort = 8080
# Create TCP welcoming socket
serverSocket = socket(AF_INET,SOCK_STREAM)
# Bind the server port to the socket
serverSocket.bind(('10.0.0.62',serverPort))
# Server begins listerning foor incoming TCP connections
serverSocket.listen(1)
print ('--- The server is ready to receive ---')

def newTCPServerThread(connectionSocket): 
    #Varying logic based on request type

    # Read from socket (but not address as in UDP)
    request = connectionSocket.recv(1024).decode()
    #get headers
    headers = request.split('\n')
    #get file path
    request_type = headers[0].split()[0]
    print("request type: " + request_type)
    currentTime = datetime.now()
    dateStr = currentTime.strftime("%c")

    if (request_type == 'GET'):
        try:
            filename = headers[0].split()[1]
            fin = open(filename[1:] + '.html')
            content = fin.read()
            fin.close()
            print(headers)
            print(len(headers))
            if ("If-modified-since:" in headers[2]):
                modTimeEpoch = os.path.getmtime(filename[1:] + '.html')
                modTime = time.strftime('%Y-%m-%d', time.localtime(modTimeEpoch))
                fileMod = modTime.split('-')
                fileDate = datetime(int(fileMod[0]), int(fileMod[1]), int(fileMod[2]))
                print(fileDate)
                print(modTime)
                length = str(len(content))
                givenDate = headers[2].split(':')[1]
                givenMod = givenDate.split('-')
                givenDateObj = datetime(int(givenMod[0]), int(givenMod[1]), int(givenMod[2]))
                print(headers)
                print(givenDate)
                if (fileDate < givenDateObj):
                    response = f"HTTP/1.1 304 NOT MODIFIED\r\nDate: {dateStr}"
                    connectionSocket.sendall(response.encode("utf-8"))
                
                else:
                    length = str(len(content))
                    response = f"HTTP/1.1 200 OK\r\nlength: {length}\r\nContent-Type: text/html\r\nDate: {dateStr}\r\n\r\n" + content
                    connectionSocket.sendall(response.encode("utf-8"))

            else:
                length = str(len(content))
                response = f"HTTP/1.1 200 OK\r\nlength: {length}\r\nContent-Type: text/html\r\nDate: {dateStr}\r\n\r\n" + content
                connectionSocket.sendall(response.encode("utf-8"))
        except FileNotFoundError:
            response = f'HTTP/1.0 404 NOT FOUND\r\nContent-Type: text/html\r\nDate: {dateStr}'
            connectionSocket.sendall(response.encode("utf-8"))
        


    elif (request_type == 'HEAD'):
        try:
            filename = headers[0].split()[1]
            file = open(filename[1:] + '.html')
            content = file.read()
            file.close()
            
            length = str(len(content))

            response = f"HTTP/1.1 200 OK\r\nlength: {length}\r\nContent-Type: text/html\r\nDate: {dateStr}\r\n\r\n"
            connectionSocket.sendall(response.encode("utf-8"))
        except FileNotFoundError:
            response = f'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\nDate: {dateStr}'
            connectionSocket.sendall(response.encode("utf-8"))

    elif (request_type == 'PUT' or request_type == 'DELETE' or request_type == 'POST'):

        file = open('error.html')
        content = file.read()
        file.close()
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nDate: {dateStr}\r\n\r\n" + content
        connectionSocket.sendall(response.encode("utf-8"))

    else:
        response = f'HTTP/1.1 400 BAD REQUEST\r\nDate: {dateStr}'
        connectionSocket.sendall(response.encode("utf-8"))

    # Send the reply
    #capitalizedSentence = sentence.upper()
    #connectionSocket.send(msg.encode())
    
    # Close connectiion too client (but not welcoming socket)
    connectionSocket.close()

try:
    while True: # Loop forever
        # Server waits on accept for incoming requests.
        # New socket created on return
        connectionSocket, addr = serverSocket.accept()
        newServerThread = threading.Thread(target=newTCPServerThread, args=[serverSocket])
        newServerThread.start()
        threads.append(newServerThread)

    
except KeyboardInterrupt:
    print('interrupted!')
    pass
