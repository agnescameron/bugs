import time
import socket
import sys
import RPi.GPIO as GPIO
from ast import literal_eval
import zmq

GPIO.setmode(GPIO.BOARD)

#pin 11 is motor.1
GPIO.setup(11, GPIO.OUT)
GPIO.output(11,False)
#pin 13 is motor.2
GPIO.setup(13, GPIO.OUT)
GPIO.output(13,False)
#pin 15 is motor.3
GPIO.setup(15, GPIO.OUT)
GPIO.output(15,False)
#pin 19 is motor.4
GPIO.setup(19, GPIO.OUT)
GPIO.output(19,False)
#pin 21 is motor.5
GPIO.setup(21, GPIO.OUT)
GPIO.output(21,False)
#pin 23 null
GPIO.setup(23, GPIO.OUT)
GPIO.output(23,False)
#pin 29 is null
GPIO.setup(29, GPIO.OUT)
GPIO.output(29,False)
#pin 31 is null
GPIO.setup(31, GPIO.OUT)
GPIO.output(31, False)

buzzlist = ['31', '29', '23', '21', '19', '15', '13', '11']

port = "12345"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

#if len(sys.argv) > 2:
#    port1 =  sys.argv[2]
#    int(port1)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://10.50.0.52:12345")
if len(sys.argv) > 2:
  socket.connect("tcp://10.50.0.52:12345")

topicfilter = ""
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

while True:
  phrase = socket.recv()
  print phrase
  b2 = literal_eval(phrase)
  for i in range(0, 8):
    if b2[i] == '1':
      GPIO.output(int(buzzlist[i]), True)
      print (b2)
      time.sleep(0.01)
    else:
      GPIO.output(int(buzzlist[i]), False)
      time.sleep(0.01)


