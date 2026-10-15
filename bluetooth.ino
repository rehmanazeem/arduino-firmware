// bluetooth.ino - ESP8266 (NodeMCU) WiFi TCP server controlling a single relay.
// Listens on port 8080; clients send "0" (relay OFF) or "1" (relay ON) over TCP.
// (Includes commented-out scaffolding for a second relay.)
#include <ESP8266WiFi.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

WiFiServer server(8080);

const int relayPin = D1;  // GPIO5
// const int relayPin2 = D2;  // GPIO5

void setup() {
  pinMode(relayPin, OUTPUT);
  // pinMode(relayPin2, OUTPUT);

  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi");

  


  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println(".");
  }

  Serial.println();
  Serial.print("Connected! IP: ");
  Serial.println(WiFi.localIP());

  server.begin();

  digitalWrite(relayPin, HIGH);  // Relay ON initially (active LOW)
  // digitalWrite(relayPin, LOW);  // Relay ON initially (active LOW)
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
          // digitalWrite(relayPin2, LOW);
          response = "COMMAND {0} > RELAY STATUS >> 1: OFF";
        } 
        else if (number == 1){
          digitalWrite(relayPin, HIGH);
          // digitalWrite(relayPin2, HIGH);
          response = "COMMAND {1} > RELAY STATUS >> 1: ON";
        } 
        // else if (number == 2){
        //   digitalWrite(relayPin, HIGH);
        //   // digitalWrite(relayPin2, LOW);
        //   response = "COMMAND {0} > RELAY STATUS >> 1: OFF, 2: ON";
        // } else if (number == 3){
        //   digitalWrite(relayPin, HIGH);
        //   // digitalWrite(relayPin2, HIGH);
        //   response = "COMMAND {0} > RELAY STATUS >> 1: OFF, 2: OFF";
        // } 
        else {
          response = "INVALID COMMAND!";
        }

        client.println(response);
        Serial.println("Replied: " + response);
      }
    }

    client.stop();
    Serial.println("Client disconnected.");
  }
}