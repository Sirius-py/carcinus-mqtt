########################################################
# Libraries
########################################################

import paho.mqtt.client as mqtt  # Library to MQTT Client
import time
import RPi.GPIO as GPIO
from datetime import datetime    # Library to Extract Current Time

GPIO.setup(17, GPIO.OUT)

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
    
    # Extract Current Current Time
    now = datetime.now()    
    
    # Display Received Time & Received Message
    print(now.strftime("%H:%M:%S") + " - MSG: " + str(msg.payload)) #Imprime Trama de Entrada
    
    if "ON" in msg.payload:
        GPIO.output(17, GPIO.HIGH)
    elif "OFF" in msg.payload:
        GPIO.output(17, GPIO.LOW)

    # Finalizing Condition
    if(int(msg.payload.decode('utf-8'))>= 300):
        client.flag_end = True
        client.disconnect()
    else:
        client.flag_end = False 

########################################################
# Variables
########################################################

# Create Flags in class as Global Variables
mqtt.Client.connected_flag = False 
mqtt.Client.flag_end = False

# MQTT Parameters
broker="broker.emqx.io"
port = 1883         
keepalive = 60      # Maximum time [Sec] with Broker Communication
topic = "carcinus/raspitest"

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

GPIO.setmode(GPIO.BOARD)
GPIO.setup(17, GPIO.OUT)
# Action to realize
client.subscribe(topic)

# OTHER CODE HERE

# Flag Condition of No Finnalization 

if(client.flag_end==False):
    client.loop_forever()
