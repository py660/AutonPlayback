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

# region Preamble

"!!!WARNING: DO NOT ADD ANY DEVICES USING THE GUI MENU!!!"
"(Well, okay, add at your own risk, but you have been warned!)"

"""
<<<<<<< HEAD
Port 11_R: Left Front Motor - Green Gear Cartridge
Port 20_R: Left Back
Port 1: Right Front
Port 10: Right Back
Port 15: Inertial Sensor

Port 6: Lower Outside Intake
Port 18: Lower Inside Intake
Port 7_R: Upper Outside Intake
Port 17_R: Upper Inside Intake
=======
Port 11: Left Front Motor - Green Gear Cartridge
Port 20: Left Back Motor - Green Gear Cartridge
Port 1: Right Front Motor - Green Gear Cartridge
Port 10: Right Back Motor - Green Gear Cartridge
Port 15: Inertial Sensor
Port 6: Lower Outside Intake
Port 18: Lower Inside Intake
Port 7: Upper Outside Intake
Port 17: Upper Inside Intake
>>>>>>> refs/remotes/origin/main
"""

# ------------------------------------------
# 
# 	Project:      CWRV8.1
#	Author:       py660, S.Wang
#	Created:      Sep 5, 2025
#	Description:  Customizable VEX Driving Framework
# 
# ------------------------------------------

# endregion Preamble

# region Setup & Config

import math
SAVE_SLOT = 0
BRAKEMODE = HOLD
PIDMODE = 0 # 0: normal; 1: wheel odometry priority; 2: inertial priority

<<<<<<< HEAD
=======

# Devices
>>>>>>> refs/remotes/origin/main
lfmot = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
lbmot = Motor(Ports.PORT20, GearSetting.RATIO_18_1, True)
lmot = MotorGroup(lfmot, lbmot)
rfmot = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
rbmot = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
rmot = MotorGroup(rfmot, rbmot)
inert = Inertial(Ports.PORT15)
drivetrain = SmartDrive(lmot, rmot, inert, 329.16, 330.2, 254, MM, 1) # 3rd arg used to be 319.16; formula is D * pi * 25.4
controller = Controller(PRIMARY)

fin = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
bin = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)
fout = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
bout = Motor(Ports.PORT17, GearSetting.RATIO_18_1, True)

def calInert():
    brain.screen.print("Calibrating inertial sensor...")
    brain.screen.next_row()
    brain.screen.print("Please make sure the robot is facing towards heading 0.")
    brain.screen.next_row()
    brain.screen.print("Do not move the robot until calibration is complete!")
    inert.calibrate()
    sleep(200, MSEC)
    while inert.is_calibrating(): sleep(25, MSEC)
    drivetrain.set_heading(0)
    lmot.reset_position()
    rmot.reset_position()
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

# Calibrate the Drivetrain
calInert()

<<<<<<< HEAD
# endregion Setup

# region Movement Routines

def pickUp():
    fin.spin(FORWARD, 100, PERCENT)

def putDown():
    fin.spin(REVERSE, 100, PERCENT)

=======
def pickUp():
    fin.spin(FORWARD, 100, PERCENT)

def putDown():
    fin.spin(REVERSE, 100, PERCENT)

>>>>>>> refs/remotes/origin/main
def store():
    pickUp()
    bin.spin(FORWARD, 100, PERCENT)
    fout.spin(REVERSE, 100, PERCENT)
    bout.spin(FORWARD, 100, PERCENT)

def putTop():
    pickUp()
    fout.spin(FORWARD, 100, PERCENT)
    bin.spin(FORWARD, 100, PERCENT)
    bout.spin(FORWARD, 100, PERCENT)

def putMiddle():
    pickUp()
    bin.spin(FORWARD)
    bout.spin(REVERSE)

def stopIntake():
<<<<<<< HEAD
    fin.stop(BRAKEMODE)
    bin.stop(BRAKEMODE)
    fout.stop(BRAKEMODE)
    bout.stop(BRAKEMODE)
=======
    fin.stop(brakemode)
    bin.stop(brakemode)
    fout.stop(brakemode)
    bout.stop(brakemode)

brakemode = HOLD
>>>>>>> refs/remotes/origin/main

def drive():
    while True:
        lvel = controller.axis3.position()
        rvel = controller.axis2.position()
        if 5 >= lvel:
            lmot.spin(FORWARD, lvel, PERCENT)
        elif -5 <= lvel:
            lmot.spin(REVERSE, -lvel, PERCENT)
        else:
<<<<<<< HEAD
            lmot.stop(BRAKEMODE)
=======
            lmot.stop(brakemode)
>>>>>>> refs/remotes/origin/main
        if 5 >= rvel:
            rmot.spin(FORWARD, rvel, PERCENT)
        elif -5 <= rvel:
            rmot.spin(REVERSE, -rvel, PERCENT)
        else:
            rmot.stop(brakemode)

        if controller.buttonX.pressing():
            putTop()
        elif controller.buttonY.pressing():
            putMiddle()
        elif controller.buttonA.pressing():
            store()
        elif controller.buttonB.pressing():
            pickUp()
        elif controller.buttonDown.pressing():
            putDown()
        else:
            stopIntake()

<<<<<<< HEAD
# endregion Routines

class State():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.rot = 0

        self.l = 0
        self.r = 0
        self.rot = 0

polarToRect = lambda r, theta: (r*math.cos(math.radians(theta)), r*math.sin(math.radians(theta)))

def consumeData():
    l = 

def standardPositioning(x, y, rot):
    # Sensor readings
    l, r, rot = consumeData()

def auton():
    t = time.time()
    state = State()
    while competition.is_autonomous:
        while time.time()-t<0.01:
            time.sleep(0.001)
        t = time.time()
        x, y, rot = standardPositioning(x, y, rot)
=======



def auton():
    store()
    drivetrain.turn_to_heading(90, DEGREES, wait=False)
    drivetrain.drive_for(FORWARD, 24, INCHES, wait=True)
    stopIntake()
    drivetrain.turn_to_heading(300, DEGREES, wait=True)
    sleep(1, SECONDS)
    drivetrain.turn_to_heading(180, DEGREES)
    putMiddle()
    drivetrain.drive_for(FORWARD, 24, INCHES, wait=True)
    time.sleep(5)
>>>>>>> refs/remotes/origin/main

competition = Competition(drive, auton)