#!/usr/bin/env python3
import rospy
from x_axis import XAxisCommanderInterrupt
from y_axis import YAxisCommanderInterrupt
from z_axis import ZAxisCommanderInterrupt
from ee import EndEfectorCommander
from interrupt import Interrupt
import pandas as pd
import multiprocessing as mp
import time
import csv
from pos import *

rospy.init_node('main')

#### constant ####
theta_dynamixel_id = 1
karcher_dynamixel_id = 2
# interrupt_csv_path = '../csv/interrupt.csv'
interrupt_csv_path = '~/catkin_ws/src/fcsc_toilet/cleaning_toilet/csv/interrupt.csv'
script_csv_path = '../csv/script.csv'
_script_csv_path = '../csv/_script.csv'
# scriptDF = pd.read_csv(script_csv_path)
# _scriptDF = scriptDF.copy()

#### variable ####

#### instance ####
interrupt = Interrupt(interrupt_csv_path)
xaxiscom = XAxisCommanderInterrupt(interrupt)
yaxiscom = YAxisCommanderInterrupt(interrupt)
zaxiscom = ZAxisCommanderInterrupt(interrupt)
eecom = EndEfectorCommander(theta_dynamixel_id, karcher_dynamixel_id)

time.sleep(5) # wait for starting ros

def zeroAdjusted():
	print('[main::zeroAdjusted]')
	px = mp.Process(target=xaxiscom.zeroAdjusted)
	py = mp.Process(target=yaxiscom.zeroAdjusted)
	pz = mp.Process(target=zaxiscom.zeroAdjusted)

	px.start()
	py.start()
	pz.start()

	px.join()
	py.join()
	pz.join()

def adjustZTheToiletSeat():
	print('[main::adjustZTheToiletSeat]')

	#### go on the seat ####
	xaxiscom.setTargetPos(10)
	yaxiscom.setTargetPos(10)
	zaxiscom.setTargetPos(10)

	#### adjust z ####
	# while not eecom.floor_switch:
	# 	zaxiscom.setPWM(10)
	# zaxiscom.setPWM(zaxiscom.hold_pos_pwm)
	# time.sleep(1)
	# zaxiscom.seat_pos = zaxiscom.current_pos
def sweep_benki_top():
	print('[main::sweep benki top]')

def sweep_benki_rightside_floor():
	#right side of benki
	print('[main::sweepTheFloor1]')
	xaxiscom.setTargetPos(X_MIN)
	yaxiscom.setTargetPos(Y_MIN)
	eecom.setVacuumState(True)
	eecom.setKarcherAngle(-10)
	zaxiscom.setTargetPos(Z_FLOOR)
	yaxiscom.setTargetPos(Y_BENKI_SIDE)
	zaxiscom.setTargetPos(Z_FLOOR_MOVING)

	xaxiscom.setTargetPos(X_BENKI_RIGHT_SIDE)
	yaxiscom.setTargetPos(Y_MIN)
	eecom.setVacuumState(True)
	eecom.setKarcherAngle(-10)
	zaxiscom.setTargetPos(Z_FLOOR)
	yaxiscom.setTargetPos(Y_BENKI_SIDE)
	zaxiscom.setTargetPos(Z_FLOOR_MOVING)

def move_benki_right2left():
	print('[main::move_benki_right2left]')
	zaxiscom.setTargetPos(Z_FLOOR_MOVING)
	yaxiscom.setTargetPos(Y_EVACUATION)
	xaxiscom.setTargetPos(X_BENKI_LEFT_SIDE)

def sweep_benki_leftside_floor():
	#left side of benki
	print('[main::sweepTheFloor1]')
	xaxiscom.setTargetPos(X_BENKI_LEFT_SIDE)
	yaxiscom.setTargetPos(Y_MIN)
	eecom.setVacuumState(True)
	eecom.setKarcherAngle(-10)
	zaxiscom.setTargetPos(Z_FLOOR)
	yaxiscom.setTargetPos(Y_BENKI_SIDE)
	zaxiscom.setTargetPos(Z_FLOOR_MOVING)
	
	xaxiscom.setTargetPos(X_MAX)
	yaxiscom.setTargetPos(Y_MIN)
	eecom.setVacuumState(True)
	zaxiscom.setTargetPos(Z_FLOOR)
	yaxiscom.setTargetPos(Y_BENKI_SIDE)
	zaxiscom.setTargetPos(Z_FLOOR_MOVING)

def move_benki_left2front():
	print('[main::move_benki_left2front]')
	zaxiscom.setTargetPos(Z_FLOOR_MOVING)
	yaxiscom.setTargetPos(Y_EVACUATION)
	xaxiscom.setTargetPos(X_BENKI_LEFT_SIDE)

def	sweep_benki_frontside_floor():
	print('[main::sweep_benki_frontside_floor]')

def	sweep_benki_frontside():
	print('[main::sweep_benki_frontside]')

def getAllState():
	print('[main::getAllState]')

def doFunc(i):
	eval(i)()
	_scriptDF.drop(0, axis=0)
	_scriptDF.to_csv(_script_csv_path)

def setcheckTargetPos(commander, pos):
	if commander.setTargetPos(pos) == False:
		commander.setTargetPos(pos)

def main():
	print('main')

	# eecom.setThetaPos(2050)

	eecom.setVacuumState(True)
	time.sleep(2)
	eecom.setVacuumState(False)


	# zaxiscom.zeroAdjusted()
	# yaxiscom.zeroAdjusted()
	# xaxiscom.zeroAdjusted()

	# setcheckTargetPos(xaxiscom, 300)
	# setcheckTargetPos(yaxiscom, 300)
	# zaxiscom.setTargetPos(-100)

	# xaxiscom._setTargetPos(100)
	# yaxiscom.setTargetPos(100)
	# zaxiscom.setTargetPos(-100)

	# zeroAdjusted()
	# sweep_benki_top()
	# sweep_benki_rightside_floor()
	# move_benki_right2left()
	# sweep_benki_leftside_floor()
	# move_benki_left2front()
	# sweep_benki_frontside_floor()
	# sweep_benki_frontside()
	# zeroAdjusted()
	

	# for i in scriptDF.index:
	# 	doFunc(scriptDF.at[i, 'func'])

if __name__ == "__main__":
	main()