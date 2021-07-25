from axis import AxisCommander
import pandas as pd

class ZAxisCommander(AxisCommander):
	def __init__(self, interrupt):
		super().__init__('z', interrupt)

		zero_csv_path = '../csv/zero.csv'
		zeroDF = pd.read_csv(zero_csv_path, index_col=0)

		self.home_pos = 0
		self.hold_pos_pwm = 0
		self.seat_pos = int(zeroDF.at['seatZ', 'pos'])