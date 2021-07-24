#### constant ####
theta_dynamixel_id = 1
karcher_dynamixel_id = 2

#### variable ####
offset = 0

#### instance ####
xaxiscom = XAxisCommander()
yaxiscom = YAxisCommander()
zaxiscom = ZAxisCommander()
eecom = EndEfectorCommander(theta_dynamixel_id, karcher_dynamixel_id)

def calibration():
	print('calibration')

def sweepTheFloor():
	print('sweepTheFloor')

def karcherTheToiletSeat():
	print('karcherTheToiletSeat')

def karcherTheFloor():
	print('karcherTheFloor')

def main():
	print('main')

if __name__ == "__main__":
	main()