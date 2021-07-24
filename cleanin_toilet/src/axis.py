import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Bool

class AxisCommander:
	def __init__(self, axis):
		#### Publisher ####
		self.target_pos_pub = rospy.Publisher('/arduino_{}/target_pos'.format(axis), Int32, queue_size=10)
		self.interrupt_switch_pub = rospy.Publisher('/arduino_{}/interrupt_switch_state'.format(axis), Bool, queue_size=10)

		#### Subscriber ####
		rospy.Subscriber('/arduino_{}/current_pos'.format(axis), Int32, self.callbackCurrentPos)
		rospy.Subscriber('/arduino_wall/interrupt_switch_state', Bool, self.callbackInterruptSwitch)

	def callbackCurrentPos(self, data):
		data.data
	
	def callbackInterruptSwitch(self, state):
		self.publishInterrupt(state.data)

	def setTargetPos(self, pos):
		self.target_pos_pub.publish(pos)

	def publishInterrupt(self, state):
		self.interrupt_switch_pub.publish(state)


def main():
	rospy.init_node('axis', anonymous=True)
	

	r = rospy.Rate(10) # 10hz
	while not rospy.is_shutdown():
		setTargetPos()

		rospy.spin()
		r.sleep()

	

if __name__ == '__main__':
	main()