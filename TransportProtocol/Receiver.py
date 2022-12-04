# Include Python's Socket Library, and flow control helper libraries
import sys
import socket
import select
import json
import time
import matplotlib.pyplot as plt
import CongestionControl



# Checking arguments
if len(sys.argv) < 2:
    print("Required arguments missing!")
    print("Usage: sender <hostname> <port>")
    sys.exit(1)

#Initialize congestion control object
CControl = CongestionControl.CongestionStrategy(100, 1)

#capture hostname and port
serverName = sys.argv[1]
serverPort = int(sys.argv[2])

# Create TCP welcoming socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server port to the socket
serverSocket.bind(('',serverPort))

# Server begins listerning foor incoming TCP connections
serverSocket.listen(1)
print ('The server is ready to receive')

while True: # Loop forever
    # Server waits on accept for incoming requests.
    # New socket created on return
    connectionSocket, addr = serverSocket.accept() 
    print(f"Connection Estabished - {addr[0]}:{addr[1]}")
    
    # Read from socket
    string = connectionSocket.recv(1024).decode()
    CongestionControl.CongestionStrategy.
    cc.process_ack
    print(string)
    
    # Send the reply
    capitalizedString = string.upper()
    connectionSocket.send(capitalizedString.encode())
    
    # Close connection too client (but not welcoming socket)
    connectionSocket.close()