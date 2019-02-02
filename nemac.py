import RPi.GPIO as GPIO
import time

servoPIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization

try:
    p.ChangeDutyCycle(6)
    time.sleep(1)
except KeyboardInterrupt:
  p.stop()

  GPIO.cleanup()

