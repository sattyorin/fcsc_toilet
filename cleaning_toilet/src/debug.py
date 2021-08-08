#!/usr/bin/env python3
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

zaxiscom = ZAxisCommander()

time.sleep(3)

# zaxiscom.zeroAdjusted()

zaxiscom.setTargetPos(20)

time.sleep(3)

zaxiscom.setTargetPos(10)

time.sleep(3)

zaxiscom.setTargetPos(50)

time.sleep(3)

zaxiscom.setTargetPos(0)