#define PID_COFF -1
#define ENC_COUNT_DIRECTION -1
#define PI_LIMIT_PIN A5
#define GURE_RATIO 100.0
#define POS_TOLERANCE 5
#define Kp 2.0
#define Ki 0.0
#define Kd -0.1
#define POWER_LIMIT 100

#define PI_LIMIT_INPUT_MODE "INPUT_PULLUP"

#include "/home/yuyaletsnote/catkin_ws/src/fcsc_toilet/cleaning_toilet/firmware/axis_arduino.hpp"

void publishLimitState()
{
	limit_state.data = !digitalRead(PI_LIMIT_PIN);
	pub_limit_state.publish(&limit_state);
}

#include "/home/yuyaletsnote/catkin_ws/src/fcsc_toilet/cleaning_toilet/firmware/axis_arduino_loop.hpp"