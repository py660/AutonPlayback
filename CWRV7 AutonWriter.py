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

# DO NOT ADD ANY DEVICES USING THE GUI MENU

# ------------------------------------------
# 
# 	Project:      CWRV7 AutonWriter
#	Author:       py660, S.Wang
#	Created:
#	Description:  github.com/py660/AutonPlayback
# 
# ------------------------------------------

SAVE_SLOT = 0


# Devices
left_drive_smart = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
right_drive_smart = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
controller_1 = Controller(PRIMARY)
controller = controller_1
Conveyer = Motor(Ports.PORT3, GearSetting.RATIO_6_1, True)
Intake = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
PneumaticClaw = DigitalOut(brain.three_wire_port.a)
DavidWhacker = Motor(Ports.PORT11, GearSetting.RATIO_6_1, False)
Flash = DigitalOut(brain.three_wire_port.c)
controller = controller_1

#AutonPlayback Helpers

def bprint(*args, **kwargs):
    brain.screen.print(*args, **kwargs)
    brain.screen.next_row()

def clearscreen():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.set_font(FontType.MONO12)
    #brain.screen.set_font(FontType.MONO20)
    #brain.screen.set_fill_color(Color.RED)
    #brain.screen.set_pen_color(Color.RED)
    #brain.screen.draw_rectangle(0, 0, 480, 36)
    #brain.screen.set_pen_color(Color.WHITE)
    #bprint(" "*14 + "AutonPlayback v1.0.0")
    #brain.screen.set_font(FontType.MONO12)
    #brain.screen.set_cursor(3,1)
    #bprint(" "*18 + "WRITE MODE ACTIVATED")

def cprint(*args, **kwargs):
    controller.screen.print(*args, **kwargs)
    controller.screen.next_row()

def ctrlclear():
    controller.screen.clear_screen()
    controller.screen.set_cursor(1,1)

bprint("Awaiting controller input...")

# CoOoOoOoOol credits, remove in prod
bprint("-----------------------------------------------")
bprint("| Submit a PR: github.com/py660/AutonPlayback |")
bprint("-----------------------------------------------")

bprint("You are saving to save slot #" + str(SAVE_SLOT))
controller.rumble("..")

try:
    bprint("Opening drive sequence file for writing...")
    fseq = open("sequence" + str(SAVE_SLOT) + ".txt", "w+")
except OSError as e:
    bprint("File IO operation exited with", e)
    bprint("Did you insert an SD card with an appropriate FS (e.g. FAT32)?")

bprint("File successfully opened. Awaiting start command...")
bprint("Tap screen to stop recording.")


cprint("Press X to start")
controller.rumble("..")

startseq = False
startseqcountdown = False

controller_1.buttonDown.pressed(lambda: btnupdate("Down", True))
controller_1.buttonDown.released(lambda: btnupdate("Down", False))
controller_1.buttonUp.pressed(lambda: btnupdate("Up", True))
controller_1.buttonUp.released(lambda: btnupdate("Up", False))
controller_1.buttonL1.pressed(lambda: btnupdate("L1", True))
controller_1.buttonL1.released(lambda: btnupdate("L1", False))
controller_1.buttonL2.pressed(lambda: btnupdate("L2", True))
controller_1.buttonL2.released(lambda: btnupdate("L2", False))
controller_1.buttonR1.pressed(lambda: btnupdate("R1", True))
controller_1.buttonR1.released(lambda: btnupdate("R1", False))
controller_1.buttonR2.pressed(lambda: btnupdate("R2", True))
controller_1.buttonR2.released(lambda: btnupdate("R2", False))
controller_1.buttonB.pressed(lambda: btnupdate("B", True))
controller_1.buttonB.released(lambda: btnupdate("B", False))
controller_1.buttonX.pressed(lambda: btnupdate("X", True))
controller_1.buttonX.released(lambda: btnupdate("X", False))
controller_1.axis2.changed(lambda: axisupdate("Left", controller.axis2))
controller_1.axis3.changed(lambda: axisupdate("Right", controller.axis3))

while not startseqcountdown:
    wait(50, MSEC)

for i in range(3, 0, -1):
    ctrlclear()
    cprint(i)
    controller.rumble(".")
    wait(1, SECONDS)
ctrlclear()
cprint("GO!")
controller.rumble("-")
startseq = True


brain.timer.clear()

log = []

def save():
    for line in log:
        fseq.write("\t".join(map(str, line)) + "\n")
    fseq.close()
    clearscreen()
    bprint("Done writing!")
    ctrlclear()
    cprint("Saved!")
    controller.rumble("-")
    wait(120, SECONDS)
    while True:
        controller.rumble("-.")
        wait(50, MSEC)

#brain.screen.pressed(save)

# 17 rows avail.
# 480 x 240

def brainupdate():
    for line in log[-10:]:
        clearscreen()
        bprint("\t".join(line))

brainupdate_thread = Thread(brainupdate)

