#ifndef axis_arduino_hpp_
#define axis_arduino_hpp_

#include "arduino.hpp"

//// pin assign setting ////
#define ENABLE_PIN 11
#define ENC_A 2
#define ENC_B 3
#define IN_A_PIN 12
#define IN_B_PIN 9
#define PWM_PIN  10
#define LED_PIN 13

//// set constant ////
#define PI 3.141592
#define REFERENCE_CIRCLE_DIAMETER 30
#define PULSE_NUM 13.0

//// init variable ////
volatile int current_enc = 0;
int pre_enc = 0;
volatile int current_pos_mm = 0;
int target_pos_mm = 0;
int32_t last_calc_time = 0;
float integral = 0.0;
int last_error = 0;
String control_mode = "None";
unsigned long last_pwm_time;
bool change_target_pos = false;
int count = 0;
std_msgs::Bool limit_state;
std_msgs::Int32 current_pos;
std_msgs::Bool finish_flag;
std_msgs::Bool error_flag;
int pre_target_pwm = 0;

//// define callback func ////
void callbackTargetPos(const std_msgs::Int32 &pos);
void callbackTargetPWM(const std_msgs::Int32 &pwm);
void callbackControlMode(const std_msgs::String &mode);
void callbackResetFlag(const std_msgs::Bool &flag);

//// ros /////
ros::NodeHandle nh;
ros::Publisher pub_current_pos("current_pos", &current_pos);
ros::Publisher pub_limit_state("axis_limit_state", &limit_state);
ros::Publisher pub_finish_flag("finish_flag", &finish_flag);
ros::Publisher pub_error_flag("error_flag", &error_flag);
ros::Subscriber<std_msgs::Int32> sub_target_pos("target_pos", callbackTargetPos);
ros::Subscriber<std_msgs::Int32> sub_target_pwm("target_pwm", callbackTargetPWM);
ros::Subscriber<std_msgs::String> sub_control_mode("control_mode", callbackControlMode);
ros::Subscriber<std_msgs::Bool> sub_reset_flag("reset_flag", callbackResetFlag);

void getState()
{
	current_pos_mm = (float)current_enc/PULSE_NUM/GURE_RATIO*(REFERENCE_CIRCLE_DIAMETER*PI);
}

void publishCurrentPos()
{
	getState();
	current_pos.data = current_pos_mm;
	pub_current_pos.publish(&current_pos);
}

void publishFinishFlag()
{
	pub_finish_flag.publish(&finish_flag);
}

void publishErrorFlag()
{
	pub_error_flag.publish(&error_flag);
}

void countEnc()
{
	if (digitalRead(ENC_B) == 1) current_enc += ENC_COUNT_DIRECTION;
	else current_enc -= ENC_COUNT_DIRECTION;
}

void setPWM(int target_pwm)
{
	if (target_pwm == 0)
	{
		analogWrite(PWM_PIN, target_pwm);
	}
	else
	{
		if (target_pwm < 0)
		{
			if (pre_target_pwm == -1)
			{
				digitalWrite(IN_A_PIN, LOW);
				digitalWrite(IN_B_PIN, LOW);
				delay(10);
			}
			digitalWrite(IN_A_PIN, LOW);
			digitalWrite(IN_B_PIN, HIGH);
			pre_target_pwm = 1;
		}
		else
		{
			if (pre_target_pwm == 1)
			{
				digitalWrite(IN_A_PIN, LOW);
				digitalWrite(IN_B_PIN, LOW);
				delay(10);
			}
			digitalWrite(IN_B_PIN, LOW);
			digitalWrite(IN_A_PIN, HIGH);
			pre_target_pwm = -1;
		}

		if (target_pwm < 0) target_pwm = -target_pwm;
		if (target_pwm > 255) target_pwm = 255;
		if (target_pwm > POWER_LIMIT) target_pwm = POWER_LIMIT;
		analogWrite(PWM_PIN, target_pwm);
	}

	{
		pre_enc = current_enc;
		last_pwm_time = millis();
	}
}

void callbackTargetPos(const std_msgs::Int32 &pos)
{
	target_pos_mm = pos.data;
}

void callbackTargetPWM(const std_msgs::Int32 &pwm)
{
	if (control_mode == "pwm")
	{
		setPWM(int(PID_COFF*pwm.data));
	}
}

void callbackControlMode(const std_msgs::String &mode)
{
	control_mode = mode.data;
}

void callbackResetFlag(const std_msgs::Bool &flag)
{
	if (flag.data) current_enc = 0;
}

void servo()
{
	if (control_mode == "servo")
	{
		int error = target_pos_mm - current_pos_mm;
		integral=integral+(float)error*(micros()-last_calc_time)/1000000;
		float normalized_pid=Kp*error+Ki*integral+Kd*(error - last_error);
		last_error = error;
		last_calc_time = micros();
		if (-POS_TOLERANCE <= error && error <= POS_TOLERANCE && pre_enc == current_enc)
		{
			setPWM(0);
			finish_flag.data = true;
		}
		else if (pre_enc == current_enc && finish_flag.data == false)
		{
			if (millis() - last_pwm_time > 2000)
			{
				error_flag.data = true;
			}
		}
		else
		{
			setPWM(int(PID_COFF*normalized_pid));
			finish_flag.data = false;
		}

		if (error_flag.data == true)
		{
			count ++;
			if (count > 30)
			{
				count = 0;
				error_flag.data = false;
				finish_flag.data = true;
			}
		}

	}
}

void setup()
{
	//// pinMode ////
	pinMode(IN_A_PIN, OUTPUT);
	pinMode(IN_B_PIN, OUTPUT);
	pinMode(PWM_PIN, OUTPUT);
	pinMode(LED_PIN, OUTPUT);
	pinMode(ENABLE_PIN, OUTPUT);
	if (PI_LIMIT_INPUT_MODE == "INPUT_PULLUP") {pinMode(PI_LIMIT_PIN, INPUT_PULLUP);}
	else {pinMode(PI_LIMIT_PIN, INPUT);}
	// pinMode(ENC_A, INPUT);
	// pinMode(ENC_B, INPUT);

	//// write ////
	digitalWrite(IN_A_PIN, LOW);
	digitalWrite(IN_B_PIN, LOW);
	digitalWrite(LED_PIN, LOW);
	digitalWrite(ENABLE_PIN, HIGH);
	analogWrite(PWM_PIN, 0);

	//// encoder ////
	attachInterrupt(digitalPinToInterrupt(ENC_A), countEnc, RISING);

	//// nh ////
	nh.initNode();
	nh.advertise(pub_current_pos);
	nh.advertise(pub_limit_state);
	nh.advertise(pub_finish_flag);
	nh.advertise(pub_error_flag);
	nh.subscribe(sub_target_pos);
	nh.subscribe(sub_target_pwm);
	nh.subscribe(sub_control_mode);
	nh.subscribe(sub_reset_flag);

	finish_flag.data = true;
	error_flag.data = false;

	delay(1000);
}

#endif