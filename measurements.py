#!/usr/bin/python

import sys
import Adafruit_DHT
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def save_to_api(temp, hum):
    hed = {'Authorization': 'Bearer ' + os.getenv('API_TOKEN')}
    data = {'temp': temp, 'humidity': hum}

    response = requests.post( os.getenv('API_HOST')+'/api/measurements', json=data, headers=hed)
    print(response)

# ------------------------------------------------------------------------

sensor = Adafruit_DHT.DHT11
pin = os.getenv('PIN_DHT11')

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    save_to_api(temperature, humidity)
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)