def btnupdate(key, pressed):
    if not startseq:
        if key == "X":
            startseqcountdown = True
        return
    log.append((brain.timer.time(MSEC)/1000, key, pressed))

def axisupdate(side, ctrlaxis):
    if not startseq:
        return
    log.append((brain.timer.time(MSEC)/1000, side, ctrlaxis.position()))

# define variables used for controlling motors based on controller inputs
controller_1_left_shoulder_control_motors_stopped = True
controller_1_right_shoulder_control_motors_stopped = True
controller_1_x_b_buttons_control_motors_stopped = True
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# mainloop
def mainloop():
  global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, controller_1_left_shoulder_control_motors_stopped, controller_1_right_shoulder_control_motors_stopped, controller_1_x_b_buttons_control_motors_stopped, remote_control_code_enabled
  # process the controller input every 20 milliseconds
  # update the motors based on the input values
  while True:
      if not startseq:
          pass
      elif brain.timer.time(MSEC) > 15000:
          startseq = False
          save()
      else:
          # calculate the drivetrain motor velocities from the controller joystick axies
          # left = axis3
          # right = axis2
          drivetrain_left_side_speed = controller_1.axis3.position()
          drivetrain_right_side_speed = controller_1.axis2.position()
        
          # check if the value is inside of the deadband range
          if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
              # check if the left motor has already been stopped
              if drivetrain_l_needs_to_be_stopped_controller_1:
                  # stop the left drive motor
                  left_drive_smart.stop()
                  # tell the code that the left motor has been stopped
                  drivetrain_l_needs_to_be_stopped_controller_1 = False
          else:
              # reset the toggle so that the deadband code knows to stop the left motor next
              # time the input is in the deadband range
              drivetrain_l_needs_to_be_stopped_controller_1 = True
          # check if the value is inside of the deadband range
          if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
              # check if the right motor has already been stopped
              if drivetrain_r_needs_to_be_stopped_controller_1:
                  # stop the right drive motor
                  right_drive_smart.stop()
                  # tell the code that the right motor has been stopped
                  drivetrain_r_needs_to_be_stopped_controller_1 = False
          else:
              # reset the toggle so that the deadband code knows to stop the right motor next
              # time the input is in the deadband range
              drivetrain_r_needs_to_be_stopped_controller_1 = True
        
          # only tell the left drive motor to spin if the values are not in the deadband range
          if drivetrain_l_needs_to_be_stopped_controller_1:
              left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
              left_drive_smart.spin(FORWARD)
          # only tell the right drive motor to spin if the values are not in the deadband range
          if drivetrain_r_needs_to_be_stopped_controller_1:
              right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
              right_drive_smart.spin(FORWARD)
          # check the buttonL1/buttonL2 status
          if controller_1.buttonDown.pressing():
              PneumaticClaw.set(False)
          elif controller_1.buttonUp.pressing():
              PneumaticClaw.set(True)
          # to control Conveyer
          if controller_1.buttonL1.pressing():
              Conveyer.set_velocity(2000)
              Conveyer.spin(FORWARD)
              controller_1_left_shoulder_control_motors_stopped = False
          elif controller_1.buttonL2.pressing():
              Conveyer.set_velocity(200)
              Conveyer.spin(REVERSE)
              controller_1_left_shoulder_control_motors_stopped = False
          elif not controller_1_left_shoulder_control_motors_stopped:
              Conveyer.stop()
              # set the toggle so that we don't constantly tell the motor to stop when
              # the buttons are released
              controller_1_left_shoulder_control_motors_stopped = True
          # check the buttonR1/buttonR2 status
          # to control Intake
          if controller_1.buttonR1.pressing():
              Intake.set_velocity(1000)
              Intake.spin(FORWARD)
              controller_1_right_shoulder_control_motors_stopped = False
          elif controller_1.buttonR2.pressing():
              Intake.set_velocity(1000)
              Intake.spin(REVERSE)
              controller_1_right_shoulder_control_motors_stopped = False
          elif not controller_1_right_shoulder_control_motors_stopped:
              Intake.stop()
              # set the toggle so that we don't constantly tell the motor to stop when
              # the buttons are released
              controller_1_right_shoulder_control_motors_stopped = True
          # check the buttonX/buttonB status
          # to control DavidWhacker
          if controller_1.buttonB.pressing():
              DavidWhacker.set_velocity(500)
              DavidWhacker.spin(FORWARD)
              controller_1_x_b_buttons_control_motors_stopped = False
          elif controller_1.buttonX.pressing():
              DavidWhacker.set_velocity(500)
              DavidWhacker.spin(REVERSE)
              controller_1_x_b_buttons_control_motors_stopped = False
          elif not controller_1_x_b_buttons_control_motors_stopped:
              DavidWhacker.stop()
              # set the toggle so that we don't constantly tell the motor to stop when
              # the buttons are released
              controller_1_x_b_buttons_control_motors_stopped = True
      # wait before repeating the process
      wait(20, MSEC)


mainloop_thread = Thread(mainloop)
