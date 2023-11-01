#include "dht.h"  //include library
dht DHT;
#define DHT11_PIN 7 //set Pin 7 (LED)
int pin2 = 2; //set Pin 2 (LED)
int pin3 = 3; //set Pin 3 (LED)
int pin4 = 4; //set Pin 4 (LED)
int INA = 9; // set Pin 9(Fan motor)
int INB = 8; //set Pin 8(Fan motor)

int currentMode = 0; // default of mode is 0
void setup() {
  pinMode(pin2, OUTPUT); 
  pinMode(pin3, OUTPUT); 
  pinMode(pin4, OUTPUT);
  pinMode(INA, OUTPUT);
  pinMode(INB, OUTPUT);
  //Set default of Fan to low
  digitalWrite(INA, LOW);
  digitalWrite(INB, LOW);
  Serial.begin(9600);
}

void loop() {
  int value = Serial.read(); //Read the Serial input
  if (value == '1' && currentMode != 1) { // if the Serial input is 1 and current mode is not 1
    currentMode = 1; // set current mode = 1 (automatically)
  } else if ((value == '2' || value == '3') && currentMode != 2) {
    currentMode = 2; // set the current mode = 2 (For displaying LED customly)
  } else if (value == '4' && currentMode != 4){
    currentMode = 4; // set current mode = 2 (For displaying LED customly and run fan motor)
  }
  int chk = DHT.read11(DHT11_PIN);
  Serial.print("Humidity = ");
  Serial.println(DHT.humidity); //Display humidity from sensor
  Serial.print("Temperature = ");
  Serial.println(DHT.temperature); //Display temperature from sensor
  if (currentMode == 1){ // the code will run automatically if currentMode is 1
    if (DHT.humidity >= 50 && DHT.humidity <= 60) {
      digitalWrite(pin2, HIGH); //trigger green light
      digitalWrite(pin3, LOW);
      digitalWrite(pin4, LOW);
      digitalWrite(INA, LOW);
      digitalWrite(INB, LOW);
    } else if (DHT.humidity >= 61 && DHT.humidity <= 70) {
      digitalWrite(pin2, LOW);
      digitalWrite(pin3, HIGH); //trigger yellow light
      digitalWrite(pin4, LOW);
      digitalWrite(INA, LOW);
      digitalWrite(INB, LOW);
    } else if (DHT.humidity >= 71 || DHT.humidity <= 49) {
      digitalWrite(pin2, LOW);
      digitalWrite(pin3, LOW);
      digitalWrite(pin4, HIGH); //trigger red light
      //run Fan motor clockwise
      digitalWrite(INA, HIGH); 
      digitalWrite(INB, LOW);
    }
  } else {
    if (value == '2') {
      digitalWrite(pin2, HIGH); //trigger green led
      digitalWrite(pin3, LOW);
      digitalWrite(pin4, LOW);
      digitalWrite(INA, LOW);
      digitalWrite(INB, LOW);
    } else if (value == '3') {
      digitalWrite(pin2, LOW);
      digitalWrite(pin3, HIGH); // trigger yellow led
      digitalWrite(pin4, LOW);
      digitalWrite(INA, LOW);
      digitalWrite(INB, LOW);
    } else if (value == '4') {
      digitalWrite(pin2, LOW);
      digitalWrite(pin3, LOW);
      digitalWrite(pin4, HIGH); //trigger red led
      digitalWrite(INA, HIGH); //trigger fan motor
      digitalWrite(INB, LOW);
    }
  }
  while (currentMode == 4) { // keep the fan run if current mode is 4
    digitalWrite(INA, HIGH); 
    digitalWrite(INB, LOW);
  }
  Serial.print("CurrentMode = ");
  Serial.println(currentMode); //print current mode for debugging
  delay(2000); // delay 2s
}