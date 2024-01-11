import os
import openai
import json
import re
from dotenv import load_dotenv
import time
from datetime import datetime


load_dotenv()

print(os.getenv("CHAT-API-KEY"))

openai.api_key = os.getenv("CHAT-API-KEY")

msg_history = []
msg_history.append(
    {
        "role": "system",
        "content": 'Interpret the following user input and convert it into JSON of the form { "intent": ["string"],"action": ["string"],"device":["string"], "location":["string"], "ask_time":boolean, "ask_weather":boolean,"language":"string","response":"string" }. Only return JSON. User input:',
    }
)

model_id = "ft:gpt-3.5-turbo-0613:personal::8TRvVks1"


def generateResponse(user_input, role="user"):
    global msg_history
    msg_history.append({"role": role, "content": f"{user_input}"})
    start_time = time.time()
    completion = openai.ChatCompletion.create(model=model_id, messages=msg_history)
    end_time = time.time()
    response_time = end_time - start_time
    print("time response: " + str(response_time))
    response = completion.choices[0].message.content
    print(completion.choices[0].message.content.strip())
    msg_history.append({"role": "assistant", "content": f"{response}"})
    return response


# while True:
#     prompt = input("User:")
#     conversation = generateResponse(prompt, role="user")
#     if conversation is None:
#         break
#     try:
#         parsed_response = json.loads(conversation)

#         # Extract intent and entities from the parsed response
#         intent = parsed_response["intent"] if parsed_response["intent"] else []
#         action = parsed_response["action"] if parsed_response["action"] else []
#         device = parsed_response["device"] if parsed_response["device"] else []
#         location = parsed_response["location"] if parsed_response["location"] else []
#         ask_time = [
#             parsed_response["ask_time"] if parsed_response["ask_time"] else False
#         ]
#         ask_weather = [
#             parsed_response["ask_weather"] if parsed_response["ask_weather"] else False
#         ]
#         language = parsed_response["language"] if parsed_response["language"] else []
#         response = parsed_response["response"] if parsed_response["response"] else []
#         #     # Print the intent and entities
#         print("Intent:", intent)
#         print("Action:", action)
#         print("Device:", device)
#         print("Location:", location)
#         print("Ask time:", ask_time)
#         print("Ask weather:", ask_weather)
#         print("Language:", language)
#         if intent == ["ask_time"]:
#             print("Response:", response + str(datetime.now().strftime("%H:%M:%S")))
#         else:
#             print("Response:", response)

#     except json.JSONDecodeError:
#         print("Error: Unable to decode JSON response from the model.")
