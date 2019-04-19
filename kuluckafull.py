import time
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import os
import lcddriver
import smtplib
from email.mime.text \
import MIMEText
from datetime import datetime
import urllib


icerik_metni = "test"
sensor = Adafruit_DHT.DHT11
pin = 20
pin2 = 4
lcd = lcddriver.lcd()
lcd.lcd_clear()

def internet():
    try :
        url = "https://www.google.com"
        urllib.urlopen(url)
        return True
    except :
        return False


def mail_yolla(icerik_metni):
    smtpadresi = "smtp.gmail.com"
    smtpport = 587
    kullaniciadi = "ehminternetcafebilgi@gmail.com"
    sifre = "Fatsa052"
    gonderilecekadres = ["ehminternetcafebilgi@gmail.com", "muratdikmetas@gmail.com"]
    konu = "Kulucka Isi Bildirisidir"
    mail = MIMEText(icerik, "html", "utf-8")
    mail["From"] = kullaniciadi
    mail["Subject"] = konu
    mail["To"] = ",".join(gonderilecekadres)
    mail = mail.as_string()
    s = smtplib.SMTP(smtpadresi, smtpport)
    s.starttls()
    s.login(kullaniciadi, sifre)
    s.sendmail(kullaniciadi, gonderilecekadres, mail)


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17,GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(27,GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(21,GPIO.OUT)
    GPIO.setup(15,GPIO.OUT)
    
    try:
        while True:
            zaman = datetime.now()
            dakika = zaman.strftime("%M")
            print (dakika)
            time.sleep(1)
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            nem, sicaklik = Adafruit_DHT.read_retry(sensor, pin2)

            if humidity is not None and temperature is not None:
                lcd.lcd_display_string('SICAKLIK: {0:0.1f} C'.format(temperature), 1)
                lcd.lcd_display_string('NEM: {0:0.1f} %'.format(humidity), 2)
                time.sleep(2)
                lcd.lcd_clear()
            else:
                GPIO.output(17, GPIO.LOW)
                GPIO.output(27, GPIO.LOW)
                lcd.lcd_display_string('SICAKLIK VE NEM', 1)
                lcd.lcd_display_string('OKUNAMIYOR', 2)
                time.sleep(5)
                os.system('sudo reboot')

            time.sleep(0)

            if nem is not None and sicaklik is not None:
                lcd.lcd_display_string('2.SICAKLIK: {0:0.1f} C'.format(sicaklik), 1)
                lcd.lcd_display_string('2.NEM: {0:0.1f} %'.format(nem), 2)
                time.sleep(1)

            else:
                GPIO.output(17, GPIO.LOW)
                GPIO.output(27, GPIO.LOW)
                lcd.lcd_display_string('2SICAKLIK VE NEM', 1)
                lcd.lcd_display_string('OKUNAMIYOR', 2)
                time.sleep(5)
                os.system('sudo reboot')


            if temperature > 37:
                GPIO.output(17, GPIO.HIGH)
            else:
                GPIO.output(17, GPIO.LOW)
            time.sleep(0)
            if temperature > 39:
                os.system('sudo reboot')
            time.sleep(0)

            if humidity > 62:
                    GPIO.output(27,GPIO.HIGH)
# os.system('python /home/pi/kapakac.py') #nem 64 un ustun kapat
            else:
                    GPIO.output(27,GPIO.LOW)
# os.system('python /home/pi/kapakkapat.py') #nem 64 un ac
            time.sleep(0)

            if humidity > 80:
                    GPIO.output(15,GPIO.HIGH)
# os.system('python /home/pi/kapakac.py')
            else:
                    GPIO.output(15,GPIO.LOW)
# os.system('python /home/pi/kapakkapat.py')
            time.sleep(2)

            if dakika == "45" :
                if internet() == True:
                    icerik = "1. SICAKLIK : " + str(temperature) + " " + "1. NEM : " + str(humidity) + "%" + " " + "2. SICAKLIK : " + str(sicaklik) + " " + "2. NEM : " + str(nem) + "%"
                    mail_yolla(icerik_metni)

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Bye")
