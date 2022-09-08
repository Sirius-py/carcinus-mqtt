########################################################
# Libraries
########################################################

import paho.mqtt.client as mqtt  # Library to MQTT Client
import time
import RPi.GPIO as GPIO
from datetime import datetime    # Library to Extract Current Time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(23, GPIO.OUT)

########################################################
# Functions
########################################################

# Function to Connect MQTT Client to Broker
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

# Function to Receive data from Broker Subscription
def on_message(client, userdata, msg):
    
    if b'ON' in msg.payload:
        print("LED ON")
        GPIO.output(23, True)
    elif b'OFF' in msg.payload:
        print("LED OFF")
        GPIO.output(23, False)

########################################################
# Variables
########################################################

# Create Flags in class as Global Variables
mqtt.Client.connected_flag = False 
mqtt.Client.flag_end = False

# MQTT Parameters
broker="test.mosquitto.org"
port = 1883         
keepalive = 60      # Maximum time [Sec] with Broker Communication
topic = "raspicarcinus/topic"

########################################################
# Initial Configuration
########################################################

# Create MQTT Instance
client = mqtt.Client()

# Configure MQTT Broker Connection Status Function             
client.on_connect=on_connect       

# Configure Receive Message Function
client.on_message = on_message

########################################################
# Main Code
########################################################

# Connect to MQTT Broker
client.connect(broker, port, keepalive)

# Action to realize
client.subscribe(topic)

# OTHER CODE HERE

# Flag Condition of No Finnalization 

client.loop_forever()