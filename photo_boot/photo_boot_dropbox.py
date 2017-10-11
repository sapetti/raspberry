#!/usr/bin/env python
import shutil
import os.path
from time import sleep
import RPi.GPIO as GPIO
from time import gmtime, strftime
from threading import Thread
#Facebook
#from facepy import GraphAPI
#from facebook_client import FacebookClient
#Twitter
#import tweepy
#Dropbox
import dropbox
#import datetime

# CONSTANTS
UPLOAD_LIGHT = 16
USB_LIGHT = 18
UPLOAD_PIC = 11
USB_PIC = 13
RESET = 15
OFF = True
ON = False
#PATHS
FILE_PATH_PI = r'/home/pi/fotos/'
FILE_PATH_USB = r'/home/pi/fotos/'
# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# Buttons
GPIO.setup(USB_PIC, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Setup pin as input to take picture and save it locally
GPIO.setup(UPLOAD_PIC, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Setup pin as input to take picture and upload it
GPIO.setup(RESET, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # Setup pin as input to shutdown the system
# Leds
GPIO.setup(UPLOAD_LIGHT, GPIO.OUT) # Setup pin as output for the upload light as output
GPIO.setup(USB_LIGHT, GPIO.OUT) # Setup pin as output for the usb light as output
GPIO.output(UPLOAD_LIGHT, OFF) # Turn off upload light
GPIO.output(USB_LIGHT, OFF) # Turn off usb light

# Media access token key
# ACCESS_TOKEN = ''

###############################################################################
## GPIO HANDLE CODE
###############################################################################
def push_buttons():
	try:
        	while True:
			if(GPIO.input(USB_PIC) == 1):
				GPIO.wait_for_edge(USB_PIC, GPIO.FALLING)
				take_photo(False, USB_LIGHT)
			if(GPIO.input(UPLOAD_PIC) == 1):
                		GPIO.wait_for_edge(UPLOAD_PIC, GPIO.FALLING)
				take_photo(False, UPLOAD_LIGHT)
	                if(GPIO.input(RESET) == 1):
        	               	print "Pushed reset"
                	       	GPIO.cleanup()
                       		break
                sleep(0.1)
		print "Exit main loop"
	except:
		print "Error in push_buttons"
	finally:
		GPIO.cleanup()

###############################################################################
## Gphoto2
###############################################################################
def take_photo(share, light):
	print "Start taking picture"
	try:
		#pose time
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
		file_name = get_file_name(share)
		#take photo
		os.system("gphoto2 --capture-image-and-download --filename " + sys_path + file_name)
		
		if sys_path != usb_path:
				print "Moving file"
				shutil.copy(sys_path + file_name, usb_path)
				os.remove(sys_path + file_name)

		if(share):
			print "Sharing"
			thread = Thread(target = upload_to_dropbox, args = (usb_path, file_name))
			thread.start()
	except:
		print "Error in take_photo"
	finally:
		print "Clean lights"
		GPIO.output(light, OFF)
	print "End take picture"


###############################################################################
## Twitter
###############################################################################
def twitter_autenticate():
        # Authenticate
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        return tweepy.API(auth)

def upload_to_twitter(msg, fname):
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

def upload_to_facebook(msg, fname):
	facebookClient = FacebookClient('[[EMAIL]]', '[[PASSWORD]]')
	facebookClient.upload_photo(fname)
	print "End sharing photo in Facebook"

##############################################################################
## Dropbox
##############################################################################

def upload_to_dropbox(path, fname):
	uploaded = False
	count = 0
	print 'Fname ' + fname
	while(uploaded == False and count < 3):
		try:
			print 'Uploading ' + fname + ' Try ' + str(count) 
			#time = datetime.datetime.now().time()
			client = dropbox.client.DropboxClient('[[API_KEY]]')
			f = open(path+fname, 'rb')
			response = client.put_file('/'+fname, f)
			#print response
			if(response):
				uploaded = True
		except Exception as e:
			print "Error in upload_to_dropbox:: " + str(e)
		count+=1
	if uploaded == False:
		f = open(FILE_PATH_PI + '../failed.txt','a')
		f.write(fname+'\n') # python will convert \n to os.linesep
		f.close() # you can omit in most cases as the destructor will call it
	print "End sharing photo in Dropbox"

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
	return file_path


def get_file_name(share):
	name = "photo"
	if(share):
		name = name + '_dpbx_'
	return name + strftime("%H%M%S", gmtime()) + ".jpg"

##############################################################################
## Call main method
##############################################################################

for i in range(0, 10):
        GPIO.output(USB_LIGHT, ON)
	GPIO.output(UPLOAD_LIGHT, ON)
        sleep(0.3)
        GPIO.output(UPLOAD_LIGHT, OFF)
	GPIO.output(USB_LIGHT, OFF)
	sleep(0.3)
print "ready!!"
push_buttons()



