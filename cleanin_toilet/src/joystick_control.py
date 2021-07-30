#!/usr/bin/env python
# coding:utf-8
import rospy
from sensor_msgs.msg import Joy
from x_axis import XAxisCommander
from y_axis import YAxisCommander
from z_axis import ZAxisCommander
from ee import EndEfectorCommander
import csv

#### constant ####
theta_dynamixel_id = 1
karcher_dynamixel_id = 2
pwm = 10
zero_csv_path = '../csv/zero.csv'

#### variable #####
select = 0
flag_select = False
flag_ee = False

#### instance ####
xaxiscom = XAxisCommander()
yaxiscom = YAxisCommander()
zaxiscom = ZAxisCommander()
eecom = EndEfectorCommander(theta_dynamixel_id, karcher_dynamixel_id)

def writeCSV():

	#### write seat z pos ####
	with open(zero_csv_path, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(['', 'pos'])
		writer.writerow(['seat_left', xaxiscom.seat_left])
		writer.writerow(['seat_right', xaxiscom.seat_right])
		writer.writerow(['seat_frontX', yaxiscom.seat_frontX])
		writer.writerow(['seat_frontY', yaxiscom.seat_frontY])
		writer.writerow(['seat_Z', zaxiscom.seat_Z])
		writer.writerow(['floor_Z', zaxiscom.floor_Z])

def selectPos():
	if select == 5:
		select = 0
	else:
		select += 1
	
	if select == 0:
		print('seat_left')
	elif select == 1:
		print('seat_right')
	elif select == 2:
		print('seat_frontX')
	elif select == 3:
		print('seat_frontY')
	elif select == 4:
		print('seat_Z')
	elif select == 5:
		print('floor_Z')


def callback(data):

	#### move ####
	xaxiscom.setPWM(data.buttons[1] * pwm)
	xaxiscom.setPWM(data.buttons[3] * -pwm)
	yaxiscom.setPWM(data.buttons[0] * pwm)
	yaxiscom.setPWM(data.buttons[2] * -pwm)
	xaxiscom.setPWM(data.buttons[5] * pwm)
	xaxiscom.setPWM(data.buttons[7] * -pwm)

	#### ee ####
	if data.buttons[11] == 1:
		flag_ee = not flag_ee
		if flag_ee:
			eecom.setThetaPos(1024)
		else:
			eecom.setThetaPos(0)

	#### select pos ####
	if data.buttons[8] == 1 and flag_select == True:
		flag_select == False
		selectPos()

	elif data.buttons[8] == 0:
		flag_select == True

	#### save pos ####
	if data.buttons[6] == 1:

		if select == 0:
			xaxiscom.seat_left = xaxiscom.current_pos
			print('seat_left: {}'.format(xaxiscom.seat_left))
		elif select == 1:
			xaxiscom.seat_right = xaxiscom.current_pos
			print('seat_right: {}'.format(xaxiscom.seat_right))
		elif select == 2:
			yaxiscom.seat_frontX = yaxiscom.current_pos
			print('seat_frontX: {}'.format(yaxiscom.seat_frontX))
		elif select == 3:
			yaxiscom.seat_frontY = yaxiscom.current_pos
			print('seat_frontY: {}'.format(yaxiscom.seat_frontY))
		elif select == 4:
			zaxiscom.seat_Z = zaxiscom.current_pos
			print('seat_Z: {}'.format(zaxiscom.seat_Z))
		elif select == 5:
			zaxiscom.floor_Z = zaxiscom.current_pos
			print('floor_Z: {}'.format(zaxiscom.floor_Z))

		selectPos()

	if data.buttons[9] == 1:
		writeCSV()


def main():
	rospy.init_node('joystick_control')
	rospy.Subscriber("joy", Joy, callback)

	r=rospy.Rate(30)
	while not rospy.is_shutdown():
		r.sleep()

if __name__ == '__main__':
	main()