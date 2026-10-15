// tcp.ino - ESP8266 (NodeMCU) WiFi TCP server controlling a single relay.
// Listens on port 8080; clients send "0" (relay OFF) or "1" (relay ON) over TCP.
#include <ESP8266WiFi.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

WiFiServer server(8080);

const int relayPin = D1;  // GPIO5
const int btnPin = D6;  

void setup() {
  pinMode(relayPin, OUTPUT);
  pinMode(btnPin, INPUT_PULLUP);

  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("");
  Serial.println("=============================");
  Serial.println("Connecting to WiFi");
  Serial.println("=============================");

  


  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("=============================");
  Serial.print("Connected! IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("=============================");

  server.begin();

  digitalWrite(relayPin, HIGH);  // Relay ON initially (active LOW)
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    Serial.println("Client connected.");

    while (client.connected()) {
      if (client.available()) {
        String data = client.readStringUntil('\n');
        data.trim();
        Serial.print("Received: ");
        Serial.println(data);

        int number = data.toInt();
        String response;

        if (data.length() == 0 || (number == 0 && data != "0")) {
          response = "Invalid input.";
        } 
        
        else if (number == 0) {
          digitalWrite(relayPin, LOW);
          response = "COMMAND {0} > RELAY STATUS >> 1: OFF";
        } 
        else if (number == 1){
          digitalWrite(relayPin, HIGH);
          response = "COMMAND {1} > RELAY STATUS >> 1: ON";
        } 
        else {
          response = "INVALID COMMAND!";
        }

        client.println(response);
        Serial.println("Replied: " + response);
      }
      // else
      //     {
      //     Serial.println("Client disconnected.");
      //     client.stop();
      //     }
    }

    client.stop();
    Serial.println("Client disconnected.");
  }
}