#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration


"!!!WARNING: DO NOT ADD ANY DEVICES USING THE GUI MENU!!!"
"(Well, okay, add at your own risk, but you have been warned!)"


# ------------------------------------------
# 
# 	Project:      CWRV8.1
#	Author:       py660, S.Wang
#	Created:      Sep 5, 2025
#	Description:  Customizable VEX Driving Framework
# 
# ------------------------------------------

import math
SAVE_SLOT = 0


# Devices
lfmot = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
lbmot = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
lmot = MotorGroup(lfmot, lbmot)
rfmot = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
rbmot = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
rmot = MotorGroup(rfmot, rbmot)
drivetrain = DriveTrain(lmot, rmot, 329.16, 330.2, 254, MM, 1) # 3rd arg used to be 319.16; formula is D * pi * 25.4
controller = Controller(PRIMARY)

# start both moters at 100%

while True:
    lvel = controller.axis3.position()
    rvel = controller.axis2.position()
    if 5 >= lvel:
        lmot.spin(FORWARD, lvel, PERCENT)
    elif -5 <= lvel:
        lmot.spin(REVERSE, -lvel, PERCENT)
    else:
        lmot.stop(COAST)
        #lmot.stop(BRAKE)

    if 5 >= rvel:
        rmot.spin(FORWARD, rvel, PERCENT)
    elif -5 <= rvel:
        rmot.spin(REVERSE, -rvel, PERCENT)
    else:
        rmot.stop(BRAKE)
        #rmot.stop(COAST)