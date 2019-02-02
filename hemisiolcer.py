import time
import sys
import playsound
import Adafruit_DHT
import RPi.GPIO as GPIO
import os
def readAdafruitDHT(moduleType,pin):
    """returns the humidity and temperature as integers."""
    sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
    sensor = sensor_args[moduleType]

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return (int(humidity), int(temperature))


if __name__ == '__main__':
    #Setup the GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17,GPIO.OUT)
    GPIO.setup(27,GPIO.OUT)
    GPIO.setup(21,GPIO.OUT)

    try:
        while True:
            # Read the temperature and humidity
            humidity, temperature = readAdafruitDHT('11',4)
            # If the temp is > 30 turn the pin on
            if temperature > 37.5:
                GPIO.output(17,GPIO.HIGH)
            else:
                GPIO.output(17,GPIO.LOW)
            time.sleep(0)
            if humidity > 64:
                GPIO.output(27,GPIO.HIGH)
                os.system('python3 /home/pi/nemac.py')
            else:
                GPIO.output(27,GPIO.LOW)
                os.system('python3 /home/pi/nemkapat.py')
            time.sleep(0)
            #if humidity < 63:
            #   os.system('python3 nemkapat.py')
           # else:
           #    os.system('python3 nemac.py')
           # time.sleep(0)

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Bye")








