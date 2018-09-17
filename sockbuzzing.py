import time
import socket
import sys
import RPi.GPIO as GPIO
from ast import literal_eval
import ast


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

buzzlist = ['31', '29', '23', '21', '19', '15', '13', '11']

s = socket.socket()
host = '10.50.0.98'# ip of raspberry pi 
port = 12345
s.connect((host, port))

while True:
  phrase = (s.recv(40, socket.MSG_WAITALL))
  b2 = literal_eval(phrase)
  for i in range(0, 8):
   if b2[i] == '1':
    GPIO.output(int(buzzlist[i]), True)
#    print (b2)
    print buzzlist[i] + "buzzing!"
    time.sleep(0.05)
   else:
    GPIO.output(int(buzzlist[i]), False)
    time.sleep(0.05)


"""
#start eval to turn into list
  tree = ast.parse(phrase, mode='eval')
  class Transformer(ast.NodeTransformer):
    ALLOWED_NAMES = set(['List'])
    ALLOWED_NODE_TYPES = set(['Tuple', 'list','String', 'Num'])

  def visit_Name(self, node):
        if not node.id in self.ALLOWED_NAMES:
            raise RuntimeError("Name access to %s is not allowed" % node.id)

        # traverse to child nodes
        return self.generic_visit(node)

  def generic_visit(self, node):
        nodetype = type(node).__name__
        if nodetype not in self.ALLOWED_NODE_TYPES:
            raise RuntimeError("Invalid expression: %s not allowed" % nodetype)

        return ast.NodeTransformer.generic_visit(self, node)

  transformer = Transformer()

  # raises RuntimeError on invalid code
  transformer.visit(tree)
  # compile the ast into a code object
  clause = compile(tree, '<AST>', 'eval')
  # make the globals contain only the Decimal class,
  # and eval the compiled object
  result = eval(phrase)

#  print(result)
#  print(type(result))
"""
