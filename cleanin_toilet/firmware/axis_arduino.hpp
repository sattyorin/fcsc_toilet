#ifndef axis_arduino_hpp_
#define axis_arduino_hpp_

#include "arduino.hpp"

//// pin assign setting ////
#define ENC_A 2
#define ENC_B 3
#define PID_COFF 1
#define IN_A_PIN 12
#define IN_B_PIN 9
#define PWM_PIN  10

//// set constant ////
#define PI 3.141592
#define REFERENCE_CIRCLE_DIAMETER 30
#define POWER_LIMIT 30
#define Kp 1.0
#define Ki 0.0
#define Kd -0.1

//// init variable ////
volatile int current_enc = 0;
volatile int current_pos_mm = 0;
int target_pos_mm = 0;
int32_t last_calc_time = 0;
float integral = 0.0;
int last_error = 0;
bool interrupt = False;
std_msgs::Int32 current_pos;

//// define callback func ////
void setTargetPos(const std_msgs::Int32 &pos);

//// ros /////
ros::NodeHandle nh;
ros::Publisher pub_current_pos("current_pos", &current_pos);
ros::Subscriber<std_msgs::Int32> sub_target_pos("target_pos", callbackTargetPos);
ros::Subscriber<std_msgs::Bool> sub_interrupt("interrupt_switch_state", callbackInterrupt);


void publishCurrentPos()
{
	current_pos.data = current_pos_mm;
	pub_current_pos.publish(&current_pos);
}

void getState()
{
	current_pos_mm = (float)current_enc/13.0/27.0*(REFERENCE_CIRCLE_DIAMETER*PI); // what are the numbers 13.0 and 27.0
}

void countEnc()
{
	if (digitalRead(ENC_B) == 1) current_enc --;
	else current_enc++;
}

void setPWM(int target_pwm)
{
	if (target_pwm < 0)
	{
		digitalWrite(IN_A_PIN, LOW);
		digitalWrite(IN_B_PIN, HIGH);
	} 
	else
	{
		digitalWrite(IN_A_PIN, HIGH);
		digitalWrite(IN_B_PIN, LOW);
	}

	if (target_pwm < 0) target_pwm = -target_pwm;
	if (target_pwm > 255) target_pwm = 255;
	if (target_pwm > POWER_LIMIT) target_pwm = POWER_LIMIT;
	analogWrite(PWM_PIN, target_pwm);
}

void callbackTargetPos(const std_msgs::Int32 &pos)
{
	target_pos_mm = pos.data;
}

void callbackInterrupt(const std_msgs::Bool &state)
{
	interrupt = state.data;
}

void servo()
{
	int error = target_pos_mm - current_pos_mm;
	integral=integral+(float)error*(micros()-last_calc_time)/1000000;
	float normalized_pid=Kp*error+Ki*integral+Kd*(error - last_error);
	last_error = error;
	last_calc_time = micros();
	setPWM(int(PID_COFF*normalized_pid));
}

void setup()
{
	//// pinMode ////
	pinMode(IN_A_PIN, OUTPUT);
	pinMode(IN_B_PIN, OUTPUT);
	pinMode(PWM_PIN, OUTPUT);
	pinMode(13, OUTPUT); // what is it?

	//// write ////
	digitalWrite(IN_A_PIN, LOW);
	digitalWrite(IN_B_PIN, LOW);
	analogWrite(PWM_PIN, 0);

	//// encoder ////
	attachInterrupt(digitalPinToInterrupt(ENC_A), countEnc, RISING);

	//// nh ////
	nh.initNode();
	nh.advertise(pub_current_pos);
	nh.subscribe(sub_pos_command);

	delay(1000);
}

void loop()
{
	publishCurrentPos();
	servo();
	nh.spinOnce();
}

#endif