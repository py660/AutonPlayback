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

3WP A & B: Right Optical Shaft Encoder
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

AUTONMODE = 0 # 0 = RIGHT; 1 = LEFT

# Driving dynamics (if it's plural, it's probably a dictionary)
BOTCONSTANTS = { # Intrinsic properties of the robot
    "wheelTravel": 329.16, # wheel's circumference in mm
    "trackWidth": 330.2, # robot width; distance between wheels on opposite sides
    "odomWheelTravel": 164.892, # odometry wheel's circumference in mm
    "odomWidth": 163.576, # the distance between two wheels if you mirrored the odometry wheel onto the other axis; negative if odom wheel is on left side
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
    "auton": 1 # 0.25; isolated tracking wheels remove the need for smoothing
}
AUTONPOWERCOEF = 0.8 # Autonomous speed restriction; scaled from normal operating speed in addition to POWERCOEFS

# AUTON LOOP:
#   1 -> Sense;     Sensor Data Collection
#   2 -> Odom;      Odometry (outputs current v-pose)
#   3 -> PreNav;    Path Planning and Adaptation (manages objectives (including V-POSE, ROT, CMD, etc), aka. keyframes, given pre-planned spline and command-hybrid path)
#   4 -> Nav;       Path Following (turns current objective into live navigation instructions and determines v-pose error)
#   5 -> PID;       Motor Controller (turns error into actions; outputs motor PWM with respect to error accumulation and its subsequent correction)

# 1&2 Sense/Odom: Autonomous odometry (position tracking)
ODOMMODE = 0b10 # Which sensor to trust more: 0=internal notor encoders/1=optical encoder(s); 0=normal/1=don't use inertial
STARTPOS = { # Starting pose of robot during calibration
    "x": -1390, # Remember, the origin is at the center of the playing field
    "y": -390, # The units are millimeters, always
    "heading": 90 # Degrees clockwise from vertical/+y direction (0<=theta<360)
}

# 3 PreNav: Spline (path-creating) configuration
SAVE_SLOT = 0 # Underscore must remain for historical reasons
SUBDIVRESOLUTION = 70 # mm (+- 1) between each recorded point in a path
VPOSEEPSILON = 60 # mm tolerance from a V-POSE objective's pos target to still be acceptably accomplished
ROTEPSILON = 1 # deg tolerance from a ROT objective's rot target

# 4 Nav: Planning (live navigation curve-creating) algorithm
LOOKAHEAD = 0.7 # Don't change this

# 5: Autonomous PID (navigation algorithm)
DRIVEPIDCOEFS = { # Motor controller PID settings
    "proportional": 0.2, # 0 for disabled
    "integral": 0,
    "derivative": 0
}
TURNPIDCOEFS = { # (turn-in-place algorithm)
    "proportional": 0.1,
    "integral": 0,
    "derivative": 0
}

# The field, including walls, is 3690mm x 3690mm. Assuming
# the origin is at the center, the usable field's coordinates
# fall within [-1778,1778] for both x and y, although it's
# best to stay within +-1750.

# NOTE: (127*14 to convert from desmos coordinates to mm)
# NOTE: This program deals in millimeters and headings in clockwise degrees. Thus, remember to use math.atan2(x, y) and math.radians() when appropriate.


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
renc = Encoder(brain.three_wire_port.a)
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
    #lenc.reset_position()
    renc.reset_position()
    lmot.reset_position()
    rmot.reset_position()
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

def flopInputMode():
    global inputmode
    inputmode = 1 - inputmode
    controller.rumble("." + "."*inputmode)
    #controller.screen.clear_screen()
    #controller.screen.print("Input mode: {}".format("Two-Wheel Drive" if inputmode == 1 else "Throttle-Steering Drive"))

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

# endregion Routines

# region Autonomous Routines

