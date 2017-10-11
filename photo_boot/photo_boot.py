#!/usr/bin/env python
import shutil
import os.path
from time import sleep
import RPi.GPIO as GPIO
from time import gmtime, strftime
from threading import Thread

# CONSTANTS
TWEET_LIGHT = 16
PIC_LIGHT = 18
TWEET_PIC = 11
TAKE_PIC = 13
RESET = 15
OFF = False
ON = True
#Paths
FILE_PATH_PI = r'/home/pi/fotos/'
FILE_PATH_USB = r'/home/pi/usbdrv/fotos/'
# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# Buttons
GPIO.setup(TAKE_PIC, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Take picture and save it locally
GPIO.setup(TWEET_PIC, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Take picture and upload it
GPIO.setup(RESET, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Reset
# Leds
GPIO.setup(TWEET_LIGHT, GPIO.OUT) # Ready
GPIO.setup(PIC_LIGHT, GPIO.OUT) # Pose
GPIO.output(TWEET_LIGHT, OFF) # Tweet light off 
GPIO.output(PIC_LIGHT, OFF) # Picture light off

# Twitter keys
#CONSUMER_KEY = ''
#CONSUMER_SECRET = ''
#ACCESS_KEY = ''
#ACCESS_SECRET = ''

# Facebook keys
ACCESS_TOKEN =''
	
###############################################################################
## GPIO
###############################################################################
def push_buttons():
	try:
        	while True:
                	if(GPIO.input(TAKE_PIC) == 1):
				GPIO.wait_for_edge(TAKE_PIC, GPIO.FALLING)
				take_picture(False, PIC_LIGHT)
			if(GPIO.input(TWEET_PIC) == 1):
                                GPIO.wait_for_edge(TWEET_PIC, GPIO.FALLING)
                                take_picture(True, TWEET_LIGHT)
                	if(GPIO.input(RESET) == 1):
                        	print "Pushed reset"
                        	GPIO.cleanup()
                        	break
                	sleep(0.1)
		print "Exit main loop"
	finally:
		GPIO.cleanup()

###############################################################################
## Gphoto2
###############################################################################
def take_picture(share, light):
	print "Start taking picture"
	GPIO.output(light, ON)
	sleep(0.3)
	GPIO.output(light, OFF)
	sleep(0.3)
        GPIO.output(light, ON)
        sleep(0.3)
        GPIO.output(light, OFF)
        sleep(0.3)
        GPIO.output(light, ON)
	#get file path
	sys_path = get_file_storage(False)
	usb_path = get_file_storage(True)
	file_name = get_file_name()
	#take photo
	os.system("gphoto2 --capture-image-and-download --filename " + sys_path + file_name)
        GPIO.output(light, OFF)
	
        if sys_path != usb_path:
                print "Moving file"
                shutil.copy(sys_path + file_name, usb_path)
                os.remove(sys_path + file_name)

	if(share):
		print "Sharing"
		#tweet the photo
		thread = Thread(target = post_media_facebook, args = ("#sapberry uploading media", usb_path + file_name))
		thread.start()
	print "End take picture"


###############################################################################
## Twitter
###############################################################################
def twitter_autenticate():
        # Authenticate
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        return tweepy.API(auth)

def post_media_tweet(msg, fname):
        x = twitter_autenticate()
        if(os.path.isfile(fname)):
                fn = os.path.abspath(fname)
                print 'Uploading file ' + fn + '...'
		sleep(25)
        else:
                print 'File does not exit'

##############################################################################
## Facebook
##############################################################################

def post_media_facebook(msg, fname):
	facebookClient = FacebookClient('[[EMAIL]]', '[[PASSWORD]]')
	facebookClient.upload_photo(fname)
	print "End sharing photo"



##############################################################################
## File storage
##############################################################################
def get_file_storage(usb):
	file_path = ""
	#check if USB exits
	if (usb and os.path.isdir(FILE_PATH_USB)):
		file_path = FILE_PATH_USB
	else:
		file_path = FILE_PATH_PI
        #check if folder needs to be created
	if(not os.path.isdir(file_path)):
		os.system("mkdir " + file_path)
	#returnn file path
        return file_path


def get_file_name():
	return "photo_" + strftime("%H%M%S", gmtime()) + ".jpg"

##############################################################################
## Call main method
##############################################################################

for i in range(0, 10):
        GPIO.output(PIC_LIGHT, ON)
	GPIO.output(TWEET_LIGHT, ON)
        sleep(0.3)
        GPIO.output(TWEET_LIGHT, OFF)
	GPIO.output(PIC_LIGHT, OFF)
	sleep(0.3)

push_buttons()
