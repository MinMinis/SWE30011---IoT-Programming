//Task 1. Control DC motor speed using potentiometer

int fan = 9; 

void setup() 
{
  pinMode(fan, OUTPUT); 
}

void loop()
{
   // read the input on analog pin 0:
   int analogueValue = analogRead(A0); //analogueValue reads analog input A0 value
   int fan_speed = analogueValue * (255 / 1023.0); //this scales the value between 0-255
   analogWrite(fan,fan_speed); 
   delay(10); 
}
