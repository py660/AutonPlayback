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

RIGHT = 0; LEFT = 1

# Left/Right Auton:
AUTONMODE = RIGHT

# region Preamble

"!!!WARNING: DO NOT ADD ANY DEVICES USING THE GUI MENU!!!"
"(Well, okay, add at your own risk, but you have been warned!)"

"""
Port 11_R: Left Front Motor - Green Gear Cartridge
Port 20_R: Left Back
Port 1: Right Front
Port 10: Right Back
Port 15: Inertial Sensor

Port 6: Lower Outside Intake
Port 18: Lower Inside Intake
Port 7_R: Upper Outside Intake
Port 17_R: Upper Inside Intake
"""

#
#
#                ██████╗██╗    ██╗██████╗ ██╗   ██╗ █████╗                                 
#               ██╔════╝██║    ██║██╔══██╗██║   ██║██╔══██╗                                
#               ██║     ██║ █╗ ██║██████╔╝██║   ██║╚█████╔╝                                
#               ██║     ██║███╗██║██╔══██╗╚██╗ ██╔╝██╔══██╗                                
#               ╚██████╗╚███╔███╔╝██║  ██║ ╚████╔╝ ╚█████╔╝                                
#                ╚═════╝ ╚══╝╚══╝ ╚═╝  ╚═╝  ╚═══╝   ╚════╝     
#
#
#    o     o .oPYo.  o    o           oooooo   o     o  .oPYo. .oPYo. 
#    8     8 8.      `b  d'           8        8     8  8   `8 8    8 
#    8     8 `boo     `bd'     o    o 8pPYo.   8     8 o8YooP' 8      
#    `b   d' .P       .PY.     Y.  .P     `8   `b   d'  8   `b 8      
#     `b d'  8       .P  Y.    `b..d'     .P    `b d'   8    8 8    8 
#      `8'   `YooP' .P    Y.    `YP'  `YooP'     `8'    8    8 `YooP' 
#    :::..::::.....:..::::..:::::...:::.....::::::..::::..:::..:.....:
#    :::::::::: CWRV8 AutonPlayback - VEX Driving Framework ::::::::::
#    :::::::::::: https://github.com/py660/AutonPlayback :::::::::::::
#    :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#        
#

__author__ = "py660"
__copyright__ = "Copyright (C) 2025 py660"
__version__ = "8.3"

# endregion Preamble

# region Setup & Settings

import math
import time

# Driving dynamics (if it's plural, it's probably a dictionary)
BOTCONSTANTS = { # Intrinsic properties of the robot
    "wheelTravel": 329.16, # wheel's circumference in mm
    "trackWidth": 330.2, # robot width; distance between wheels on opposite sides
    "wheelBase": 254, # robot length; distance between the front and back wheels' axles on the same side
    "externalGearRatio": 1 # One revolution of the motor is how many revolutions of the wheel?
}
BRAKEMODE = COAST # COAST = no resistance; BRAKE = short the + and - leads of the motor, aka regenerative braking; HOLD = use encoder to counter rotation
POWERCOEFS = { # Manual correction of potential deviations in motor efficiency; a trivial difference in speed is achieved at 85-127
    "left": 0.85,
    "right": 0.85
}
LERPCOEFS = { # How smooth the acceleration should be; used for slip prevention
    "drive": 0.85,
    "auton": 1 # UNUSED 0.25; isolated tracking wheels remove the need for smoothing
}
AUTONPOWERCOEF = 0.8 # Autonomous speed restriction; scaled from normal operating speed in addition to POWERCOEFS

STARTPOS = { # Starting pose of robot during calibration
    "x": -1390, # Remember, the origin is at the center of the playing field
    "y": -390, # The units are millimeters, always
    "heading": 90 # Degrees clockwise from vertical/+y direction (0<=theta<360)
}

# Tempvars
ldrivelerp = 0
rdrivelerp = 0
inputmode = 0


# Devices
lfmot = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
lbmot = Motor(Ports.PORT20, GearSetting.RATIO_18_1, True)
lmot = MotorGroup(lfmot, lbmot)
rfmot = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
rbmot = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
rmot = MotorGroup(rfmot, rbmot)
inert = Inertial(Ports.PORT15)
drivetrain = SmartDrive(lmot, rmot, inert, units=MM, **BOTCONSTANTS) # 4th arg used to be 319.16 (idk why); formula is D * pi * 25.4
controller = Controller(PRIMARY)

fin = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
bin = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)
fout = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
bout = Motor(Ports.PORT17, GearSetting.RATIO_18_1, True)

def calibrate():
    brain.screen.print("Calibrating sensors...")
    brain.screen.next_row()
    brain.screen.print("Please make sure the robot is configured at the specified starting position.")
    brain.screen.next_row()
    brain.screen.print("Do not move the robot until calibration is complete!")
    inert.calibrate()
    sleep(200, MSEC)
    while inert.is_calibrating(): sleep(25, MSEC)
    inert.set_heading(STARTPOS.get("heading", 0))
    drivetrain.set_heading(STARTPOS.get("heading", 0))
    lmot.reset_position()
    rmot.reset_position()
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

