import json
import paho.mqtt.client as mqtt
import psutil
import subprocess

def get_system_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    return cpu_usage, ram_usage

def get_power_consumption():
    try:
        result = subprocess.run(["upsc", "ups", "ups.realpower"], capture_output=True, text=True, check=True)
        power = result.stdout.strip()
        return power
    except subprocess.CalledProcessError as e:
        return 0



cpu, ram = get_system_usage()
power = get_power_consumption()
metrics = {
  "cpu_usage": cpu,
  "ram_usage": ram,
  "power_consumption": power
}

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set("mosquitto", "mqttpassword")
client.connect("sae203.louino.fr", 1883, 60)
payload = json.dumps(metrics)
client.publish("python/PVElouis", payload)
client.disconnect()


