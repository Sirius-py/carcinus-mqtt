
#######################################################
# Libraries
########################################################

from pickle import TRUE
import paho.mqtt.client as mqtt  # Library to MQTT Client
from datetime import datetime    # Library to Extract Current Time
import random                    # Library to get Random Numbers
import time                      # Library of System Wait Time

import RPi.GPIO as GPIO
import time 
GPIO.setmode(GPIO.BCM)

GPIO.setup(1, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(7,GPIO.IN,pull_up_down=GPIO.PUD_UP)
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


def on_publish(client,userdata,result):             #create function for callback 
    pass

########################################################
# Variables
########################################################

# Create Flags in class as Global Variables
mqtt.Client.connected_flag = False 

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
client.on_connect = on_connect       

# Configure Receive Message Function
client.on_publish = on_publish 

########################################################
# Main Code
########################################################

# Connect to MQTT Broker
client.connect(broker, port, keepalive)


# Action to realize
while (True):
    
    GPIO.output(1, True)
    GPIO.output(16, True)
     
    input_state=GPIO.input(20)
    if input_state==TRUE:
        status = client.publish(topic,"ON")
        print("Motor 1 ON")
        time.sleep(2)

    input_state=GPIO.input(7)
    if input_state==TRUE:
        status = client.publish(topic,"OFF")
        print("Motor 2 ON")
        time.sleep(2)
    
    
        
client.disconnect()
print("End of Publish Data")
