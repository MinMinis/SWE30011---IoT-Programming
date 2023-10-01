// Task 1 writing program for blinking LED using pin number 2
int led = 8;
int time = 100;
void setup() 
{
   // put your setup code here, to run once:
   
   // Set pin number 2 as output to send current to LED
   pinMode(led,OUTPUT);
}

void loop() 
{
    // put your main code here, to run repeatedly:

    // Start sending current to LED via pin number 2
    digitalWrite(led,HIGH); 

    // Delay the program for 1 second
    delay(time); 

    // Stop sending current to LED via pin number 2
    digitalWrite(led,LOW); 

    // Delay the program for 1 second
    delay(time); 
}
