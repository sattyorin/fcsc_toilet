#!/usr/bin/env python3
import rospy
from x_axis import XAxisCommanderInterrupt
from y_axis import YAxisCommanderInterrupt
from z_axis import ZAxisCommanderInterrupt
from ee import EndEfectorCommander
from ee import BarCommander
from interrupt import Interrupt
import pandas as pd
import multiprocessing as mp
import time
import csv
from pos import *

rospy.init_node('main')

#### constant ####
theta_dynamixel_id = 1
bar_dynamixel_id = 2
# interrupt_csv_path = '../csv/interrupt.csv'
interrupt_csv_path = '~/catkin_ws/src/fcsc_toilet/cleaning_toilet/csv/interrupt.csv'
script_csv_path = '../csv/script.csv'
_script_csv_path = '../csv/_script.csv'
# scriptDF = pd.read_csv(script_csv_path)
# _scriptDF = scriptDF.copy()

#### variable ####

#### instance ####
eecom = EndEfectorCommander(theta_dynamixel_id)
barcom = BarCommander(bar_dynamixel_id)
interrupt = Interrupt(interrupt_csv_path, eecom, barcom)
xaxiscom = XAxisCommanderInterrupt(interrupt)
yaxiscom = YAxisCommanderInterrupt(interrupt)
zaxiscom = ZAxisCommanderInterrupt(interrupt)

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
# 初期位置(便座左)に移動
def move_init_pos():
	print('[main::move_init_pos]')
	setcheckTargetPos(zaxiscom,Z_BENKI + 50)
	eecom.setThetaPos(ANGLE_EE_LEFT)
	time.sleep(2)
	setcheckTargetPos(xaxiscom,X_MAX)
	setcheckTargetPos(yaxiscom,Y_MIN-30)
	setcheckTargetPos(zaxiscom,Z_BENKI)

	# eecom.setThetaPos(ANGLE_EE_CENTER)
	# setcheckTargetPos(xaxiscom,X_MIN)
	# setcheckTargetPos(yaxiscom,Y_EVACUATION)
	# setcheckTargetPos(xaxiscom,X_MAX)
	# setcheckTargetPos(yaxiscom,Y_MIN-30)
	# setcheckTargetPos(zaxiscom,Z_BENKI)
	# eecom.setThetaPos(ANGLE_EE_LEFT)

# スタートコマンド待機
def wait_start_command():
	print('[main::wait_start_command]')
	input("Press Enter...")
# 便器上清掃
def sweep_benki_top():
	print('[main::sweep_benki_top]')
	eecom.setThetaPos(ANGLE_EE_CENTER)
	setcheckTargetPos(zaxiscom,Z_MAX)
	setcheckTargetPos(yaxiscom,Y_EVACUATION)
	setcheckTargetPos(xaxiscom,X_BENKI_FRONT-80)
	setcheckTargetPos(yaxiscom,Y_BENKI_TOP_MIN)
	setcheckTargetPos(zaxiscom,Z_BENKI)
	setcheckTargetPos(yaxiscom,Y_EVACUATION)
	setcheckTargetPos(zaxiscom,Z_MAX)
	setcheckTargetPos(xaxiscom,X_BENKI_FRONT+80)
	setcheckTargetPos(yaxiscom,Y_BENKI_TOP_MIN)
	setcheckTargetPos(zaxiscom,Z_BENKI)
	setcheckTargetPos(yaxiscom,Y_EVACUATION)
	setcheckTargetPos(zaxiscom,Z_MAX)
	# setcheckTargetPos(xaxiscom,X_BENKI_FRONT)
	# setcheckTargetPos(yaxiscom,Y_BENKI_TOP_MIN+200)
	# setcheckTargetPos(zaxiscom,Z_BENKI)
	# setcheckTargetPos(yaxiscom,Y_EVACUATION)
	# setcheckTargetPos(zaxiscom,Z_MAX)

