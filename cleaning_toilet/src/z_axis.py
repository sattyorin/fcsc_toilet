from axis import AxisCommander
from axis import AxisCommanderInterrupt
import pandas as pd

home_pos = 0
hold_pos_pwm = 0
zero_adjusted_pwm = 35
min_pos = -900
max_pos = 0
after_adjusted_pos = -100

zero_csv_path = '~/catkin_ws/src/fcsc_toilet/cleaning_toilet/csv/zero.csv'
zeroDF = pd.read_csv(zero_csv_path, index_col=0)

class ZAxisCommander(AxisCommander):
	def __init__(self):
		super().__init__('z')

		self.zero_adjusted_pwm = zero_adjusted_pwm
		self.home_pos = home_pos
		self.hold_pos_pwm = hold_pos_pwm
		self.seat_Z = int(zeroDF.at['seat_Z', 'pos'])
		self.floor_Z = int(zeroDF.at['floor_Z', 'pos'])
		self.min_pos = min_pos
		self.max_pos = max_pos
		self.after_adjusted_pos = after_adjusted_pos

class ZAxisCommanderInterrupt(AxisCommanderInterrupt):
	def __init__(self, interrupt):
		super().__init__('z', interrupt)

		self.zero_adjusted_pwm = zero_adjusted_pwm
		self.home_pos = home_pos
		self.hold_pos_pwm = hold_pos_pwm
		self.seat_Z = int(zeroDF.at['seat_Z', 'pos'])
		self.floor_Z = int(zeroDF.at['floor_Z', 'pos'])
		self.min_pos = min_pos
		self.max_pos = max_pos
		self.after_adjusted_pos = after_adjusted_pos