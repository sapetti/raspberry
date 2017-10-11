#!/usr/bin/env python

import serial
import sys

arduino = serial.Serial('/dev/ttyACM0', 9600)

print("Start py")
# Get the total number of args passed to the demo.py
total = len(sys.argv)
print("2")
# Get the arguments list 
cmdargs = str(sys.argv)
 
# Print it
print("The total numbers of args passed to the script: %d " % total)
print("Args list: %s " % cmdargs)





#print("'' received!")

#arduino.write(comando) #Mandar un comando hacia Arduino
#arduino.close() #Finalizamos la comunicacion


