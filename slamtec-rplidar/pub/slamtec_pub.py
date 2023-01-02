import paho.mqtt.client as mqtt
import rplidar
import json

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# Create MQTT client and connect to the server
client = mqtt.Client()
client.on_connect = on_connect
client.connect("second-rpi-ip", 1883, 60)

# Connect to the RPLidar
lidar = rplidar.RPLidar("/dev/ttyUSB0")

# Start the motor
lidar.start_motor()

# Continuously send scan data to the second Raspberry Pi
while True:
    # Get the scan data
    scan_data = lidar.iter_scans()

    # Iterate through the scan data and send it to the second Raspberry Pi
    for scan in scan_data:
        # Convert the scan data to a JSON string
        data = json.dumps({"scan": scan})

        # Publish the data to the MQTT topic
        client.publish("rpi/autocar", data)

# Stop the motor and disconnect from the RPLidar
lidar.stop_motor()
lidar.disconnect()
