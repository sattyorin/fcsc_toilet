#define PID_COFF 1
#define PI_LIMIT_PIN A5
#define PI_THRESHOLD 150

#include "/home/yuyaletsnote/catkin_ws/src/fcsc_toilet/cleaning_toilet/firmware/axis_arduino.hpp"

void publishLimitState()
{
	if (analogRead(PI_LIMIT_PIN) < PI_THRESHOLD) limit_state.data = false;
	else limit_state.data = true;
	pub_limit_state.publish(&limit_state);
}

#include "/home/yuyaletsnote/catkin_ws/src/fcsc_toilet/cleaning_toilet/firmware/axis_arduino_loop.hpp"

// void loop()
// {
// 	publishCurrentPos();
// 	publishLimitState();
// 	servo();
// 	nh.spinOnce();
// }