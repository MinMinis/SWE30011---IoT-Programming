// Task 2 writing program for blinking LED and alarming buzzer using pin number 2

void setup() 
{
   // put your setup code here, to run once:
   
   // Set pin number 2 as output to send current to LED and buzzer
   pinMode(2,OUTPUT);
}

void loop() 
{
    // put your main code here, to run repeatedly:

    // Start sending current to LED and buzzer via pin number 2
    digitalWrite(2,HIGH); 

    // Delay the program for 1 second
    delay(1000); 

    // Stop sending current to LED and buzzer via pin number 2
    digitalWrite(2,LOW); 

    // Delay the program for 1 second
    delay(1000); 
}
