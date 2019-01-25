import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(22,GPIO.OUT)

GPIO.output(22,GPIO.LOW)
time.sleep(15)

GPIO.output(22,GPIO.HIGH)
time.sleep(1)

GPIO.cleanup()

