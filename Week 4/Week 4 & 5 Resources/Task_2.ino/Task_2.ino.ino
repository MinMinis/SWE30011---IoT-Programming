// Task 2. Print via serial port

void setup() 
{
   Serial.begin(9600);
}
void loop()
{
   Serial.println("IoT Programming is Great");
   delay(2000); 
}
