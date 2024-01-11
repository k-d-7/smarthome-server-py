from flask import Flask, jsonify, request
from mqtt.mqtt_client import MQTTClient
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv
import signal
from common import *
from handler.index_handler import gptResponseHandler


app = Flask(__name__)
socketio = SocketIO(app)


load_dotenv()
MQTT_SERVER = os.getenv("MQTT_SERVER")
MQTT_PORT = os.getenv("MQTT_PORT")
print(MQTT_PORT)

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
TOPICS = [
    "/innovation/airmonitoring/smarthome/sensors",
    "/innovation/airmonitoring/smarthome/light",
]

mqtt_client = MQTTClient(MQTT_SERVER, MQTT_PORT, TOPICS, MQTT_USERNAME, MQTT_PASSWORD)


# Get Text Voice from User
@app.route("/api/v1/speech", methods=["POST"])
def getTextVoice():
    textVoice = request.json.get("textVoice")
    if textVoice:
        rsp = gptResponseHandler(textVoice)
        return jsonify({"Message": rsp}), 200
    else:
        return jsonify({"error": "Invalid input"}), 400


# Flask route for publishing messages to the MQTT broker
@app.route("/api/publish", methods=["POST"])
def publish_message():
    topic = request.json.get("topic")
    message = request.json.get("message")

    if topic and message:
        mqtt_client.publishMessage(topic, message)
        return jsonify({"status": "Message published successfully"})
    else:
        return jsonify({"error": "Invalid input"}), 400


# Flask routes for SocketIO
@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


def gracefulShutdown(signal, frame):
    print("Shutting down gracefully...")
    mqtt_client.client.disconnect()
    print("MQTT client disconnected.")
    socketio.stop()
    print("SocketIO closed.")
    print("Server shut down.")
    exit(0)


# Register the signal handler for graceful shutdown
signal.signal(signal.SIGINT, gracefulShutdown)
signal.signal(signal.SIGTERM, gracefulShutdown)

if __name__ == "__main__":
    mqtt_client.connect()  # Connect the MQTT client
    app.run(host="0.0.0.0", port=5000, debug=False)
    socketio.run(app, debug=True)
