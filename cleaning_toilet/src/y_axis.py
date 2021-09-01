from axis import AxisCommander
from axis import AxisCommanderInterrupt
import pandas as pd

home_pos = 0
hold_pos_pwm = 0
zero_adjusted_pwm = -20
min_pos = 0
max_pos = 1280
after_adjusted_pos = 30

zero_csv_path = '~/catkin_ws/src/fcsc_toilet/cleaning_toilet/csv/zero.csv'
zeroDF = pd.read_csv(zero_csv_path, index_col=0)

class YAxisCommander(AxisCommander):
	def __init__(self):
		super().__init__('y')

		self.zero_adjusted_pwm = zero_adjusted_pwm
		self.home_pos = home_pos
		self.hold_pos_pwm = hold_pos_pwm
		self.seat_frontX = int(zeroDF.at['seat_frontX', 'pos'])
		self.seat_frontY = int(zeroDF.at['seat_frontY', 'pos'])
		self.min_pos = min_pos
		self.max_pos = max_pos
		self.after_adjusted_pos = after_adjusted_pos

class YAxisCommanderInterrupt(AxisCommanderInterrupt):
	def __init__(self, interrupt):
		super().__init__('y', interrupt)

		self.zero_adjusted_pwm = zero_adjusted_pwm
		self.home_pos = home_pos
		self.hold_pos_pwm = hold_pos_pwm
		self.seat_frontX = int(zeroDF.at['seat_frontX', 'pos'])
		self.seat_frontY = int(zeroDF.at['seat_frontY', 'pos'])
		self.min_pos = min_pos
		self.max_pos = max_pos
		self.after_adjusted_pos = after_adjusted_pos