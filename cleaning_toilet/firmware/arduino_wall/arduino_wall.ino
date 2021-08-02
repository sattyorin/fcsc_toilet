#include "/home/yuyaletsnote/catkin_ws/src/fcsc_toilet/cleaning_toilet/firmware/arduino.hpp"

//// pin assign setting ////
#define SWITCH_PIN 2

//// init variable ////
std_msgs::Bool switch_state;

//// ros /////
ros::NodeHandle nh;
ros::Publisher pub_switch_state("interrupt_switch_state", &switch_state);

void publishSwichState()
{
	switch_state.data = digitalRead(SWITCH_PIN);
	pub_switch_state.publish(&switch_state);
}

void setup()
{
	//// pinMode ////
	pinMode(SWITCH_PIN, INPUT_PULLUP);

	//// nh ////
	nh.initNode();
	nh.advertise(pub_switch_state);

	delay(1000);
}

void loop()
{
	publishSwichState();
	nh.spinOnce();
}