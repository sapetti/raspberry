from time import sleep
import RPi.GPIO as GPIO

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

GPIO.setup(16, GPIO.IN)
GPIO.setup(18, GPIO.IN)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.output(11, GPIO.HIGH)
GPIO.output(13, GPIO.HIGH)
GPIO.output(15, GPIO.HIGH)


def push_buttons():
	state = 0
	inc = 1
	while True:
    		if(GPIO.input(16) == True):
        		if(inc == 1):
            			state = state + 1
        		else:
            			state = state - 1

			if(state == 3):
				inc = 0
			elif(state == 0):
				inc = 1

			if(state == 1):
				turn_on(11)
			elif (state == 2):
				turn_on(13)
			elif (state == 3):
				turn_on(15)
			else:
				turn_on(10)
			print "pushed ON"
		if(GPIO.input(18) == True):
			turn_on(10)
			print "Pushed Exit"
			GPIO.cleanup()
			break
		sleep(0.2)


def turn_on(started_led):
	led_ids = [11,13,15]
	for led in led_ids:
		if led <= started_led:
			GPIO.output(led, GPIO.LOW)
		else:
			GPIO.output(led, GPIO.HIGH)
	

push_buttons()
