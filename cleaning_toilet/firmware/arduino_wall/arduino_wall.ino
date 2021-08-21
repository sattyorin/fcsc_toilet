#include "/home/yuyaletsnote/catkin_ws/src/fcsc_toilet/cleaning_toilet/firmware/arduino.hpp"
#include <Adafruit_NeoPixel.h>

//// pin assign setting ////
#define SWITCH_PIN 4
#define LED_DATA_PIN 6
#define NUMPIXELS 8

//// init variable ////
std_msgs::Bool switch_state;

//// LED ////
Adafruit_NeoPixel pixels(NUMPIXELS, LED_DATA_PIN, NEO_GRB + NEO_KHZ800);
void messageCb(const std_msgs::String& toggle_msg);

//// ros /////
ros::NodeHandle nh;
ros::Publisher pub_switch_state("interrupt_switch_state", &switch_state);
ros::Subscriber<std_msgs::String> sub("toggle_led_state", messageCb );

void messageCb(const std_msgs::String& toggle_msg){
	String led_mode = toggle_msg.data;
	pixels.clear();
	if(led_mode == "MOVE")for(int i=0;i<NUMPIXELS;i++)pixels.setPixelColor(i, pixels.Color(255, 0, 0));
	if(led_mode == "MOVE2WAIT")for(int i=0;i<NUMPIXELS;i++)pixels.setPixelColor(i, pixels.Color(255, 255, 0));
	if(led_mode == "WAIT")for(int i=0;i<NUMPIXELS;i++)pixels.setPixelColor(i, pixels.Color(0, 255, 0));
	pixels.show();
}

void publishSwichState()
{
	switch_state.data = digitalRead(SWITCH_PIN);
	pub_switch_state.publish(&switch_state);
}

void setup()
{
	//// pinMode ////
	pinMode(SWITCH_PIN, INPUT_PULLUP);
	pixels.begin();

	//// nh ////
	nh.initNode();
	nh.advertise(pub_switch_state);
	nh.subscribe(sub);

	delay(1000);
}

void loop()
{
	publishSwichState();
	nh.spinOnce();
	delay(50);
}