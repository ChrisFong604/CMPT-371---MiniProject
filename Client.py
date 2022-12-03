# Include Python's Socket Library
import socket
import sys

# Checking arguments
if len(sys.argv) < 2:
    print("Required arguments missing!")
    print("Usage: receiver <hostname> <port>")
    sys.exit(1)

#capture hostname and port
serverName = sys.argv[1]
serverPort = int(sys.argv[2])

# Create TCP Socket for Client
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to TCP Server Socket
clientSocket.connect((serverName,serverPort))

# Recieve user input from keyboard
string = input('Input string:')

# Send! 
clientSocket.send(string.encode())

# Read reply characters!
buffer = clientSocket.recv(1024)

# Print out the received string
print ('From Server:', buffer.decode())

# Close the socket
clientSocket.close()