def flopInputMode():
    global inputmode
    inputmode = 1 - inputmode
    controller.rumble(".")
    controller.screen.clear_screen()
    controller.screen.print("Input mode: {}".format("Two-Wheel Drive" if inputmode == 1 else "Throttle-Steering Drive"))

# Calibrate sensors
calibrate()

controller.buttonUp.pressed(flopInputMode)

# endregion Setup & Settings

# region Movement Routines

def intakeSpeed(speed):
    fin.set_velocity(speed, PERCENT)
    fout.set_velocity(speed, PERCENT)
    bin.set_velocity(speed, PERCENT)
    bout.set_velocity(speed, PERCENT)

def pickUp():
    fin.spin(FORWARD)

def putDown():
    fin.spin(REVERSE)

def store():
    pickUp()
    bin.spin(FORWARD)
    fout.spin(REVERSE)
    bout.spin(FORWARD)

def putTop():
    pickUp()
    fout.spin(FORWARD)
    bin.spin(FORWARD)
    bout.spin(FORWARD)

def putMiddle():
    pickUp()
    bin.spin(FORWARD)
    fout.spin(FORWARD)
    bout.spin(REVERSE)

def stopIntake():
    fin.stop(BRAKEMODE)
    bin.stop(BRAKEMODE)
    fout.stop(BRAKEMODE)
    bout.stop(BRAKEMODE)

def ldrive(speed, lerp): # Ignore that this lerp is clock-dependent for now (not a big issue)
    global ldrivelerp
    ldrivelerp += (speed - ldrivelerp) * lerp
    #controller.screen.set_cursor(1, 1)
    #controller.screen.print("Lerp: {:.2f}".format(ldrivelerp))
    if abs(ldrivelerp) < 0.01:
        ldrivelerp = 0
    if ldrivelerp == 0:
        lmot.stop(BRAKEMODE)
    lmot.spin(FORWARD if ldrivelerp > 0 else REVERSE, abs(ldrivelerp * 100)*POWERCOEFS.get("left", 1), PERCENT)

def rdrive(speed, lerp):
    global rdrivelerp
    rdrivelerp += (speed - rdrivelerp) * lerp
    if abs(rdrivelerp) < 0.01:
        rdrivelerp = 0
    if rdrivelerp == 0:
        rmot.stop(BRAKEMODE)
    rmot.spin(FORWARD if rdrivelerp > 0 else REVERSE, abs(rdrivelerp * 100)*POWERCOEFS.get("right", 1), PERCENT)

def drive():
    intakeSpeed(100)
    while True:
        lvel = controller.axis3.position()
        if inputmode == 1:
            rvel = controller.axis1.position()
        else:
            rvel = controller.axis2.position()
        lvel = lvel if abs(lvel) > 5 else 0
        rvel = rvel if abs(rvel) > 5 else 0
        if inputmode == 1:
            ldrive((lvel+rvel)/100, LERPCOEFS.get("drive", 1))
            rdrive((lvel-rvel)/100, LERPCOEFS.get("drive", 1))
        else:
            ldrive(lvel/100, LERPCOEFS.get("drive", 1))
            rdrive(rvel/100, LERPCOEFS.get("drive", 1))

        if controller.buttonX.pressing() or controller.buttonL1.pressing():
            putTop()
        elif controller.buttonY.pressing() or controller.buttonL2.pressing():
            putMiddle()
        elif controller.buttonA.pressing() or (controller.buttonR1.pressing() and controller.buttonR2.pressing()):
            store()
        elif controller.buttonB.pressing() or controller.buttonR1.pressing():
            pickUp()
        elif controller.buttonDown.pressing() or controller.buttonR2.pressing():
            putDown()
        else:
            stopIntake()

# endregion Movement Routines

# region Easy Auton

def auton():
    intakeSpeed(40)
    drivetrain.set_drive_velocity(100*AUTONPOWERCOEF, PERCENT)
    putTop()
    drivetrain.drive_for(FORWARD, 1100, MM)
    time.sleep(1.7)
    stopIntake()
    drivetrain.drive_for(REVERSE, 500, MM)
    if AUTONMODE == 1:
        drivetrain.turn_to_heading(0, DEGREES)
    else:
        drivetrain.turn_to_heading(180, DEGREES)
    drivetrain.drive_for(FORWARD, 730, MM)
    drivetrain.turn_to_heading(90, DEGREES)
    drivetrain.drive_for(FORWARD, 150, MM)
    intakeSpeed(80)
    putTop()
    drivetrain.drive_for(FORWARD, 50, MM)
    time.sleep(2.75)

# endregion Easy Auton

#auton(True)
competition = Competition(drive, auton)