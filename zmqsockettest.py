import time
import socket
import sys

server = socket.socket()
host = '10.50.0.52'# ip of raspberry pi 
port = 12345
server.connect((host, port))

while True:
  phrase = (server.recv(40, socket.MSG_WAITALL))
  print (phrase)
