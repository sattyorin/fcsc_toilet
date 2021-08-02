#define PI_PIN A5

void setup() {
	Serial.begin(9600);  
	pinMode(PI_PIN,INPUT);
}
 
void loop() {
	print (analogRead(PI_PIN));
	delay(100);
}