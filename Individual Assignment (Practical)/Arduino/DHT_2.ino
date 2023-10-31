#include "dht.h"
dht DHT;
#define DHT11_PIN 7
int pin2 = 2;
int pin3 = 3;
int pin4 = 4;
int INA = 9;
int INB = 8;

int currentMode = 0;
void setup() {
  pinMode(pin2, OUTPUT);
  pinMode(pin3, OUTPUT);
  pinMode(pin4, OUTPUT);
  pinMode(INA, OUTPUT);
  pinMode(INB, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int value = Serial.read();
  if (value == '1' && currentMode != 1) {
    currentMode = 1;
  } else if ((value == '2' || value == '3') && currentMode != 2) {
    currentMode = 2;
  } else if (value == '4' && currentMode != 4){
    currentMode = 4;
  }
  int chk = DHT.read11(DHT11_PIN);
  Serial.print("Humidity = ");
  Serial.println(DHT.humidity);
  Serial.print("Temperature = ");
  Serial.println(DHT.temperature);
  if (currentMode == 1){
    if (DHT.humidity >= 0 && DHT.humidity <= 69) {
      digitalWrite(pin2, HIGH);
      digitalWrite(pin3, LOW);
      digitalWrite(pin4, LOW);
      digitalWrite(INA, LOW);
      digitalWrite(INB, LOW);
    } else if (DHT.humidity >= 70 && DHT.humidity <= 75) {
      digitalWrite(pin2, LOW);
      digitalWrite(pin3, HIGH);
      digitalWrite(pin4, LOW);
      digitalWrite(INA, LOW);
      digitalWrite(INB, LOW);
    } else if (DHT.humidity >= 76) {
      digitalWrite(pin2, LOW);
      digitalWrite(pin3, LOW);
      digitalWrite(pin4, HIGH);
      digitalWrite(INA, HIGH);
      digitalWrite(INB, LOW);
    }
  } else {
    if (value == '2') {
      digitalWrite(pin2, HIGH);
      digitalWrite(pin3, LOW);
      digitalWrite(pin4, LOW);
      digitalWrite(INA, LOW);
      digitalWrite(INB, LOW);
    } else if (value == '3') {
      digitalWrite(pin2, LOW);
      digitalWrite(pin3, HIGH);
      digitalWrite(pin4, LOW);
      digitalWrite(INA, LOW);
      digitalWrite(INB, LOW);
    } else if (value == '4') {
      digitalWrite(pin2, LOW);
      digitalWrite(pin3, LOW);
      digitalWrite(pin4, HIGH);
      digitalWrite(INA, HIGH);
      digitalWrite(INB, LOW);
    }
  }
  while (currentMode == 4) {
    digitalWrite(INA, HIGH);
    digitalWrite(INB, LOW);
  }
  Serial.print("CurrentMode = ");
  Serial.println(currentMode);
  delay(2000);
}