import pandas as pd

class Interrupt:
	def __init__(self, interrupt_csv_path):
		self.interrupt_csv_path = interrupt_csv_path
		self.columns_len = 4
		self.df = pd.DataFrame()
		self.go_home_flag = False

	def getAxisPos(self, axis, pos):
		self.df.at[0, axis] = pos

	def getState(self, name, state):
		self.df.at[0, name] = state

	def checkData(self):
		if len(self.df.columns) == self.columns_len:
			self.writeCSV()

	def writeCSV(self):
		self.df.to_csv(self.interrupt_csv_path)
		self.go_home_flag = True
