import socket
import select
import sys
from smbus import SMBus
import time

address = 0x28
CAP1188_SENINPUTSTATUS = 0x3
CAP1188_SENLEDSTATUS = 0x4
CAP1188_MTBLK = 0x2A
CAP1188_PRODID = 0xFD
CAP1188_MANUID = 0xFE
CAP1188_STANDBYCFG = 0x41
CAP1188_REV = 0xFF
CAP1188_MAIN = 0x00
CAP1188_MAIN_INT = 0x01
CAP1188_LEDPOL = 0x73
CAP1188_INTENABLE = 0x27
CAP1188_REPRATE = 0x28
CAP1188_LEDLINK = 0x72

CAP1188_SENSITIVITY = 0x1f
CAP1188_CALIBRATE = 0x26

b = SMBus(1)
b.write_byte_data(address, CAP1188_MTBLK, 0)
b.write_byte_data(address, CAP1188_STANDBYCFG, 0x30)
b.write_byte_data(address, CAP1188_INTENABLE, 0x05)
b.write_byte_data(address, CAP1188_LEDLINK, 0xff)

b.write_byte_data(address, CAP1188_SENSITIVITY, 0x2f)
b.write_byte_data(address, CAP1188_CALIBRATE, 0xff)

def on_new_client(clientsocket,addr):
       while True:
           msg = clientsocket.recv(1024)
           #do some checks and if msg == someWeirdSignal: break:
           print addr, ' >> ', msg
           msg = raw_input('SERVER >> ')
           #Maybe some code to compute the last digit of PI, play game or anything else can go here and $
           clientsocket.send(msg)
       clientsocket.close()


#create a socket
host = '10.50.0.98' #ip of raspberry pi
port = 12345
backlog = 25
maxsize = 64

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (host, port)
print >>sys.stderr, 'starting up on %s port %s' % server_address

# Bind Socket to Port
server.bind((host, port))
server.listen(backlog)
input = [server,] #a list of all connections we want to check for data 
                  #each time we call select.select()

running = 1 #set running to zero to close the server
while running:
  inputready,outputready,exceptready = select.select(input,[],[])

  for s in inputready: #check each socket that select() said has available data

    if s == server: #if select returns our server socket, there is a new 
                    #remote socket trying to connect
      client, addr = server.accept()
      input.append(client) #add it to the socket list so we can check it now
      print ('Got connection from',addr)

      while True:
        t1 = b.read_byte_data(address, CAP1188_SENINPUTSTATUS)
        b1 = '{0:08b}'.format(t1)
        b2 = list(b1)
#    print(b2)
        time.sleep(0.1)
        client.send(str(b2))
        b.write_byte_data(address, CAP1188_MAIN, 0)
