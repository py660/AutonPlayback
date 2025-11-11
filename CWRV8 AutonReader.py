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

# ------------------------------------------
# 
# 	Project:      CWRV8
#	Author:       py660
#	Created:      Sep 5, 2025
#	Description:  VEX Driving Framework
# 
# ------------------------------------------

__author__ = "py660"
__copyright__ = "Copyright (C) 2025 py660"
__version__ = "8.1"

# endregion Preamble

# region Setup & Settings

import math
import time

SAVE_SLOT = 0 # Underscore must remain for historical reasons

# Driving dynamics (if it's plural, it's probably a dictionary)
BOTCONSTANTS = { # Intrinsic properties of the robot
    "wheelTravel": 329.16, # wheel's circumference; circumference of wheel
    "trackWidth": 330.2, # robot width; distance between wheels on opposite sides
    "wheelBase": 254, # robot length; distance between the front and back wheels' axles on the same side
    "externalGearRatio": 1 # One revolution of the motor is how many revolutions of the wheel?
}
BRAKEMODE = HOLD # COAST = no resistance; BRAKE = short the + and - leads of the motor, aka regenerative braking; HOLD = use encoder to counter rotation
POWERCOEFS = { # Manual correction of varying motor strengths
    "left": 1.0,
    "right": 1.0
}
LERPCOEFS = { # How smoothed out steering should be; used as skid prevention
    "drive": 0.85,
    "auton": 0.25
}
AUTONPOWERCOEF = 0.4 # Autonomous speed restriction, based on normal operating speed

# Autonomous odometry (position tracking)
ODOMMODE = 0 # Which sensor to trust more: 0=normal; 1=wheel encoder priority
STARTPOS = { # Starting position of robot during calibration
    "x": 0, # Remember, the origin is at the center of the playing field
    "y": 0, # The units are millimeters, always
    "heading": 0 # Degrees clockwise from vertical/+y direction (0<=theta<360)
}

# Autonomous PID (movement algorithm)
DRIVEPIDMODE = 0b100 # Path-following PID module enable/disable flags; bits: 2=Proportional, 1=Integral, 0=Derivative Modules
DRIVEPIDCOEFS = { # Path-following PID controller settings
    "proportional": 0,
    "integral": 0,
    "derivative": 0
}
TURNPIDMODE = 0b100 # Turn-in-place PID module enable/disable flags; bits: 2=Proportional, 1=Integral, 0=Derivative Modules
TURNPIDCOEFS = { # Turn-in-place PID controller settings
    "proportional": 0,
    "integral": 0,
    "derivative": 0
}

# Tempvars
ldrivelerp = 0
rdrivelerp = 0


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

def calInert():
    brain.screen.print("Calibrating inertial sensor...")
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

# Calibrate sensors
calInert()

# endregion Setup

# region Movement Routines

def pickUp():
    fin.spin(FORWARD, 100, PERCENT)

def putDown():
    fin.spin(REVERSE, 100, PERCENT)

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
    fin.stop(BRAKEMODE)
    bin.stop(BRAKEMODE)
    fout.stop(BRAKEMODE)
    bout.stop(BRAKEMODE)

def ldrive(speed, lerp):
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
    while True:
        lvel = controller.axis3.position()
        rvel = controller.axis2.position()
        if -5 <= lvel <= 5:
            #lmot.stop(BRAKEMODE)
            ldrive(0, LERPCOEFS.get("drive", 1))
        else:
            ldrive(lvel/100, LERPCOEFS.get("drive", 1))
        if -5 <= rvel <= 5:
            #rmot.stop(BRAKEMODE)
            rdrive(0, LERPCOEFS.get("drive", 1))
        else:
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

# endregion Routines

# region Autonomous Routines
class State():
    def __init__(self, x=0, y=0, heading=0):
        self.x = x
        self.y = y
        self.rot = heading

        # Tempvars
        self.l = self.r = 0
        self.dl = self.dr = self.drot = 0

polarToRect = lambda r, theta: (r*math.cos(math.radians(theta)), r*math.sin(math.radians(theta)))

def consumeData(state):
    state.dl = lmot.position(DEGREES)/360*BOTCONSTANTS.get("wheelTravel", 300) - state.l
    state.l += state.dl
    state.dr = rmot.position(DEGREES)/360*BOTCONSTANTS.get("wheelTravel", 300) - state.r
    state.r += state.dr
    state.drot = inert.heading(DEGREES)/360*BOTCONSTANTS.get("wheelTravel", 300) - state.rot
    state.rot += state.drot

def trackOdometry(state, mode):
    r = theta = 0
    if mode == 0: # Default odometry
        r = (state.dl + state.dr)/2
        theta = state.drot
    if mode == 1: # Wheel encoder priority
        r = (state.dl + state.dr)/2
        theta = 180*(state.dl - state.dr)/(math.pi*BOTCONSTANTS.get("trackWidth", 320))
    #if mode == 2: # Inertial accelerometer priority
    #    rGivenL = state.dl * 
    #    r = state.drot*
    #    theta = state.drot
    dx, dy = polarToRect(r, state.rot + theta/2)
    state.x += dx
    state.y += dy

def auton(override=False):
    t = time.time()
    state = State(**STARTPOS)
    while override or (competition.is_autonomous() and competition.is_enabled()):
        if override:
            lvel = controller.axis3.position() # -100<=lvel<=100
            rvel = controller.axis2.position()
            if -5 <= lvel <= 5:
                #lmot.stop(BRAKEMODE)
                ldrive(0, LERPCOEFS.get("auton", 1))
            else:
                ldrive(lvel/100*AUTONPOWERCOEF, LERPCOEFS.get("auton", 1))
            if -5 <= rvel <= 5:
                #rmot.stop(BRAKEMODE)
                rdrive(0, LERPCOEFS.get("auton", 1))
            else:
                rdrive(rvel/100*AUTONPOWERCOEF, LERPCOEFS.get("auton", 1))

        #while time.time()-t<0.01:
        #    time.sleep(0.001)
        t = time.time()
        consumeData(state)
        trackOdometry(state, ODOMMODE)
        #brain.screen.clear_screen()
        controller.screen.set_cursor(1, 1)
        controller.screen.print("X: {:.2f} Y: {:.2f} R: {:.2f}".format(state.x, state.y, state.rot))

# endregion Autonomous Routines

#auton(True)
competition = Competition(drive, auton)