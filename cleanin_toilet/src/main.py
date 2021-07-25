from. import XAxisCommander
from. import YAxisCommander
from. import ZAxisCommander
from. import EndEfectorCommander
from. import Interrupt
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
zero_csv_path = '../csv/zero.csv'
scriptDF = pd.read_csv(script_csv_path)
_scriptDF = scriptDF.copy()

#### variable ####

#### instance ####
interrupt = Interrupt()
xaxiscom = XAxisCommander(interrupt)
yaxiscom = YAxisCommander(interrupt)
zaxiscom = ZAxisCommander(interrupt)
eecom = EndEfectorCommander(theta_dynamixel_id, karcher_dynamixel_id)

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
	while not eecom.floor_switch:
		zaxiscom.setPWM(10)
	zaxiscom.setPWM(zaxiscom.hold_pos_pwm)
	time.sleep(1)
	zaxiscom.seat_pos = zaxiscom.current_pos

	#### write seat z pos ####
	with open(zero_csv_path, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(['', 'pos'])
		writer.writerow(['seatZ', zaxiscom.seat_pos])

def sweepTheFloor1():
	print('[main::sweepTheFloor1]')
	xaxiscom.setTargetPos(10)
	eecom.setThetaPos(20)
	eecom.setKarcherPos(-10)

def sweepTheFloor2():
	print('[main::sweepTheFloor2]')
	xaxiscom.setTargetPos(10)
	eecom.setThetaPos(20)
	eecom.setKarcherPos(-10)

def sweepTheFloor3():
	print('[main::sweepTheFloor3]')
	xaxiscom.setTargetPos(10)
	eecom.setThetaPos(20)
	eecom.setKarcherPos(-10)

def karcherTheToiletSeat1():
	print('[main::karcherTheToiletSeat1]')
	zaxiscom.setTargetPos(zaxiscom.seat_pos)
	eecom.setKarcherPos(10)

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
	for i in scriptDF:
		doFunc(scriptDF[i, 'func'])

if __name__ == "__main__":
	main()