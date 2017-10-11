#!/usr/bin/env python
import shutil
import os.path
from time import sleep
import RPi.GPIO as GPIO
#from time import gmtime, strftime

# CONSTANTS
TMP = 16
USB_LIGHT = 18
OFF = True
ON = False
# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(USB_LIGHT, GPIO.OUT) # Setup pin as output for the usb light as output
GPIO.setup(TMP, GPIO.OUT)

#import RPI.GPIO as GPIO
#import time
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(USB_LIGHT, GPIO.OUT)
GPIO.output(USB_LIGHT, False)
GPIO.output(TMP, False)
sleep(10)
GPIO.cleanup()
