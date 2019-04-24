import time
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import os
import lcddriver
from datetime import datetime
import urllib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

icerik_metni = "test"
sensor = Adafruit_DHT.DHT11
pin = 20
pin2 = 4
lcd = lcddriver.lcd()
lcd.lcd_clear()
mail_gitti = True

def internet():
    try :
        url = "https://www.google.com"
        urllib.urlopen(url)
        return True
    except :
        return False

def mail_yolla(icerik_metni, mail_gitti):
    try:
        fromaddr = "ehminternetcafebilgi@gmail.com"
        toaddr = "muratdikmetas@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "KULUCKA MAKINASI SAATLIK DURUM BILGISIDIR"
        msg.attach(MIMEText(body, 'plain'))
        filename = "bilgidosyasi.txt"
        attachment = open("/home/pi/lcd/bilgidosyasi.txt", "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, "Fatsa052")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        mail_gitti = False

    except:
        print("Mail Gonderilemedi !!!")

def bilgidosyasi():
    dosya = open("/home/pi/lcd/bilgidosyasi.txt", "a")
    dosya.write('\n')
    dosya.write(gunvesaat + " " "1. SICAKLIK : " + str(temperature) + " " + "1. NEM : " + str(humidity) + "%")
    dosya.write('\n')
    dosya.write(gunvesaat + " " "2. SICAKLIK : " + str(sicaklik) + " " + "2. NEM : " + str(nem) + "%")
    dosya.write('\n')
    dosya.close()

def dosyasilme():
    try:
        os.remove("/home/pi/lcd/bilgidosyasi.txt")
        return True
    except:
        return False

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17,GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(27,GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(21,GPIO.OUT)
    GPIO.setup(15,GPIO.OUT)
#   GPIO.setup(22,GPIO.OUT)

    try:
        while True:
            gunvesaat = time.strftime("%d/%m/%Y %H:%M:%S")
            zaman = datetime.now()
            dakika = zaman.strftime("%M")
            saniye = zaman.strftime("%S")
            tamsure = zaman.strftime("%M:%S")
            dakika2 = time.localtime().tm_min
            saniye2 = time.localtime().tm_sec

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

            if dakika == "56" :
                if internet() == True:
                    body = gunvesaat + " " "1. SICAKLIK : " + str(temperature) + " " + "1. NEM : " + str(humidity) +$
                    if mail_gitti == True:
                        mail_yolla(icerik_metni,mail_gitti)


            if dakika == "10" or dakika == "20" or dakika == "30" or dakika == "40" or dakika == "50":
                bilgidosyasi()

            if dakika == "59":
                dosyasilme()
                mail_gitti = True

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Bye")