# エンドエフェクタ安全確保
def sweep_laege_gomi():
	print('[main::sweep_laege_gomi]')
	eecom.setThetaPos(ANGLE_EE_CENTER)
	setcheckTargetPos(xaxiscom,X_MIN)
	setcheckTargetPos(yaxiscom,Y_MAX)
	barcom.setThetaPos(BAR_DOWN_POS)
	time.sleep(1)
	setcheckTargetPos(yaxiscom,Y_MIN+400)
	barcom.setThetaPos(BAR_HOME_POS)
	setcheckTargetPos(yaxiscom,Y_EVACUATION)
	
# 便座正面床清掃
def sweep_benki_frontside_floor_first():
	print('[main::sweep_benki_frontside_floor_first]')
	setcheckTargetPos(yaxiscom,Y_EVACUATION)
	# eecom.setThetaPos(ANGLE_EE_LEFT)
	setcheckTargetPos(xaxiscom,X_FRONT_FLOOR_MIN)
	setcheckTargetPos(yaxiscom,Y_BENKI_FRONT_EE_SIDE)
	eecom.setVacuumState(True)	
	setcheckTargetPos(zaxiscom,Z_FLOOR+400)
	eecom.setThetaPos(ANGLE_EE_LEFT)
	setcheckTargetPos(zaxiscom,Z_FLOOR)
	setcheckTargetPos(xaxiscom,X_FRONT_FLOOR_MAX)
	eecom.setVacuumState(False)
	setcheckTargetPos(zaxiscom,Z_FLOOR_MOVING)
	setcheckTargetPos(yaxiscom,Y_BENKI_FRONT_EE_SIDE+150)
	setcheckTargetPos(xaxiscom,X_FRONT_FLOOR_MIN)
	eecom.setVacuumState(True)
	setcheckTargetPos(zaxiscom,Z_FLOOR)
	setcheckTargetPos(xaxiscom,X_FRONT_FLOOR_MAX)
	eecom.setVacuumState(False)
	setcheckTargetPos(zaxiscom,Z_FLOOR_MOVING)

def sweep_benki_frontside_floor_second():
	print('[main::sweep_benki_frontside_floor_second]')
	setcheckTargetPos(yaxiscom,Y_EVACUATION)
	# eecom.setThetaPos(ANGLE_EE_LEFT)
	setcheckTargetPos(xaxiscom,X_FRONT_FLOOR_MAX)
	eecom.setThetaPos(ANGLE_EE_RIGHT)
	time.sleep(3)
	setcheckTargetPos(zaxiscom,Z_FLOOR+300)
	setcheckTargetPos(yaxiscom,Y_BENKI_FRONT_EE_SIDE_REVERSE)
	eecom.setVacuumState(True)	
	setcheckTargetPos(zaxiscom,Z_FLOOR)
	setcheckTargetPos(xaxiscom,X_FRONT_FLOOR_MIN)
	eecom.setVacuumState(False)
	setcheckTargetPos(zaxiscom,Z_FLOOR_MOVING)
	
	# setcheckTargetPos(yaxiscom,Y_EVACUATION)
	# setcheckTargetPos(xaxiscom,X_FRONT_FLOOR_MAX)
	# setcheckTargetPos(zaxiscom,Z_FLOOR+300)
	# setcheckTargetPos(yaxiscom,Y_BENKI_FRONT_EE_SIDE_REVERSE)
	# eecom.setVacuumState(True)	
	# setcheckTargetPos(zaxiscom,Z_FLOOR)
	# setcheckTargetPos(xaxiscom,X_FRONT_FLOOR_MIN)
	# eecom.setVacuumState(False)
	# setcheckTargetPos(zaxiscom,Z_FLOOR_MOVING)


