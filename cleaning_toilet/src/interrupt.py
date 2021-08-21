from sys import flags
import pandas as pd


class Interrupt:
	def __init__(self, interrupt_csv_path):
		print('[Interrupt::__init__]')
		self.interrupt_csv_path = interrupt_csv_path
		self.columns_len = 3
		self.df = pd.DataFrame()
		self.go_home_flag = False
		self.got_home_flag = False
		self.restart_flag = False
		self.gotHome = {}
		self.return_job = {}
		self.current_pos = {}
		self.go_home_sequence = []
		self.home_pos = 0
		self.got_interruption_pos_flag = False

	def getAxisPos(self, axis, pos):
		print('[Interrupt::getAxisPos]')
		self.df.at[0, axis] = pos

	def getState(self, name, state):
		print('[Interrupt::getState]')
		self.df.at[0, name] = state

	def checkData(self):
		print('[Interrupt::checkData]')
		if len(self.df.columns) == self.columns_len:
			self.writeCSV()

	def writeCSV(self):
		print('[Interrupt::writeCSV]')
		self.df.to_csv(self.interrupt_csv_path)
		self.go_home_flag = True

	def checkGotInterruptionPos(self, axis): 
		print('[Interrupt::checkGotInterruptionPos]')
		self.gotHome[axis] = True
		if len(self.gotHome) == self.columns_len:
			self.restart_flag = True
			self.gotHome = {}

	def checkReturnJob(self, axis):
		print('[Interrupt::resetFlag]')
		self.return_job[axis] = True
		if len(self.return_job) == self.columns_len: #if all finished
			self.go_home_flag = False
			self.restart_flag = False
			self.df = pd.DataFrame()
			self.return_job = {}
			self.got_interruption_pos_flag = False
			self.got_home_flag = False

	def chooseHomeSequence(self):
		if self.current_pos['x'] == 0:
			self.go_home_sequence = [
				['z', 0],
				['y', 0],
				['x', 0],
			]
			self.interruption_pos_order = ['x', 'y', 'z']
		else:
			self.go_home_sequence = [
				['z', 0],
				['y', 0],
				['x', 0],
			]
			self.interruption_pos_order = ['x', 'y', 'z']

	def setCurrentPos(self, axis, pos):
		self.current_pos[axis] = pos
		if len(self.current_pos) == self.columns_len:
			self.chooseHomeSequence()

	def getHomePos(self, axis):
		if self.go_home_sequence[0][0] == axis:
			self.home_pos = self.go_home_sequence[0][1]
			return True
		else:
			return False

	def gotHomePos(self):
		self.go_home_sequence.pop(0)
		if len(self.go_home_sequence) == 0:
			self.got_home_flag = True
			self.chooseHomeSequence()
			for axis in self.interruption_pos_order:
				self.go_home_sequence.insert(0, [axis, int(self.df.at[0, axis])])
			print(self.go_home_sequence)
			self.current_pos = {}

	
	def getInterruptionPos(self, axis):
		if self.go_home_sequence[-1][0] == axis:
			self.home_pos = self.go_home_sequence[-1][1]
			return True
		else:
			return False

	def gotInterruptionPos(self):
		self.go_home_sequence.pop(-1)
		if len(self.go_home_sequence) == 0:
			self.got_interruption_pos_flag = True
