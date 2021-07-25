import rospy
from dynamixel_workbench_msgs.srv import *
from std_msgs.msg import Bool

class DynamixelCommander:
	def __init__(self, id):
		self.id = id
		self.dynamixel_com = rospy.ServiceProxy('dynamixel_workbench/dynamixel_command', DynamixelCommand)

	def setVelocity(self, vel):
		request = DynamixelCommandRequest()
		request.command = ""
		request.id = self.id
		request.addr_name = "Goal_Velocity"
		request.value = vel
		self.dynamixel_com(request)

	def selPosition(self, position):
		request = DynamixelCommandRequest()
		request.command = ""
		request.id = self.id
		request.addr_name = "Goal_Position"
		request.value = position
		self.dynamixel_com(request)

class EndEfectorCommander:
	def __init__(self, theta_dynamixel_id, karcher_dynamixel_id):
		#### variable ####
		self.floor_switch = False
		self.vacuum_state = False
		self.interrupt_flag = False

		#### dynamixel ####
		self.thetadynamixelcommander = DynamixelCommander(theta_dynamixel_id)
		self.karcherdynamixelcommander = DynamixelCommander(karcher_dynamixel_id)

		#### Publisher ####
		self.vacuume_state_pub = rospy.Publisher('/arduino_ee/vacuume_state', Bool, queue_size=10)

		#### Subscriber ####
		rospy.Subscriber('/arduino_ee/floor_switch_state', Bool, self.callbackFloorSwitch)
		rospy.Subscriber('/arduino_wall/interrupt_switch_state', Bool, self.callbackInterruptSwitch)

	def setThetaPos(self, pos):
		self.thetadynamixelcommander.selPosition(pos)

	def setThetaVel(self, vel):
		self.thetadynamixelcommander.selPosition(vel)

	def setKarcherPos(self, pos):
		self.karcherdynamixelcommander.selPosition(pos)

	def setKarcherVel(self, vel):
		self.karcherdynamixelcommander.selPosition(vel)

	def setVacuumState(self, state):
		self.vacuume_state_pub.publish(state)
		self.vacuum_state = state

	def callbackFloorSwitch(self, state):
		self.floor_switch = state

	def callbackInterruptSwitch(self, state):
		self.interrupt_state = state.data
		if self.interrupt_state == True and self.interrupt_flag:
			self.interrupt_flag = False
			self.doInterruptJob()
			self.interrupt_flag = True

	def doInterruptJob(self):
		#### stop vacuum ####
		vacuum_state = self.vacuum_state
		self.setVacuumState(False)

		#### send state ####
		self.interrupt.getState('vacuum_state', vacuum_state)
		self.interrupt.checkData()

		#### wait press switch ####
		while self.interrupt_state:
			pass

		#### return to the state before the interruption ####
		self.setVacuumState(vacuum_state)