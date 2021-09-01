from sys import flags
import pandas as pd
from pos import *


class Interrupt:
	def __init__(self, interrupt_csv_path, eecom):
		print('[Interrupt::__init__]')
		self.interrupt_csv_path = interrupt_csv_path
		self.eecom = eecom
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
		self.df.at[0, 'ee'] = self.eecom.current_theta
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

	def chooseHomeSequence(self, ret = False):

		## x <= X/2 ##
		if self.current_pos['x'] <= FIELD_X/2:

			## during cleaning front ##
			if self.current_pos['x'] > FRONT_PROHIBITION_X_MIN \
					and self.current_pos['y'] < FRONT_PROHIBITION_Y_MAX:

				if self.current_pos['z'] < Z_CUP:
					if ret == False:
						self.go_home_sequence = [
							['z', Z_CUP],
							['y', FRONT_PROHIBITION_Y_MAX],
							['z', Z_MAX],
							['ee', ANGLE_EE_CENTER],
							['x', X_MIN],
							['y', Y_MIN],
						]
					
					else:
						self.go_home_sequence = [
							['z', int(self.df.at[0, 'z'])],
							['y', int(self.df.at[0, 'y'])],
							['z', Z_CUP],
							['ee', int(self.df.at[0, 'ee'])],
							['x', int(self.df.at[0, 'x'])],
							['y', FRONT_PROHIBITION_Y_MAX],
						]

				elif Z_CUP <= self.current_pos['z'] < Z_BENKI - 20:
					if ret == False:
						self.go_home_sequence = [
							['y', FRONT_PROHIBITION_Y_MAX],
							['z', Z_MAX],
							['ee', ANGLE_EE_CENTER],
							['x', X_MIN],
							['y', Y_MIN],
						]
					
					else:
						self.go_home_sequence = [
							['y', int(self.df.at[0, 'y'])],
							['z', int(self.df.at[0, 'z'])],
							['ee', int(self.df.at[0, 'ee'])],
							['x', int(self.df.at[0, 'x'])],
							['y', FRONT_PROHIBITION_Y_MAX],
						]

				elif Z_BENKI - 20 <= self.current_pos['z']:
					if ret == False:
						self.go_home_sequence = [
							['z', Z_MAX],
							['ee', ANGLE_EE_CENTER],
							['x', X_MIN],
							['y', Y_MIN],
						]

					else:
						self.go_home_sequence = [
							['z', int(self.df.at[0, 'z'])],
							['ee', int(self.df.at[0, 'ee'])],
							['x', int(self.df.at[0, 'x'])],
							['y', int(self.df.at[0, 'y'])],
						]

				else:
					assert False

			else:
				if ret == False:
					self.go_home_sequence = [
						['z', Z_MAX],
						['ee', ANGLE_EE_CENTER],
						['x', X_MIN],
						['y', Y_MIN],
					]
				else:
						self.go_home_sequence = [
							['z', int(self.df.at[0, 'z'])],
							['ee', int(self.df.at[0, 'ee'])],
							['x', int(self.df.at[0, 'x'])],
							['y', int(self.df.at[0, 'y'])],
						]

		## x > X/2 ##
		elif self.current_pos['x'] > FIELD_X/2:

			## during cleaning front ##
			if self.current_pos['x'] < FRONT_PROHIBITION_X_MAX \
					and self.current_pos['y'] < FRONT_PROHIBITION_Y_MAX:

				if self.current_pos['z'] < Z_CUP:
					if ret == False:
						self.go_home_sequence = [
							['z', Z_CUP],
							['y', FRONT_PROHIBITION_Y_MAX],
							['z', Z_MAX],
							['ee', ANGLE_EE_CENTER],
							['x', X_MAX],
							['y', Y_MIN],
						]
					
					else:
						self.go_home_sequence = [
							['z', int(self.df.at[0, 'z'])],
							['y', int(self.df.at[0, 'y'])],
							['z', Z_CUP],
							['ee', int(self.df.at[0, 'ee'])],
							['x', int(self.df.at[0, 'x'])],
							['y', FRONT_PROHIBITION_Y_MAX],
						]

				elif Z_CUP <= self.current_pos['z'] < Z_BENKI - 20:
					if ret == False:
						self.go_home_sequence = [
							['y', FRONT_PROHIBITION_Y_MAX],
							['z', Z_MAX],
							['ee', ANGLE_EE_CENTER],
							['x', X_MAX],
							['y', Y_MIN],
						]
					
					else:
						self.go_home_sequence = [
							['y', int(self.df.at[0, 'y'])],
							['z', int(self.df.at[0, 'z'])],
							['ee', int(self.df.at[0, 'ee'])],
							['x', int(self.df.at[0, 'x'])],
							['y', FRONT_PROHIBITION_Y_MAX],
						]

				elif Z_BENKI - 20 <= self.current_pos['z']:
					if ret == False:
						self.go_home_sequence = [
							['z', Z_MAX],
							['ee', ANGLE_EE_CENTER],
							['x', X_MAX],
							['y', Y_MIN],
						]
					
					else:
						self.go_home_sequence = [
							['z', int(self.df.at[0, 'z'])],
							['ee', int(self.df.at[0, 'ee'])],
							['x', int(self.df.at[0, 'x'])],
							['y', int(self.df.at[0, 'y'])],
						]

				else:
					assert False

			else:
				if ret == False:
					self.go_home_sequence = [
						['z', Z_MAX],
						['ee', ANGLE_EE_CENTER],
						['x', X_MAX],
						['y', Y_MIN],
					]

				else:
					self.go_home_sequence = [
							['z', int(self.df.at[0, 'z'])],
							['ee', int(self.df.at[0, 'ee'])],
							['x', int(self.df.at[0, 'x'])],
							['y', int(self.df.at[0, 'y'])],
						]

		else:
			assert False

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
			self.chooseHomeSequence(ret = True)
			# for axis in self.interruption_pos_order:
			# 	self.go_home_sequence.insert(0, [axis, int(self.df.at[0, axis])])
			self.current_pos = {}
		elif self.go_home_sequence[0][0] == 'ee':
			self.eecom.setThetaPos(self.go_home_sequence[0][1])
			self.gotHomePos()

	
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
		elif self.go_home_sequence[-1][0] == 'ee':
			self.eecom.setThetaPos(int(self.go_home_sequence[-1][1]))
			self.gotInterruptionPos()
