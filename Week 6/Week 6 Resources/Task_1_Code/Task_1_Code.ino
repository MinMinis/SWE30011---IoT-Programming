//Reading potentiometer value through serial monitor

void setup() 
{
   Serial.begin(9600);
}

void loop()
{
   // read the input on analog pin 0:
   int analogueValue = analogRead(A0); 
   Serial.println(analogueValue);
}
