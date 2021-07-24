#include "/home/yuyaletsnote/catkin_ws/src/fcsc_toilet/cleanin_toilet/firmware/arduino.hpp"

//// pin assign setting ////
#define SWITCH_PIN 2
#define VACUUM_PIN 5

//// init variable ////
std_msgs::Bool switch_state;

//// define callback func ////
void setVacuumState( const std_msgs::Bool& vacuume_state);

//// ros /////
ros::NodeHandle nh;
ros::Subscriber<std_msgs::Bool> sub_vacuum_state("vacuume_state", setVacuumState);
ros::Publisher pub_switch_state("floor_switch_state", &switch_state);
ros::Subscriber<std_msgs::Bool> sub_interrupt("interrupt_switch_state", callbackInterrupt);

void setVacuumState(const std_msgs::Bool& vacuume_state)
{
	digitalWrite(VACUUM_PIN, vacuume_state.data);    
}

void publishSwichState()
{
	switch_state.data = digitalRead(SWITCH_PIN);
	pub_switch_state.publish(&switch_state);
}

void callbackInterrupt(const std_msgs::Bool &state)
{
	interrupt = state.data;
}

void setup()
{
	//// pinMode ////
	pinMode(VACUUM_PIN, OUTPUT);

	// 角度初期化部分
	digitalWrite(VACUUM_PIN, 0);

	//// ros ////
	nh.initNode();
	nh.subscribe(sub_vacuum_state);
	nh.advertise(pub_switch_state);
	delay(1000);
}

void loop() {
	publishSwichState();
	nh.spinOnce();
}