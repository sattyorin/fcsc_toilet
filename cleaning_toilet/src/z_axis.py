from axis import AxisCommander
from axis import AxisCommanderInterrupt
import pandas as pd

home_pos = 0
hold_pos_pwm = 0

zero_csv_path = '~/catkin_ws/src/fcsc_toilet/cleaning_toilet/csv/zero.csv'
zeroDF = pd.read_csv(zero_csv_path, index_col=0)

class ZAxisCommander(AxisCommander):
	def __init__(self):
		super().__init__('z')

		self.home_pos = home_pos
		self.hold_pos_pwm = hold_pos_pwm
		self.seat_Z = int(zeroDF.at['seat_Z', 'pos'])
		self.floor_Z = int(zeroDF.at['floor_Z', 'pos'])

class ZAxisCommanderInterrupt(AxisCommanderInterrupt):
	def __init__(self, interrupt):
		super().__init__('z', interrupt)

		self.home_pos = home_pos
		self.hold_pos_pwm = hold_pos_pwm
		self.seat_Z = int(zeroDF.at['seat_Z', 'pos'])
		self.floor_Z = int(zeroDF.at['floor_Z', 'pos'])