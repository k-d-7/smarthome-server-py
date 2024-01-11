from gpt_assistant.chatgpt_response import *
import json
from mqtt.mqtt_client import MQTTClient
from common import *
from dotenv import load_dotenv

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


def gptResponseHandler(textVoice):
    conversation = generateResponse(textVoice, role="user")
    if conversation is None:
        return False
    try:
        parsed_response = json.loads(conversation)

        # Extract intent and entities from the parsed response
        intent = parsed_response["intent"] if parsed_response["intent"] else []
        action = parsed_response["action"] if parsed_response["action"] else []
        device = parsed_response["device"] if parsed_response["device"] else []
        location = parsed_response["location"] if parsed_response["location"] else []
        ask_time = [
            parsed_response["ask_time"] if parsed_response["ask_time"] else False
        ]
        ask_weather = [
            parsed_response["ask_weather"] if parsed_response["ask_weather"] else False
        ]
        language = parsed_response["language"] if parsed_response["language"] else []
        response = parsed_response["response"] if parsed_response["response"] else []
        #     # Print the intent and entities
        print("Intent:", intent)
        print("Action:", action)
        print("Device:", device)
        print("Location:", location)
        print("Ask time:", ask_time)
        print("Ask weather:", ask_weather)
        print("Language:", language)
        if intent == ["ask_time"]:
            print("Response:", response + str(datetime.now().strftime("%H:%M:%S")))
        else:
            print("Response:", response)

    except json.JSONDecodeError:
        print("Error: Unable to decode JSON response from the model.")
        return False

    commandControlHandler(intent, action, device)

    return response


def commandControlHandler(intent, action, device):
    mapCommand = zip(action, device)
    global data_device
    command = list(mapCommand)
    if command[0] == ("turn_on", "light", "living_room"):
        data_device = {
            "data_device": [
                {"device_key": "light", "device_value": 1},
            ]
        }
        mqtt_client.publishMessage(TOPICS[1], json.dumps(data_device))
    elif command[0] == ("turn_off", "light", "living_room"):
        data_device = {
            "data_device": [
                {"device_key": "light", "device_value": 0},
            ]
        }
        mqtt_client.publishMessage(TOPICS[1], json.dumps(data_device))
