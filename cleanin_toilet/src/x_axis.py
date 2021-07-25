from. import AxisCommander

class XAxisCommander(AxisCommander):
	def __init__(self, interrupt):
		super().__init__('x', interrupt)

		self.home_pos = 0
		self.hold_pos_pwm = 0