# import serial.tools.list_ports
import sys
import time
import os
from dotenv import load_dotenv
import json

# from Adafruit_IO import MQTTClient
import paho.mqtt.client as mqttclient

load_dotenv()
MQTT_SERVER = os.getenv("MQTT_SERVER")
MQTT_PORT = os.getenv("MQTT_PORT")


MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
FEEDS = ["/innovation/airmonitoring/smarthome/sensors"]

print(MQTT_USERNAME)
print(MQTT_PASSWORD)


def connected(client, userdata, flags, rc):
    if rc == 0:
        for f in FEEDS:
            print("Subscribing to " + f)
            client.subscribe(f)
        print("Connected to broker")
    else:
        print("Connection failed")
    # loop_flag = 0


def subscribe(client, userdata, mid, granted_qos):
    print("Subscribed Successfully")


def disconnected(client):
    print("Disconnected from broker")
    sys.exit(1)


def message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print("Received " + payload + " from " + str(msg.topic))
    # todo: make a decision based on the receiving data from topic


client = mqttclient.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(MQTT_SERVER, int(MQTT_PORT))

# MQTT events
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.loop_start()


def processData(data):
    data_sensor = {
        "data_sensor": [
            {"sensor_key": "temperature", "sensor_value": data},
            {"sensor_key": "humidity", "sensor_value": data},
        ]
    }
    client.publish(FEEDS[0], json.dumps(data_sensor))
    # print("Published to " + str(FEEDS[0]) + " with message: " + data_sensor)


data = 10

while True:
    # readSerial()
    time.sleep(30)
    processData(data)
    data += 1
    print("Data: " + str(data))
    pass