# 便座前面清掃
def sweep_benki_frontside():
	print('[main::sweep_benki_frontside]')
	setcheckTargetPos(yaxiscom,Y_BENKI_FRONT_EE_SIDE+40)
	eecom.setThetaPos(ANGLE_EE_LEFT)
	setcheckTargetPos(xaxiscom,X_BENKI_FRONT)
	setcheckTargetPos(zaxiscom,Z_FLOOR+10)
	X_HUKI_DIST=50
	Y_NIGE=20
	setcheckTargetPos(yaxiscom,Y_BENKI_FRONT_EE_SIDE-40)
	setcheckTargetPos(zaxiscom,Z_FLOOR+100)
	setcheckTargetPos(yaxiscom,Y_BENKI_FRONT_EE_SIDE-30)
	setcheckTargetPos(zaxiscom,Z_FLOOR+200)
	setcheckTargetPos(yaxiscom,Y_BENKI_FRONT_EE_SIDE-10)
	setcheckTargetPos(zaxiscom,Z_FLOOR+300)
	setcheckTargetPos(yaxiscom,Y_BENKI_FRONT_EE_SIDE+10)
	setcheckTargetPos(zaxiscom,Z_FLOOR+400)
	setcheckTargetPos(yaxiscom,Y_BENKI_FRONT_EE_SIDE+30)
	setcheckTargetPos(zaxiscom,Z_FLOOR+600)
	setcheckTargetPos(yaxiscom,Y_EVACUATION)

def sweep_benki_rightside_floor():
	#right side of benki
	print('[main::sweepTheFloor1]')
	eecom.setThetaPos(ANGLE_EE_BACK)
	setcheckTargetPos(yaxiscom,Y_MAX)
	setcheckTargetPos(xaxiscom,X_MIN)
	eecom.setVacuumState(True)
	setcheckTargetPos(zaxiscom,Z_FLOOR)
	setcheckTargetPos(yaxiscom,Y_MIN+100)
	eecom.setVacuumState(False)
	setcheckTargetPos(zaxiscom,Z_FLOOR_MOVING)
	setcheckTargetPos(yaxiscom,Y_MAX)
	setcheckTargetPos(xaxiscom,X_BENKI_RIGHT_SIDE)
	setcheckTargetPos(zaxiscom,Z_FLOOR)
	eecom.setVacuumState(True)	
	setcheckTargetPos(yaxiscom,Y_MIN+100)
	setcheckTargetPos(zaxiscom,Z_FLOOR_MOVING)
	eecom.setVacuumState(False)


def move_benki_right2left():
	print('[main::move_benki_right2left]')
	setcheckTargetPos(zaxiscom,Z_FLOOR_MOVING)
	# input("Waiting...")
	setcheckTargetPos(yaxiscom,Y_EVACUATION)
	# input("Waiting...")
	setcheckTargetPos(xaxiscom,X_BENKI_LEFT_SIDE)
	# input("Waiting...")

def sweep_benki_leftside_floor():
	#left side of benki
	print('[main::sweepTheFloor1]')
	setcheckTargetPos(yaxiscom,Y_EVACUATION)
	eecom.setThetaPos(ANGLE_EE_CENTER)
	setcheckTargetPos(xaxiscom,X_MAX)
	setcheckTargetPos(yaxiscom,Y_MIN)
	setcheckTargetPos(zaxiscom,Z_FLOOR+100)
	setcheckTargetPos(xaxiscom,X_BENKI_LEFT_SIDE)
	eecom.setVacuumState(True)
	setcheckTargetPos(zaxiscom,Z_FLOOR)
	setcheckTargetPos(yaxiscom,Y_BENKI_SIDE)
	eecom.setVacuumState(False)
	setcheckTargetPos(zaxiscom,Z_FLOOR_MOVING)
	setcheckTargetPos(yaxiscom,Y_MIN)
	setcheckTargetPos(xaxiscom,X_MAX)
	eecom.setVacuumState(True)
	setcheckTargetPos(zaxiscom,Z_FLOOR)
	setcheckTargetPos(yaxiscom,Y_BENKI_SIDE)
	eecom.setVacuumState(False)
	setcheckTargetPos(zaxiscom,Z_FLOOR_MOVING)

