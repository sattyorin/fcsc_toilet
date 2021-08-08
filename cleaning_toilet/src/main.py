#!/usr/bin/env python3
from x_axis import XAxisCommanderInterrupt
from y_axis import YAxisCommanderInterrupt
from z_axis import ZAxisCommanderInterrupt
from ee import EndEfectorCommander
from interrupt import Interrupt
import pandas as pd
import multiprocessing as mp
import time
import csv

#### constant ####
theta_dynamixel_id = 1
karcher_dynamixel_id = 2
interrupt_csv_path = '../csv/interrupt.csv'
script_csv_path = '../csv/script.csv'
_script_csv_path = '../csv/_script.csv'
scriptDF = pd.read_csv(script_csv_path)
_scriptDF = scriptDF.copy()

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

def sweepTheFloor1():
	print('[main::sweepTheFloor1]')
	xaxiscom.setTargetPos(10)
	eecom.setThetaPos(20)
	eecom.setKarcherAngle(-10)

def sweepTheFloor2():
	print('[main::sweepTheFloor2]')
	xaxiscom.setTargetPos(10)
	eecom.setThetaPos(20)
	eecom.setKarcherAngle(-10)

def sweepTheFloor3():
	print('[main::sweepTheFloor3]')
	xaxiscom.setTargetPos(10)
	eecom.setThetaPos(20)
	eecom.setKarcherAngle(-10)

def karcherTheToiletSeat1():
	print('[main::karcherTheToiletSeat1]')
	zaxiscom.setTargetPos(zaxiscom.seat_pos)
	eecom.setKarcherAngle(10)

def karcherTheFloor1():
	print('[main::karcherTheFloor1]')

def getAllState():
	print('[main::getAllState]')

def doFunc(i):
	eval(i)()
	_scriptDF.drop(0, axis=0)
	_scriptDF.to_csv(_script_csv_path)

def main():
	print('main')
	for i in scriptDF.index:
		doFunc(scriptDF.at[i, 'func'])

if __name__ == "__main__":
	main()