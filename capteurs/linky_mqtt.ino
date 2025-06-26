#include <PubSubClient.h>
#include <string>
#include <WiFiMulti.h>
WiFiMulti wifiMulti;
#define DEVICE "ESP32"

String val = "";
#define WIFI_SSID "wifiSSID"
#define WIFI_PASSWORD "wifiPASSWORD"

const char *mqttServer = "sae203.louino.fr";
const char *mqttUser = "mosquitto";
const char *mqttPassword = "mqttpassword";
const char *topic = "esp32/AptPawel/Linky";
int count = 0;
String va = "";
String a = "";
String amax = "";
String heure = "";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  Serial2.begin(1200, SERIAL_7E1, 16);
  WiFi.mode(WIFI_STA);
  wifiMulti.addAP(WIFI_SSID, WIFI_PASSWORD);
  
  Serial.print("Connecting to wifi");
  while (wifiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(100);
  }
  client.setServer(mqttServer, 1883);
  reconnectMqtt();
  count = 0;
}

void reconnectMqtt(){
  while (!client.connected()) {
    String clientId = "esp32-client-";
    clientId += String(WiFi.macAddress());
    Serial.printf("Le client %s se connecte au server SAE203. \n", clientId.c_str());
    if (client.connect(clientId.c_str(), mqttUser, mqttPassword)) {
      Serial.println("Connecté au serveur SAE203.");
    } else {
      Serial.print("Problème de connexion: ");
      Serial.print(client.state());
      delay(2000);
    }
  }
}


void loop() {
  if (!client.connected()) {
    reconnectMqtt();
  }
  client.loop();

  val = Serial2.readStringUntil('\n');
  val.trim();
  String papp = "PAPP";
  if ((val.substring(0, 4) == papp.substring(0, 4))) {
    va = val.substring(5, 10);
    Serial.println(va);
  }
  String iinst = "IINST";
  if ((val.substring(0, 5) == iinst.substring(0, 5))) {
    a = val.substring(6, 9);
    Serial.println(a);
  }
  String imax = "IMAX";
  if ((val.substring(0, 4) == imax.substring(0, 4))) {
    amax = val.substring(5, 8);
    Serial.println(amax);
  }
  String ptec = "PTEC";
  String hc = "Heure Creuse";
  String hp = "Heure Pleine";
  if ((val.substring(0, 4) == ptec.substring(0, 4))) {
    if ((val.substring(5, 7) == hc.substring(0, 2))) {
      Serial.println("Heure creuse");
      heure = "1";
    }
    else {
      Serial.println("Heure pleine");
      heure = "0";
    }
  }

  if (count > 50) {
    Serial.println("Data Sent");
    String data = "{\"papp\":"+String(va.toInt())+",\"iinst\":"+String(a.toInt())+",\"imax\":"+String(amax.toInt())+",\"ptec\":"+String(heure)+"}";
    Serial.println(data);
    client.publish(topic, data.c_str());
    count = 0;
  }
  count++;
  Serial.println(count);



  
  //delay(100);
}
