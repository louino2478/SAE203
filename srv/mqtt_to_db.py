import paho.mqtt.client as mqtt
import threading
import time
import json
import datetime
import mariadb

db_config = {
    'user': 'SAE',
    'password': 'DBPassword',
    'host': '127.0.0.1',
    'database': 'SAE',
    'port': 3306
}

data = {}
def on_mqtt_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("#")

def on_mqtt_message(client, userdata, msg):
    global data
    try:
        data[msg.topic] = json.loads(msg.payload.decode())
    except Exception as e:
        print(f"Erreur lors du traitement du message {msg.topic} : {e}")

def extract_data_safely(topic,key,lastvalue):
    global data
    try:
        return data[topic][key]
    except:
        print(f"Erreur lors du traitement de la valeur {key} du topic {topic}")
        return lastvalue

def push_data_periodically():
    global data
    temperature = {"louistemp":None,"louishum":None,"paweltemp":None,"pawelhum":None,"owmtemp":None,"owmhum":None}
    elec = {"louisPAPP":None,"pawelPAPP":None,"pawelPTEC":None}
    systeminfo = {"louisCPU":None,"louisRAM":None,"pawelCPU":None,"pawelRAM":None}
    while True:
        time.sleep(60)

        # temperature
        temperature["louistemp"] = extract_data_safely("esp32/AptLouis/DHT22","temperature",temperature["louistemp"])
        temperature["louishum"] = extract_data_safely("esp32/AptLouis/DHT22","humidity",temperature["louishum"])
        temperature["paweltemp"] = extract_data_safely("esp32/AptPawel/DHT11","temperature",temperature["paweltemp"])
        temperature["pawelhum"] = extract_data_safely("esp32/AptPawel/DHT11","humidity", temperature["pawelhum"])
        temperature["owmtemp"] = extract_data_safely("python/owm","temperature",temperature["owmtemp"])
        temperature["owmhum"] = extract_data_safely("python/owm","humidity",temperature["owmhum"])
        # electricité
        elec["louisPAPP"] = extract_data_safely("python/PVElouis","power_consumption",elec["louisPAPP"])
        elec["pawelPAPP"] = extract_data_safely("esp32/AptPawel/Linky","papp",elec["pawelPAPP"])
        elec["pawelPTEC"] = extract_data_safely("esp32/AptPawel/Linky","ptec",elec["pawelPTEC"])
        # sys info
        systeminfo["louisCPU"] = extract_data_safely("python/PVElouis","cpu_usage",systeminfo["louisCPU"])
        systeminfo["louisRAM"] = extract_data_safely("python/PVElouis","ram_usage",systeminfo["louisRAM"])
        systeminfo["pawelCPU"] = extract_data_safely("python/PVEPawel","cpu_usage",systeminfo["pawelCPU"])
        systeminfo["pawelRAM"] = extract_data_safely("python/PVEPawel","ram_usage",systeminfo["pawelRAM"])

        #print(datetime.datetime.now())
        #print(temperature)
        #print(elec)
        #print(systeminfo)

        # push data to mariaDB
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()
        insert_query = "INSERT INTO environment (timestamp, louistemp, louishum, paweltemp, pawelhum, owmtemp, owmhum) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (datetime.datetime.now(), temperature["louistemp"], temperature["louishum"], temperature["paweltemp"], temperature["pawelhum"], temperature["owmtemp"], temperature["owmhum"])
        cursor.execute(insert_query, values)
        insert_query = "INSERT INTO power_data (timestamp, louisPAPP, pawelPAPP, pawelPTEC) VALUES (%s, %s, %s, %s)"
        values = (datetime.datetime.now(), elec["louisPAPP"], elec["pawelPAPP"], elec["pawelPTEC"])
        cursor.execute(insert_query, values)
        insert_query = "INSERT INTO system_usage (timestamp, louisCPU, louisRAM, pawelCPU, pawelRAM) VALUES (%s, %s, %s, %s, %s)"
        values = (datetime.datetime.now(), systeminfo["louisCPU"], systeminfo["louisRAM"], systeminfo["pawelCPU"], systeminfo["pawelRAM"])
        cursor.execute(insert_query, values)
        conn.commit()
        cursor.close()
        conn.close()
        
        # clear receved data
        data = {}

threading.Thread(target=push_data_periodically, daemon=True).start()
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_mqtt_connect
mqttc.on_message = on_mqtt_message
mqttc.username_pw_set("mosquitto", "MQTTPassword")
mqttc.connect("sae203.louino.fr", 1883, 60)
mqttc.loop_forever()
