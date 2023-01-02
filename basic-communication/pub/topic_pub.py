########################################################
# Libraries
########################################################

import paho.mqtt.client as mqtt  # Library to MQTT Client
from datetime import datetime    # Library to Extract Current Time
import random                    # Library to get Random Numbers
import time                      # Library of System Wait Time

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
    print(datetime.now().strftime("%H:%M:%S") +" - " +str(value) + " - data published \n")    
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
topic = "Test/Esp"

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
     
    value = random.randint(0,1000)
    
    status = client.publish(topic, value)
    
    # Condition of Finnalization 
    if(value>= 850):
        break
        
    else:
        time.sleep(10)
        
client.disconnect()
print("End of Publish Data")