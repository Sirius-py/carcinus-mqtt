import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import json

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("rpi/autocar")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    data = json.loads(msg.payload.decode())

    # Control the motors and LEDs based on the scan data
    if data["scan"][0]["quality"] < 50:
        # Turn left
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(16, GPIO.LOW)
        # Turn on the left LED
        GPIO.output(18, GPIO.HIGH)
        # Send a message to the "carcinus.io" MQTT broker
        client.publish("rpi/autocar/status", "Turning left")
    elif data["scan"][270]["quality"] < 50:
        # Turn right
        GPIO.output(12, GPIO.LOW)
        GPIO.output(16, GPIO.HIGH)
        # Turn on the right LED
        GPIO.output(22, GPIO.HIGH)
        # Send a message to the "carcinus.io" MQTT broker
        client.publish("rpi/autocar/status", "Turning right")
    else:
        # Go straight
        GPIO.output(12, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        # Turn on the forward LED
        GPIO.output(24, GPIO.HIGH)
        # Send a message to the "carcinus.io" MQTT broker
        client.publish("rpi/autocar/status", "Going straight")

# Set up the GPIO outputs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

# Create MQTT client and connect to the server
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("first-rpi-ip", 1883, 60)

# Subscribe to the MQTT topic
client.subscribe("rpi/autocar")

# Start the MQTT loop
client.loop_forever()

# When the program is interrupted, stop the motors and turn off the LEDs
GPIO.output(12, GPIO.LOW)
GPIO.output(16, GPIO.LOW)
GPIO.output(18, GPIO.LOW)
GPIO.output(22, GPIO.LOW)
GPIO.output(24, GPIO.LOW)
