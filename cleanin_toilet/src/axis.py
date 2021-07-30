import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Bool
from std_msgs.msg import String
import time

class AxisCommander:
	def __init__(self, axis, interrupt):
		self.axis = axis
		self.zero_adjusted_pwm = 100
		self.limit_state = False
		self.current_pos = 0.0
		self.allowable_error = 20
		self.home_pos = 0
		self.hold_pos_pwm = 0

		#### Publisher ####
		self.target_pos_pub = rospy.Publisher('/arduino_{}/target_pos'.format(axis), Int32, queue_size=10)
		self.target_pwm_pub = rospy.Publisher('/arduino_{}/target_pwm'.format(axis), Int32, queue_size=10)
		self.control_mode_pub = rospy.Publisher('/arduino_{}/control_mode'.format(axis), String, queue_size=10)
		self.reset_flag_pub = rospy.Publisher('/arduino_{}/reset_flag'.format(axis), Bool, queue_size=10)

		#### Subscriber ####
		rospy.Subscriber('/arduino_{}/current_pos'.format(axis), Int32, self.callbackCurrentPos)
		rospy.Subscriber('/arduino_{}/axis_limit_state', Bool, self.callbackLimitSwitch)

	def callbackCurrentPos(self, data):
		self.current_pos = data.data

	def callbackLimitSwitch(self, state):
		self.limit_state = state.data
	
	def setTargetPos(self, pos):
		self.control_mode_pub.publish('servo')
		self.target_pos_pub.publish(pos)
		while abs(self.current_pos - pos) > self.allowable_error:
			pass

	def setPWM(self, pwm):
		self.control_mode_pub.publish('pwm')
		self.target_pwm_pub.publish(pwm)

	def zeroAdjusted(self):
		self.setPWM(self.zero_adjusted_pwm)
		while not self.limit_state:
			pass
		self.setPWM(self.hold_pos_pwm)

		#### Don't setTargetPos ####
		self.reset_flag_pub.publish(True)
		time.sleep(1)
		self.target_pos_pub.publish(self.current_pos)
		self.reset_flag_pub.publish(False)

class AxisCommanderInterrupt(AxisCommander):
	def __init__(self, axis, interrupt):
		super().__init__(axis)

		self.interrupt = interrupt
		self.interrupt_state = False
		self.interrupt_flag = True

		rospy.Subscriber('/arduino_wall/interrupt_switch_state', Bool, self.callbackInterruptSwitch)

	def callbackInterruptSwitch(self, state):
		self.interrupt_state = state.data
		if self.interrupt_state == True and self.interrupt_flag:
			self.interrupt_flag = False
			self.doInterruptJob()
			self.interrupt_flag = True

	def doInterruptJob(self):
		#### stop servo ####
		self.setTargetPos(self.current_pos)

		#### send pos ####
		self.interrupt.getAxisPos(self.axis, self.current_pos)
		self.interrupt.checkData()
		while not self.interrupt.go_home_flag:
			pass

		#### go home pos ####
		self.setTargetPos(self.home_pos)

		#### wait press switch ####
		while self.interrupt_state:
			pass

		#### return to the position before the interruption ####
		self.setTargetPos(self.interrupt.df[0, self.axis])

	def setTargetPos(self, pos):
		self.control_mode_pub.publish('servo')
		self.target_pos_pub.publish(pos)
		while abs(self.current_pos - pos) > self.allowable_error or self.interrupt_state:
			pass