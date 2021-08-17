import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Bool
from std_msgs.msg import String
import time

class AxisCommander:
	def __init__(self, axis):
		self.axis = axis
		self.limit_state = False
		self.finish_flag = False
		self.error_flag = False
		self.current_pos = 0.0
		self.home_pos = 0
		self.hold_pos_pwm = 0

		# rospy.init_node('axis_{}'.format(axis))
		self.r = rospy.Rate(100) 

		#### Publisher ####
		self.target_pos_pub = rospy.Publisher('/arduino_{}/target_pos'.format(axis), Int32, queue_size=10)
		self.target_pwm_pub = rospy.Publisher('/arduino_{}/target_pwm'.format(axis), Int32, queue_size=10)
		self.control_mode_pub = rospy.Publisher('/arduino_{}/control_mode'.format(axis), String, queue_size=10)
		self.reset_flag_pub = rospy.Publisher('/arduino_{}/reset_flag'.format(axis), Bool, queue_size=10)

		#### Subscriber ####
		rospy.Subscriber('/arduino_{}/current_pos'.format(axis), Int32, self.callbackCurrentPos)
		rospy.Subscriber('/arduino_{}/axis_limit_state'.format(axis), Bool, self.callbackLimitSwitch)
		rospy.Subscriber('/arduino_{}/finish_flag'.format(axis), Bool, self.callbackFinishFlag)
		rospy.Subscriber('/arduino_{}/error_flag'.format(axis), Bool, self.callbackErrorFlag)

	def callbackCurrentPos(self, data):
		self.current_pos = data.data

	def callbackLimitSwitch(self, state):
		self.limit_state = state.data

	def callbackFinishFlag(self, state):
		self.finish_flag = state.data

	def callbackErrorFlag(self, state):
		self.error_flag = state.data

	def checkPos(self, pos):
		if self.min_pos > pos or pos > self.max_pos:
			print('Do not broke the machine!!')
			exit()

	def publishTopic(self, publisher, val):
		for i in range(15):
			publisher.publish(val)
			self.r.sleep()
	
	def setTargetPos(self, pos):
		self.checkPos(pos)
		self.publishTopic(self.control_mode_pub, 'servo')
		while self.finish_flag:
			self.publishTopic(self.target_pos_pub, pos)
		while not self.finish_flag:
			if self.error_flag:
				break

	def setPWM(self, pwm):
		self.publishTopic(self.control_mode_pub, 'pwm')
		self.publishTopic(self.target_pwm_pub, pwm)

	def zeroAdjusted(self):
		self.setPWM(self.zero_adjusted_pwm)
		while not self.limit_state:
			pass
		self.setPWM(self.hold_pos_pwm)

		self.publishTopic(self.reset_flag_pub, True)
		time.sleep(1)
		self.publishTopic(self.reset_flag_pub, False)
		self.setTargetPos(self.after_adjusted_pos)

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
		self.publishTopic(self.control_mode_pub, 'servo')
		self.publishTopic(self.target_pos_pub, pos)
		while abs(self.current_pos - pos) > self.allowable_error or self.interrupt_state:
			pass