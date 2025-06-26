#include <WiFi.h>
#include <DHT.h>
#include <PubSubClient.h>

const char* ssid        = "wifiSSID";
const char* wifipass    = "wifiPASSWORD";
const char* mqtthost    = "sae203.louino.fr";
const char* mqttUser    = "mosquitto";
const char* mqttPass    = "mqttpassword";
const char* topic       = "esp32/AptLouis/DHT22";

WiFiClient   espClient;
PubSubClient client(espClient);
DHT           dht(4, DHT22);

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Connexion WiFi
  Serial.print("Connexion WiFi");
  WiFi.begin(ssid, wifipass);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("\nWiFi OK");

  // Configuration du broker MQTT
  client.setServer(mqtthost, 1883);
  reconnectMQTT();
}

void reconnectMQTT() {
  while (!client.connected()) { // reconnection au serveur en cas de fermeture de connection.
    Serial.print("Tentative MQTT… ");
    String clientId = "esp32-client-";
    clientId += WiFi.macAddress();
    if (client.connect(clientId.c_str(), mqttUser, mqttPass)) {
      Serial.println("Connecté !");
    } else {
      Serial.print("Erreur ");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

void loop() {
  // Garde la connexion MQTT vivante
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();

  // Lecture capteur
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println("Erreur lecture DHT !");
    delay(2000);
    return;
  }

  // Construction du JSON
  String payload = "{\"humidity\":"+String(h,1)+",\"temperature\":"+String(t,1)+"}";

  // Envoi MQTT
  if (client.publish(topic, payload.c_str())) {
    Serial.print("Publié");
  } else {
    Serial.println("Échec publication");
  }
  Serial.println(payload);

  delay(5000);
}