# region Math Dependencies
polarToRect = lambda r, theta: Vector((r*math.cos(math.radians(theta)), r*math.sin(math.radians(theta))))
rotate = lambda vec, theta: Vector((math.cos(theta)*vec.x + math.sin(theta)*vec.y, -math.sin(theta)*vec.x + math.cos(theta)*vec.y))
class Vector(tuple):
    """Vectors without numpy."""
    def __init__(self, coord=(0,0)):
        self.x = coord[0]
        self.y = coord[1]

    def dist(self, other): # type: (Vector) -> float
        if not isinstance(other, Vector):
            raise TypeError("Distance can only be calculated between two Vectors")
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    @property
    def r(self):
        return math.sqrt(self.x**2 + self.y**2)
    @property
    def theta(self):
        return math.degrees(math.atan2(self.x, self.y)) # Clockwise from +y
    
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector((self.x + other.x, self.y + other.y))
        raise TypeError("Unsupported operand type(s) for +: 'Vector' and '{}'".format(type(other).__name__))  
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector((self.x - other.x, self.y - other.y))
        raise TypeError("Unsupported operand type(s) for -: 'Vector' and '{}'".format(type(other).__name__))
    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector((self.x * scalar, self.y * scalar))
        raise TypeError("Unsupported operand type(s) for *: 'Vector' and '{}'".format(type(scalar).__name__))
    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector((self.x / scalar, self.y / scalar))
        raise TypeError("Unsupported operand type(s) for /: 'Vector' and '{}'".format(type(scalar).__name__))
    def __floordiv__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vector((self.x // scalar, self.y // scalar))
        raise TypeError("Unsupported operand type(s) for //: 'Vector' and '{}'".format(type(scalar).__name__))
    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False
    def __repr__(self):
        return "Vector({}, {})".format(self.x, self.y)
# endregion Math Dependencies

# region Objective Definitions
class Objective():
    """Generic target; Please don't initialize without subclassing."""
    def activate(self): # type: () -> None
        pass

    def calculateError(self, state): # type: (State) -> None
        pass

    def completed(self, state): # type: (State) -> bool
        return True
    
class VPoseObjective(Objective):
    """A V-POSE (velocity + position + rotation) target from a curve."""
    def __init__(self, vel, pos, rot): # type: (int, Vector, float) -> None
        self.vel = vel
        self.pos = pos
        self.rot = rot

    def completed(self, state):
        return self.pos.dist(state.pos) <= VPOSEEPSILON

class RotationObjective(Objective):
    """A target heading."""
    def __init__(self, rot): # type: (float) -> None
        self.rot = rot

    def completed(self, state):
        return -ROTEPSILON <= self.rot - state.rot <= ROTEPSILON

class RoutineObjective(Objective):
    """A wildcard routine (e.g. intake) to perform."""
    def __init__(self, callback): # type: (Callable) -> None
        self.callback = callback # callback triggers the routine; this could be considered the most generic usuable routine

    def activate(self):
        self.callback()

class DelayObjective(Objective):
    """A pause for a specified amount of time."""
    def __init__(self, duration): # type: (int) -> None
        self.t = False
        self.duration = duration

    def activate(self):
        self.t = time.time() * 1000

    def completed(self, _):
        return self.t and time.time() * 1000 - self.t >= self.duration
# endregion Objective Definitions

class Path():
    """Manages the objectives for the robot to follow. Beware: Heavy
    multivar-calc, arc-length parametrization, and splines inside!"""
    def __init__(self, objectives): # type: (list[Objective]) -> None
        self.objectives = objectives

    @staticmethod
    def parse(data): # type: (str) -> list[Objective]
        """Parses objectives from stored file data."""
        lines = map(str.upper, map(str.replace, data.split("\n"), " ", ""))
        out = []
        vel = 100
        for line in lines:
            line = line.split(":")
            if line[0] == "CURVE":
                a, b, c, d = map(Vector, map(str.split, line[1].replace("(","").replace(")","").split("|"), ","))
                arclength = Path._arcLength(lambda t: Path.Bez(t, a, b, c, d))
                for i in range(math.ceil(arclength/SUBDIVRESOLUTION)*SUBDIVRESOLUTION+1):
                    i /= SUBDIVRESOLUTION
                    out.append(VPoseObjective(vel, Path.Bez(i, a, b, c, d), Path.BezDer(i, a, b, c, d).theta))

            elif line[0] == "CMD":
                left, right = line[1].split("=")
                if left == "SET_VELOCITY":
                    vel = int(right)
                elif left == "TURN_HEADING":
                    out.append(RotationObjective(float(right)))
                elif left == "ROUTINE":
                    routines = {
                        "PICK_UP": pickUp,
                        "PUT_DOWN": putDown,
                        "STORE": store,
                        "PUT_TOP": putTop,
                        "PUT_MIDDLE": putMiddle,
                        "STOP_INTAKE": stopIntake
                        }
                    out.append(RoutineObjective(routines[right]))
                elif left == "DELAY":
                    out.append(DelayObjective(int(right)))
                else:
                    raise ValueError("Invalid CMD \"{}\"!".format(left))
            else:
                raise ValueError("Unrecognized action \"{}\"!".format(line[0]))
        return out
    
    @staticmethod
    def _arcLength(curveFunc): #type: (Callable) -> float
        """Estimates the arc length of a curve."""
        return sum(curveFunc(x/20).dist(curveFunc((x+1)/20)) for x in range(20))
    
    @property
    def currentObjective(self): # type: () -> Objective | None
        """Returns the first objective, or None if none exist."""
        return self.objectives[0] if len(self.objectives) > 0 else None
    
    def advanceObjectives(self, state): #type: (State) -> None
        """Discards completed objectives from start of queue; activates new objectives as necessary."""
        while self.currentObjective:
            self.currentObjective.activate()
            if self.currentObjective.completed(state):
                self.objectives.pop(0)
    
    @staticmethod
    def Bez(t, A, B, C, D): # type: (float, Vector, Vector, Vector, Vector) -> Vector
        """Bernstein polynomial form for parametric cubic Bezier curves."""
        return A*(1-t)**3 + B*3*t*(1-t)**2 + C*3*t**2*(1-t) + D*t**3
    
    @staticmethod
    def BezDer(t, A, B, C, D): # type: (float, Vector, Vector, Vector, Vector) -> Vector
        """First derivative of Bernstein polynomial form for parametric cubic Bezier curves."""
        return (B - A)*3*(1-t)**2 + (C - B)*2*t*(1-t) + (D - C)*t**2
    
    @staticmethod
    def HBez(t, A, va, vd, D): # type: (float, Vector, Vector, Vector, Vector) -> Vector
        """Hermite variant of connected cubic Bezier curves."""
        return Path.Bez(t, A, A+va/3, D-vd/3, D)
    
    @staticmethod
    def HBezDer(t, A, va, vd, D): # type: (float, Vector, Vector, Vector, Vector) -> Vector
        """First derivative of hermite varient of connected cubic bezier curves"""
        return Path.BezDer(t, A, A+va/3, D-vd/3, D)


class PID:
    """Generic Proportional-Integral-Derivative controller."""
    def __init__(self, proportional, integral, derivative): # type: (float, float, float) -> None
        self.kp = proportional
        self.ki = integral
        self.kd = derivative
        self._i = 0
        self._d = 0
        self._t = 0
        self._dt = 0

    def loop(self, err): # type: (float) -> float
        if self._t == 0:
            self._t = time.time()
        dt = time.time() - self._t
        self._t += dt
        

        p = self.kp * err

        self._i += dt * err
        i = self.ki * self._i

        d = self.kd * (err - self._d) / dt
        self._d = err

        return p+i+d


class State:
    """Current v-pose (velocity + position + rotation) of the robot."""
    def __init__(self, x=0, y=0, heading=0, velocity=0, pathData=[]): # type: (float, float, float, int, list) -> None
        self.pos = Vector((x, y))
        self.rot = heading
        self.vel = velocity # Sensor Data

        self.path = Path(pathData) # PreNav Ddata
        self.drivePid = PID(**DRIVEPIDCOEFS)
        self.turnPid = PID(**TURNPIDCOEFS)

        # Tempvars
        self._l = self._r = self._0 = 0
        self._dl = self._dr = self._do = self._drot = 0

    def consumeData(self, mode): # type: (int) -> None
        """Consumes raw data from sensors."""
        self._drot = inert.heading(DEGREES) - self.rot
        self.rot += self._drot
        if mode & 0b10 == 0: # IME
            self._dl = lmot.position(DEGREES)/360*BOTCONSTANTS.get("wheelTravel", 300) - self._l
            self._l += self._dl
            self._dr = rmot.position(DEGREES)/360*BOTCONSTANTS.get("wheelTravel", 300) - self._r
            self._r += self._dr
            self.vel = (lmot.velocity(DPS)/360*BOTCONSTANTS.get("wheelTravel", 300) + rmot.velocity(DPS)/360*BOTCONSTANTS.get("wheelTravel", 300))/2
        else: # Optical Encoder
            self._do = renc.position(DEGREES)/360*BOTCONSTANTS.get("odomWheelTravel", 160) - self._o
            self._o += self._do
            self.vel = renc.velocity(DPS)/360*BOTCONSTANTS.get("odomWheelTravel", 160) - math.radians(self._drot)*BOTCONSTANTS.get("odomWidth", 160)/2
        #self.vel = (lenc.velocity(DPS)/360*BOTCONSTANTS.get("wheelTravel", 300) + renc.velocity(DPS)/360*BOTCONSTANTS.get("wheelTravel", 300))/2

    def trackOdometry(self, mode): # type: (int) -> None
        """Calculates robot position given previously read sensor data."""
        r = theta = 0
        if mode == 0b00: # Default odometry + IME
            r = (self._dl + self._dr)/2
            theta = self._drot
        elif mode == 0b01: # Wheel encoder priority + IME
            r = (self._dl + self._dr)/2
            theta = math.degrees((self._dl - self._dr)/BOTCONSTANTS.get("trackWidth", 320))
        elif mode == 0b10: # Default odometry + Optical Encoder
            r = (self._do) - math.radians(self._drot)*BOTCONSTANTS.get("odomWidth", 160)/2
            theta = self._drot
        else: # You can't have odometry using just the wheel encoders
            raise Exception("Too few encoders to use encoder priority mode; minimum 2 required.")

        #if mode == 2: # Inertial accelerometer priority
        #    rGivenL = state.dl * 
        #    r = state.drot*
        #    theta = state.drot
        dpos = polarToRect(r, self.rot + theta/2)
        self.pos = self.pos + dpos
    
    def _calcNaviBezDer(self, t): #type: (float) -> Vector
        """Calculates real-time navigational bezier."""
        if not isinstance(self.path.currentObjective, VPoseObjective):
            return Vector()
        return Path.HBezDer(t, self.pos, Vector(), polarToRect(1, self.path.currentObjective.rot)*350, self.path.currentObjective.pos)
    
    def actionNavigation(self):
        """Acts on the current objective."""
        if isinstance(self.path.currentObjective, VPoseObjective):
            Ts = self._calcNaviBezDer(LOOKAHEAD)
            Ttheta = (Ts.theta - self.rot) % math.tau
            driveDiff = self.drivePid.loop(Ttheta)
            if driveDiff >= 0:
                ldrive(1, LERPCOEFS.get("auton", 1))
                rdrive(1-driveDiff, LERPCOEFS.get("auton", 1))
            else:
                ldrive(1+driveDiff, LERPCOEFS.get("auton", 1))
                rdrive(1, LERPCOEFS.get("auton", 1))
        elif isinstance(self.path.currentObjective, RotationObjective):
            Ttheta = (self.path.currentObjective.rot - self.rot) % math.tau
            turnDiff = self.turnPid.loop(Ttheta)
            ldrive(turnDiff, LERPCOEFS.get("auton", 1))
            rdrive(-turnDiff, LERPCOEFS.get("auton", 1))
        elif isinstance(self.path.currentObjective, RoutineObjective):
            pass
        elif isinstance(self.path.currentObjective, DelayObjective):
            pass
        else:
            pass


def auton(override=False):
    t = time.time()
    path = None
    #f = open("spline0.txt", "r")
    #Path()
    fin = open("spline" + str(SAVE_SLOT) + ".txt", "r")
    data = fin.read()
    fin.close()
    state = State(**STARTPOS, pathData=Path.parse(data))
    while override or (competition.is_autonomous() and competition.is_enabled()):
        if override:
            lvel = controller.axis3.position()
            rvel = controller.axis2.position()
            lvel = lvel*AUTONPOWERCOEF if abs(lvel) > 5 else 0
            rvel = rvel*AUTONPOWERCOEF if abs(rvel) > 5 else 0
            if inputmode == 1:
                ldrive((lvel+rvel)/100, LERPCOEFS.get("auton", 1))
                rdrive((lvel-rvel)/100, LERPCOEFS.get("auton", 1))
            else:
                ldrive(lvel/100, LERPCOEFS.get("auton", 1))
                rdrive(rvel/100, LERPCOEFS.get("auton", 1))

        #while time.time()-t<0.01:
        #    time.sleep(0.001)
        t += (td := time.time() - t)
        state.consumeData(ODOMMODE)
        state.trackOdometry(ODOMMODE)
        state.path.advanceObjectives(state)
        if not override:
            state.actionNavigation()

        controller.screen.set_cursor(1, 1)
        controller.screen.print("X: {:.2f} Y: {:.2f} R: {:.2f}".format(state.pos[0], state.pos[1], state.rot))

# endregion Autonomous Routines

competition = Competition(drive, auton)