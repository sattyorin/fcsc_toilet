import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Bool
from std_msgs.msg import String
import time
import copy

class AxisCommander:
	def __init__(self, axis):
		self.axis = axis
		self.limit_state = False
		self.finish_flag = False
		self.error_flag = False
		self.current_pos = 0.0
		self.home_pos = 0
		self.hold_pos_pwm = 0
		self.same_pos_tolerance = 10

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
			print('Do not broke the machine!! Target->',pos)
			exit()

	def publishTopic(self, publisher, val):
		for i in range(6):
			publisher.publish(val)
			self.r.sleep()
		
	def publishTopicOnece(self, publisher, val):
		publisher.publish(val)
		self.r.sleep()
	
	def setTargetPos(self, pos):
		print('[{}AxisCommander::setTargetPos]'.format(self.axis))
		self.checkPos(pos)
		self.publishTopic(self.target_pos_pub, self.current_pos) #stop servo
		self.publishTopic(self.control_mode_pub, 'servo')
		if not(pos-self.same_pos_tolerance < self.current_pos < pos+self.same_pos_tolerance):
			while self.finish_flag:
				self.publishTopic(self.target_pos_pub, pos)
		while not self.finish_flag:
			if self.error_flag:
				break

	def setPWM(self, pwm):
		self.publishTopic(self.control_mode_pub, 'pwm')
		self.publishTopicOnece(self.target_pwm_pub, pwm)

	def zeroAdjusted(self):
		print('[{}AxisCommander::zeroAdjusted]'.format(self.axis))
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
		print('[{}AxisCommanderInterrupt::__init__]'.format(self.axis))

		self.interrupt = interrupt
		self.interrupt_state = False
		self.interrupt_flag = False
		self.wait_flag = False
		self.interrupt_count = 0
		self.check_flag = False

		rospy.Subscriber('/arduino_wall/interrupt_switch_state', Bool, self.callbackInterruptSwitch)

	def callbackInterruptSwitch(self, state):
		self.interrupt_state = state.data
		if self.interrupt_state or self.interrupt_flag == True:
			if self.interrupt_count > 5:
				self.interrupt_flag = True
				self.doInterruptJob()
			else:
				self.interrupt_count += 1

	def doInterruptJob(self):

		if self.interrupt.go_home_flag == False and self.wait_flag == False:
			#### stop servo ####
			self._setTargetPos(self.current_pos)
			self.interrupt.setCurrentPos(self.axis, self.current_pos)

			#### save pos ####
			self.interrupt.getAxisPos(self.axis, self.current_pos)
			self.interrupt.checkData()

		elif self.interrupt.go_home_flag and self.wait_flag == False:
			#### go home pos ####
			if self.interrupt.got_home_flag == False:
				if self.interrupt.getHomePos(self.axis):
					print('[{}AxisCommanderInterrupt::doInterruptJob] go {}'.format(self.axis, self.interrupt.home_pos))
					self._setTargetPos(self.interrupt.home_pos)
					self.interrupt.gotHomePos()
			else:
				self.wait_flag = True
				print('[{}AxisCommanderInterrupt::doInterruptJob] got home'.format(self.axis))

		elif self.wait_flag and self.interrupt_state:
			#### wait press switch ####
			pass

		elif self.wait_flag and self.interrupt_state == False:
			#### return to the position before the interruption ####
			if self.interrupt.got_interruption_pos_flag == False:
				if self.interrupt.getInterruptionPos(self.axis):
					self._setTargetPos(self.interrupt.home_pos)
					self.interrupt.gotInterruptionPos()

			elif self.interrupt.restart_flag == False and self.check_flag == False:
				self.interrupt.checkGotInterruptionPos(self.axis)
				self.check_flag = True

			elif self.interrupt.restart_flag == False and self.check_flag:
				pass

			elif self.interrupt.restart_flag:
				self.wait_flag = False
				self.interrupt_count = 0
				self.interrupt_flag = False
				self.pub_return_pos_flag = False
				self.check_flag = False
				self.interrupt.checkReturnJob(self.axis)
				print('[{}AxisCommanderInterrupt::doInterruptJob] return job'.format(self.axis))
			
			else:
				assert False

		else:
			assert False

	def _setTargetPos(self, pos):
		print('[{}AxisCommanderInterrupt::_setTargetPos] target pos: {}'.format(self.axis, pos))
		self.checkPos(pos)
		self.publishTopic(self.target_pos_pub, self.current_pos) #stop servo
		self.publishTopic(self.control_mode_pub, 'servo')
		if not(pos-self.same_pos_tolerance < self.current_pos < pos+self.same_pos_tolerance):
			self.publishTopic(self.target_pos_pub, pos)
			while self.finish_flag:
				self.publishTopic(self.target_pos_pub, pos)
			print('[{}AxisCommanderInterrupt::_setTargetPos] publishTopic()'.format(self.axis))
		else:
			print('[{}AxisCommanderInterrupt::_setTargetPos] The pos was not published. current_pos: {}'.format(self.axis, self.current_pos))
		while not self.finish_flag:
			if self.error_flag:
				break

	def setTargetPos(self, pos):
		print('[{}AxisCommanderInterrupt::setTargetPos] target pos: {}'.format(self.axis, pos))
		self.checkPos(pos)
		self.publishTopic(self.target_pos_pub, self.current_pos) #stop servo
		self.publishTopic(self.control_mode_pub, 'servo')

		if not(pos-self.same_pos_tolerance < self.current_pos < pos+self.same_pos_tolerance):
			self.publishTopic(self.target_pos_pub, pos)
			while self.finish_flag:
				self.publishTopic(self.target_pos_pub, pos)
			print('[{}AxisCommanderInterrupt::setTargetPos] publishTopic()'.format(self.axis))
		else:
			print('[{}AxisCommanderInterrupt::setTargetPos] The pos was not published. current_pos: {}'.format(self.axis, self.current_pos))
		while not self.finish_flag:
			if self.interrupt_flag:
				while self.interrupt_flag:
					pass
				return False
			if self.error_flag:
				break
		return True