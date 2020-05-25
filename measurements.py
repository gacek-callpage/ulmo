#!/usr/bin/python

import sys
import Adafruit_DHT
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def save_to_db(db, values):
    
    mycursor = db.cursor()

    sql = "INSERT INTO measurements (temp, humidity) VALUES (%s, %s)"
    mycursor.execute(sql, values)

    db.commit()

# ------------------------------------------------------------------------

mydb = mysql.connector.connect(
  host=os.getenv('DB_SERVER'),
  user=os.getenv('DB_USER'),
  passwd=os.getenv('DB_PASSWORD'),
  database=os.getenv('DB_DATABASE')
)

sensor = Adafruit_DHT.DHT11
pin = os.getenv('PIN_DHT11')

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    val = (temperature, humidity)
    save_to_db(mydb, val);
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)