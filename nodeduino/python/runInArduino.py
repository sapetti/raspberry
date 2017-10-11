#!/usr/bin/env python

import serial
import sys

#arduino = serial.Serial('/dev/ttyACM0', 9600)

print("Start python")
# Get the total number of args passed to the demo.py
#total = len(sys.argv)
# Get the arguments list 
command = str(sys.argv[1])
command = command.strip()
 
# Print it
#print("The total numbers of args passed to the script: %d " % total)
print("Command received: %s" % command)

#print("'' received!")
#arduino.write(comando) #Mandar un comando hacia Arduino

#arduino.close() #Finalizamos la comunicacion


