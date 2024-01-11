from common import *


def test():
    global data_sensor
    data_sensor = {
        "data_sensor": [
            {"sensor_key": "temperature", "sensor_value": 456},
            {"sensor_key": "humidity", "sensor_value": 789},
        ]
    }
    print(data_sensor)


test()
