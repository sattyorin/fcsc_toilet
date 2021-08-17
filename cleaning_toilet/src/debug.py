#!/usr/bin/env python3
import rospy
from x_axis import XAxisCommander
from y_axis import YAxisCommander
from z_axis import ZAxisCommander
from x_axis import XAxisCommanderInterrupt
from y_axis import YAxisCommanderInterrupt
from z_axis import ZAxisCommanderInterrupt
from ee import EndEfectorCommander
from interrupt import Interrupt
import pandas as pd
import multiprocessing as mp
import time


if __name__ == '__main__':

	rospy.init_node('main')

	xaxiscom = XAxisCommander()
	yaxiscom = YAxisCommander()
	zaxiscom = ZAxisCommander()

	time.sleep(3)

	zaxiscom.zeroAdjusted()
	xaxiscom.zeroAdjusted()
	yaxiscom.zeroAdjusted()

	# time.sleep(2)
	# zaxiscom.setTargetPos(0)

	# time.sleep(2)

	# xaxiscom.setTargetPos(100)
	# time.sleep(2)
	# xaxiscom.setTargetPos(-50)
	# time.sleep(2)
	# xaxiscom.setTargetPos(100)
	# time.sleep(2)
	# xaxiscom.setTargetPos(0)
	# time.sleep(2)

	# xaxiscom.setTargetPos(-200)

	# time.sleep(2)
