import json
import paho.mqtt.client as mqtt
import requests

def getWeather():
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?appid=APIKEY&q=Mont-De-Marsan&units=metric")
    data = response.json()
    return data

data = getWeather()
metrics = {
    "temperature" : data["main"]["temp"],
    "humidity" : data["main"]["humidity"]
    }



client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set("mosquitto", "mqttpassword")
client.connect("sae203.louino.fr", 1883, 60)
payload = json.dumps(metrics)
client.publish("python/owm", payload)
client.disconnect()
