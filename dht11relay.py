import time
import sys

import Adafruit_DHT
import RPi.GPIO as GPIO

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

    try:
        while True:
            # Read the temperature and humidity
            humidity, temperature = readAdafruitDHT('11',4) #  dht 11 yada hangi ürünü kullanıyorsanız o 4 nolu pin girişi
                if temperature > 36.5:  #36,5 dereye geldiğinde 17 nolu pin 1 konumuna gelecektir.
                GPIO.output(17,GPIO.HIGH)
            else:
                GPIO.output(17,GPIO.LOW)
            time.sleep(0)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Bye")