# メインフロア清掃
def sweep_benki_frontside_floor():
	print('[main::sweep_benki_frontside_floor]')
	eecom.setThetaPos(ANGLE_EE_LEFT)
	setcheckTargetPos(yaxiscom,Y_EVACUATION)
	# eecom.setThetaPos(ANGLE_EE_LEFT)
	setcheckTargetPos(xaxiscom,X_MIN)
	target_Y=Y_MAX
	while(target_Y>Y_BENKI_FRONT_EE_SIDE):
		setcheckTargetPos(yaxiscom,target_Y)
		eecom.setVacuumState(True)
		# eecom.setVacuumState(False)
		setcheckTargetPos(zaxiscom,Z_FLOOR)
		setcheckTargetPos(xaxiscom,X_MAX-80)
		# eecom.setVacuumState(True)
		setcheckTargetPos(zaxiscom,Z_FLOOR_MOVING)
		eecom.setVacuumState(False)
		setcheckTargetPos(xaxiscom,X_MIN)
		target_Y -=150
	setcheckTargetPos(yaxiscom,Y_BENKI_FRONT_EE_SIDE)
	eecom.setVacuumState(True)
	# eecom.setVacuumState(False)
	setcheckTargetPos(zaxiscom,Z_FLOOR)
	setcheckTargetPos(xaxiscom,X_MAX-80)
	eecom.setVacuumState(False)
	setcheckTargetPos(zaxiscom,Z_FLOOR_MOVING)
	setcheckTargetPos(xaxiscom,X_MIN)
def sweep_benki_leftside_floor_again():
	print('[main::sweep_benki_leftside_floor_again]')
	setcheckTargetPos(yaxiscom,Y_EVACUATION)
	eecom.setThetaPos(ANGLE_EE_CENTER)
	setcheckTargetPos(xaxiscom,X_MAX)
	setcheckTargetPos(yaxiscom,Y_MIN)
	eecom.setVacuumState(True)
	setcheckTargetPos(zaxiscom,Z_FLOOR)
	setcheckTargetPos(yaxiscom,Y_MAX)
	setcheckTargetPos(zaxiscom,Z_FLOOR_MOVING)
	eecom.setVacuumState(False)


# 初期位置に戻る
def move_finish_pos():
	print('[main::move_finish_pos]')
	setcheckTargetPos(zaxiscom,Z_FLOOR_MOVING)
	setcheckTargetPos(yaxiscom,Y_EVACUATION)
	eecom.setThetaPos(ANGLE_EE_CENTER)
	setcheckTargetPos(xaxiscom,X_MAX)
	setcheckTargetPos(yaxiscom,Y_MIN-30)
	eecom.setThetaPos(ANGLE_EE_LEFT)
	time.sleep(3)
	setcheckTargetPos(xaxiscom,X_BENKI_FRONT)

def getAllState():
	print('[main::getAllState]')

def doFunc(i):
	eval(i)()
	_scriptDF.drop(0, axis=0)
	_scriptDF.to_csv(_script_csv_path)

def setcheckTargetPos(commander, pos):
	if commander.setTargetPos(pos) == False:
		# commander.setTargetPos(pos)
		setcheckTargetPos(commander, pos)
	time.sleep(0.8)
	# input("Press enter to next")

def main():
	print('main')
	barcom.setThetaPos(BAR_HOME_POS)
	time.sleep(1)
	zaxiscom.zeroAdjusted()
	eecom.setThetaPos(ANGLE_EE_CENTER)	
	xaxiscom.zeroAdjusted()
	yaxiscom.zeroAdjusted()
	# 初期位置(便座左)に移動
	move_init_pos()
	# input("Waiting...")
	# # スタートコマンド待機
	wait_start_command()
	# input("Waiting...")
	# # 便器上清掃
	sweep_benki_top()
	# input("Waiting...")
	# エンドエフェクタ安全確保
	sweep_laege_gomi()
	# input("Waiting...")
	# 便座正面床清掃
	sweep_benki_frontside_floor_first()
	# input("Waiting...")
	sweep_benki_frontside_floor_second()
	# 便座前面清掃
	sweep_benki_frontside()
	# input("Waiting...")
	# exit()
	sweep_benki_leftside_floor()
	# input("Waiting...")
	# 便座右側面清掃
	sweep_benki_rightside_floor()
	# input("Waiting...")
	# メインフロア清掃
	sweep_benki_frontside_floor()
	# input("Waiting...")
	sweep_benki_leftside_floor_again()
	# 初期位置に戻る
	move_finish_pos()
	# input("Waiting...")
	# for i in scriptDF.index:
	# 	doFunc(scriptDF.at[i, 'func'])

if __name__ == "__main__":
	main()