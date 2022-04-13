import RPi.GPIO as GPIO
import time
import pika
import random
import os
####Hum & Temp-sensor ###
import adafruit_dht
from board import *
SENSOR_PIN = D5
#GPIO SETUP
GPIO.setmode(GPIO.BCM)  
credentials = pika.PlainCredentials('haleema', '4chyst')
parameters = pika.ConnectionParameters('192.168.0.126',
                                   5672,
                                   '/',
                                   credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')
def callback4():
    dht11 = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)
    temperature = dht11.temperature
    humidity = dht11.humidity
    return(humidity,temperature)
    print(f"Humidity= {humidity:.2f}")
    print(f"Temperature= {temperature:.2f}°C")
###@# infinite loop
#while True:
 #       time.sleep(3)

def checkdht():
    for i in range(10):
        try:
            h, t =callback4()
            message=str(h)+","+str(t)
            channel.basic_publish(exchange='logs', routing_key='', body= message)
            print ("sent %r" %message) 

        except RuntimeError:
            pass
        time.sleep(5)

while True:
    checkdht()

connection.close()
