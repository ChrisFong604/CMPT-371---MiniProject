# Include Python's Socket Library
from socket import *

# Specify Server Address
serverName = '10.118.38.214'
serverPort = 9000

# Create TCP Socket for Client
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to TCP Server Socket
clientSocket.connect((serverName,serverPort))
clientSocket.send("GET /test HTTP/1.1\nHost: 10.118.38.214\nIf-modified-since:2022-12-12".encode())

# Read reply characters! No need to read address! Why?
modifiedSentence = clientSocket.recv(1024)

# Print out the received string
print ('From Server:', modifiedSentence.decode())
input("hahahaha")

# Close the socket
clientSocket.close()