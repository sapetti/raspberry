import RPi.GPIO as GPIO
import time

GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT) ##puerto gpio 17 como salida
GPIO.setup(27, GPIO.OUT) ##puerto gpio 27 como salida

def blink():
    print "Iniciando script..."
    iteracion = 0
    while iteracion < 5:
        GPIO.output(17, True) ##Encender el 17
        GPIO.output(27, False) ##Apagar el 27
        time.sleep(1)
        GPIO.output(17, False) ##Apagar el 17
        GPIO.output(27, True) ##Encender el 27
        time.sleep(1)
        iteracion = iteracion + 1
    print "Teardown GPIO..."
    GPIO.cleanup()

blink()
