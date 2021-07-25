#include "/home/yuyaletsnote/catkin_ws/src/fcsc_toilet/cleanin_toilet/firmware/arduino.hpp"

//// pin assign setting ////
#define LMIT_PIN A5
#define VACUUM_PIN 5

//// set constant ////
#define PI_THRESHOLD 150

//// init variable ////
std_msgs::Bool limit_state;
bool interrupt;

//// define callback func ////
void callbackVacuumState(const std_msgs::Bool& vacuume_state);
void callbackInterrupt(const std_msgs::Bool &state);

//// ros /////
ros::NodeHandle nh;
ros::Subscriber<std_msgs::Bool> sub_vacuum_state("vacuume_state", callbackVacuumState);
ros::Subscriber<std_msgs::Bool> sub_interrupt("interrupt_switch_state", callbackInterrupt);
ros::Publisher pub_limit_state("floor_limit_state", &limit_state);

void callbackVacuumState(const std_msgs::Bool& vacuume_state)
{
	digitalWrite(VACUUM_PIN, vacuume_state.data);    
}

void publishLimitState()
{
	if (analogRead(PI_PIN) < PI_THRESHOLD) limit_state.data = false;
	else limit_state.data = true;
	pub_limit_state.publish(&limit_state);
}

void callbackInterrupt(const std_msgs::Bool &state)
{
	interrupt = state.data;
}

void setup()
{
	//// pinMode ////
	pinMode(VACUUM_PIN, OUTPUT);
	pinMode(PI_PIN, INPUT);

	// 角度初期化部分
	digitalWrite(VACUUM_PIN, 0);

	//// ros ////
	nh.initNode();
	nh.subscribe(sub_vacuum_state);
	nh.subscribe(sub_interrupt);
	nh.advertise(pub_limit_state);
	delay(1000);
}

void loop() {
	publishLimitState();
	nh.spinOnce();
}