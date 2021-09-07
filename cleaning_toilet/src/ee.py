import rospy
from dynamixel_workbench_msgs.srv import *
from std_msgs.msg import Bool
from pos import *

class DynamixelCommander:
	def __init__(self, id, dynamixel_com):
		self.id = id
		self.dynamixel_com = dynamixel_com

	def setVelocity(self, vel):
		request = DynamixelCommandRequest()
		request.command = ""
		request.id = self.id
		request.addr_name = "Goal_Velocity"
		request.value = vel
		self.dynamixel_com(request)

	def setPosition(self, position):
		request = DynamixelCommandRequest()
		request.command = ""
		request.id = self.id
		request.addr_name = "Goal_Position"
		request.value = position
		self.dynamixel_com(request)
		
class EndEfectorCommander:
	def __init__(self, theta_dynamixel_id):
		#### variable ####
		self.floor_switch = False
		self.vacuum_state = False
		self.interrupt_flag = False
		self.current_theta = ANGLE_EE_CENTER

		#### dynamixel ####
		dynamixel_com = rospy.ServiceProxy('dynamixel_workbench/dynamixel_command', DynamixelCommand)
		self.thetadynamixelcommander = DynamixelCommander(theta_dynamixel_id, dynamixel_com)
		# self.karcherdynamixelcommander = DynamixelCommander(karcher_dynamixel_id)

		#### Publisher ####
		self.vacuume_state_pub = rospy.Publisher('/arduino_ee/vacuume_state', Bool, queue_size=10)

		#### Subscriber ####
		rospy.Subscriber('/arduino_ee/floor_switch_state', Bool, self.callbackFloorSwitch)
		# rospy.Subscriber('/arduino_wall/interrupt_switch_state', Bool, self.callbackInterruptSwitch)

	def setThetaPos(self, pos):
		print('[EndEfectorCommander::setThetaPos] pos: {}'.format(pos))
		self.current_theta = pos
		self.thetadynamixelcommander.setPosition(pos)

	def setThetaVel(self, vel):
		self.thetadynamixelcommander.setVelocity(vel)

	# def setKarcherAngle(self, ang):
	# 	self.karcherdynamixelcommander.setPosition(ang)

	# def setKarcherVel(self, vel):
	# 	self.karcherdynamixelcommander.setVelocity(vel)

	def setVacuumState(self, state):
		# return
		self.vacuume_state_pub.publish(state)
		self.vacuum_state = state

	def callbackFloorSwitch(self, state):
		self.floor_switch = state

class BarCommander:
	def __init__(self, id):
		self.id = id
		dynamixel_com = rospy.ServiceProxy('dynamixel_workbench_bar/dynamixel_command', DynamixelCommand)
		self.barcommander = DynamixelCommander(id, dynamixel_com)
		self.current_theta = BAR_HOME_POS

	def setThetaPos(self, pos):
		print('[BarCommander::setThetaPos] pos: {}'.format(pos))
		self.current_theta = pos
		self.barcommander.setPosition(pos)

	def setThetaVel(self, vel):
		self.barcommander.setVelocity(vel)