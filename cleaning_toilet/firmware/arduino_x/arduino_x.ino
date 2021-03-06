#define PID_COFF -1
#define ENC_COUNT_DIRECTION -1
#define PI_LIMIT_PIN A5
#define PI_THRESHOLD 150
#define GURE_RATIO 27.0
#define POS_TOLERANCE 5
#define Kp 1.0
#define Ki 0.0
#define Kd 0.1
#define POWER_LIMIT 30

#define PI_LIMIT_INPUT_MODE "INPUT"

#include "/home/yuyaletsnote/catkin_ws/src/fcsc_toilet/cleaning_toilet/firmware/axis_arduino.hpp"

void publishLimitState()
{
	if (analogRead(PI_LIMIT_PIN) < PI_THRESHOLD) limit_state.data = false;
	else limit_state.data = true;
	pub_limit_state.publish(&limit_state);
}

#include "/home/yuyaletsnote/catkin_ws/src/fcsc_toilet/cleaning_toilet/firmware/axis_arduino_loop.hpp"
