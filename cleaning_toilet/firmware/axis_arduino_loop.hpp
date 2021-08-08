#ifndef axis_arduino_loop_hpp_
#define axis_arduino_loop_hpp_

void loop()
{
	publishCurrentPos();
	publishLimitState();
	publishFinishFlag();
	servo();
	nh.spinOnce();
}

#endif