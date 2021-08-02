#define PID_COFF -1
#define PI_LIMIT_PIN A5

#include "/home/yuyaletsnote/catkin_ws/src/fcsc_toilet/cleaning_toilet/firmware/axis_arduino.hpp"

void publishLimitState()
{
	limit_state.data = digitalRead(PI_LIMIT_PIN);
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