/*
 * This ESP8266 NodeMCU code was developed by newbiely.com
 *
 * This ESP8266 NodeMCU code is made available for public use without any restriction
 *
 * For comprehensive instructions and wiring diagrams, please visit:
 * https://newbiely.com/tutorials/esp8266/esp8266-button-debounce
 */

 #define BUTTON_PIN     D6  // The ESP8266 pin D7 connected to button
 #define DEBOUNCE_TIME  50 // The debounce time in millisecond, increase this time if it still chatters
 
 int lastSteadyState = LOW;       // The previous steady state from the input pin
 int lastFlickerableState = LOW;  // The previous flickerable state from the input pin
 int button_state;                // The current reading from the input pin
 int ledState = false;
 
 // The following variables are unsigned longs because the time, measured in
 // milliseconds, will quickly become a bigger number than can be stored in an int.
 unsigned long lastDebounceTime = 0;  // The last time the output pin was toggled
 
 void setup() {
   // Initialize the Serial to communicate with the Serial Monitor.
   Serial.begin(9600);
   // Configure the ESP8266 pin as a pull-up input: HIGH when the button is open, LOW when pressed.
   pinMode(BUTTON_PIN, INPUT_PULLUP);
   pinMode(LED_BUILTIN, OUTPUT);
 }
 
 void loop() {
   // read the state of the switch/button:
   button_state = digitalRead(BUTTON_PIN);
 
   // check to see if you just pressed the button
   // (i.e. the input went from LOW to HIGH), and you've waited long enough
   // since the last press to ignore any noise:
 
   // If the switch/button changed, due to noise or pressing:
   if (button_state != lastFlickerableState) {
     // reset the debouncing timer
     lastDebounceTime = millis();
     // save the the last flickerable state
     lastFlickerableState = button_state;
   }
 
   if ((millis() - lastDebounceTime) > DEBOUNCE_TIME) {
     // whatever the reading is at, it's been there for longer than the debounce
     // delay, so take it as the actual current state:
 
     // if the button state has changed:
     if(lastSteadyState == HIGH && button_state == LOW)
     {
       Serial.println("The button is pressed");
       ledState = !ledState;
     }
     else if(lastSteadyState == LOW && button_state == HIGH)
     {
       Serial.println("The button is released");
       digitalWrite(LED_BUILTIN, ledState ? HIGH : LOW);
     }
 
     // save the the last steady state
     lastSteadyState = button_state;
 
   }
 }
 