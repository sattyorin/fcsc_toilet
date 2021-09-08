#### SIDE
# 調整池 
X_BENKI_RIGHT_SIDE=150# ok
X_BENKI_LEFT_SIDE=780 #ok
Y_BENKI_FRONT_EE_SIDE=910
Z_BENKI = -275#ok
Z_FLOOR = -820
#### Enviroment Value####
# 固定値
X_MIN = 110 #ok
X_MAX = 820 #ok
Y_MIN = 30 #ok
Y_MAX = 1300 #ok
Y_BENKI_SIDE=850 #ok
Z_FLOOR_MOVING = Z_FLOOR+300
Y_EVACUATION = 1000

#### BENKI FRONT####
Y_BENKI_FRONT_EE_SIDE_REVERSE=Y_BENKI_FRONT_EE_SIDE-50
Y_BANKI_FRONT_EE_KERCHER=Y_BENKI_FRONT_EE_SIDE-50
X_BENKI_FRONT=int((X_MIN+X_MAX)/2)
X_FRONT_FLOOR_MIN=X_MIN-60
X_FRONT_FLOOR_MAX=X_MAX-30#ok

#### BENKI TOP####
Y_BENKI_TOP_MIN=Y_BENKI_FRONT_EE_SIDE-380
# Y_BENKI_TOP_MAX=950#ok

#### Machine Value####
ANGLE_EE_RIGHT=2570
ANGLE_EE_CENTER=2025
ANGLE_EE_LEFT=1508
ANGLE_EE_BACK=3100

#### Bar ####
BAR_HOME_POS = 2775
BAR_DOWN_POS = 1755


# need to check
#### field val ####
# X_MIN = 100 # same val
# X_MAX = 830 # same val
FIELD_X = X_MAX + X_MIN
# Y_MIN = Y_MIN
# Y_MAX = Y_MAX
Z_MIN = -840
Z_MAX = -80
Z_CUP = Z_MIN + 150
BENKI_X = 310
FRONT_PROHIBITION_X_MIN = 150 # FIELD_X/2 - BENKI_X/2
FRONT_PROHIBITION_X_MAX = 740 # FIELD_X/2 + BENKI_X/2
# RIGHT_SIDE_PROHIBITION_X_MIN = 450
# RIGHT_SIDE_PROHIBITION_X_MAX = FRONT_PROHIBITION_X_MIN
# LEFT_SIDE_PROHIBITION_X_MIN = FRONT_PROHIBITION_X_MAX
# LEFT_SIDE_PROHIBITION_X_MAX = FIELD_X - RIGHT_SIDE_PROHIBITION_X_MIN
FRONT_PROHIBITION_Y_MAX = 1000