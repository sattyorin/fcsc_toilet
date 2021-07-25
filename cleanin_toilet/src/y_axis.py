from. import AxisCommander

class YAxisCommander(AxisCommander):
	def __init__(self, interrupt):
		super().__init__('y', interrupt)

		self.home_pos = 0
		self.hold_pos_pwm = 0