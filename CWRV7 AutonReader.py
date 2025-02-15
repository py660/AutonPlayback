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


# THIS PROGRAM DEPENDS ON THE GUI DEVICES MENU BEING *EMPTY* (NO DEVICES ADDED)




# ------------------------------------------
#
#   Project:      CWRV7 AutonReader
#   Author:       py660, S.Wang
#   Created:
#   Description:  github.com/py660/AutonPlayback
#
# ------------------------------------------


# Devices
left_drive_smart = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
right_drive_smart = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
controller_1 = Controller(PRIMARY)
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


# CoOoOoOoOol credits, remove in prod
bprint("-----------------------------------------------")
bprint("| Submit a PR: github.com/py660/AutonPlayback |")
bprint("-----------------------------------------------")


try:
   bprint("Opening sequence file on SD card for reading...")
   fseq = open("sequence0.txt", "r")
except OSError as e:
   bprint("File IO operation exited with", e)
   exit()


bprint("File successfully opened. Reading inputs...")




controller_1_left_shoulder_control_motors_stopped = True
controller_1_right_shoulder_control_motors_stopped = True
controller_1_x_b_buttons_control_motors_stopped = True
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False


def rc_auto_loop_function_controller_1():
 global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, controller_1_left_shoulder_control_motors_stopped, controller_1_right_shoulder_control_motors_stopped, controller_1_x_b_buttons_control_motors_stopped, remote_control_code_enabled
 # process the controller input every 20 milliseconds
 # update the motors based on the input values
 while True:
     if True:
      
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


state = {
   "Left": 0,
   "Right": 0,
   "L1": 0,
   "L2": 0,
   "R1": 0,
   "R2": 0,
   "Up": 0,
   "Down": 0,
   "X": 0,
   "Y": 0,
   "A": 0,
   "B": 0
} # Left (Joystick), Right (Joystick), L1, L2, R1, R2, Up (Button), Down (Button), X, Y, A, B


log = []


def brainupdate():
   while True:
       clearscreen()
       bprint("Time:", brain.timer.time(MSEC))
       bprint("Tasks left:", len(log))
       for line in log[:5]:
           bprint(":".join(map(str,line)))
       for k, v in state.items():
           bprint(k, v)
       wait(100, MSEC)




def loadState():
   global log, state
   log = [
       (
           float(x.strip().split("\t")[0])*1000, x.strip().split("\t")[1],
           (bool(x.strip().split("\t")[2]) if "e" in x.strip().split("\t")[2] else float(x.strip().split("\t")[2]))
       ) for x in fseq.readlines()]
   brain.timer.clear()


   while len(log):
       if brain.timer.time(MSEC) >= log[0][0]:
           state[log[0][1]] = log[0][2]
           log.pop(0)
       else:
           wait(1, MSEC)




def autonPlayback():


 global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, controller_1_left_shoulder_control_motors_stopped, controller_1_right_shoulder_control_motors_stopped, controller_1_x_b_buttons_control_motors_stopped, remote_control_code_enabled
 # process the controller input every 20 milliseconds
 # update the motors based on the input values
 while True:
     if True:
      
         # calculate the drivetrain motor velocities from the controller joystick axies
         # left = axis3
         # right = axis2
         drivetrain_left_side_speed = state["Left"]
         drivetrain_right_side_speed = state["Right"]
         controller.screen.set_cursor(2,1)
         cprint(drivetrain_left_side_speed)
         cprint(drivetrain_right_side_speed)
      
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
         if state["Down"]:
             PneumaticClaw.set(False)
         elif state["Up"]:
             PneumaticClaw.set(True)
         # to control Conveyer
         if state["L1"]:
             Conveyer.set_velocity(2000)
             Conveyer.spin(FORWARD)
             controller_1_left_shoulder_control_motors_stopped = False
         elif state["L2"]:
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
         if state["R1"]:
             Intake.set_velocity(1000)
             Intake.spin(FORWARD)
             controller_1_right_shoulder_control_motors_stopped = False
         elif state["R2"]:
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
         if state["B"]:
             DavidWhacker.set_velocity(500)
             DavidWhacker.spin(FORWARD)
             controller_1_x_b_buttons_control_motors_stopped = False
         elif state["X"]:
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


# define variable for remote controller enable/disable
remote_control_code_enabled = True




def onauton_autonomous_0():
   pass


def ondriver_drivercontrol_0():
   pass


# create a function for handling the starting and stopping of all autonomous tasks
def vexcode_auton_function():
 ctrlclear()
 cprint("Auton started")
 # Start the autonomous control tasks
 state_task = Thread(loadState)
 brainupdate_thread = Thread(brainupdate)
 playback_task = Thread(autonPlayback)
 auton_task_0 = Thread(onauton_autonomous_0)
 # wait for the driver control period to end
 while( competition.is_autonomous() and competition.is_enabled() ):
     # wait 10 milliseconds before checking again
     wait(10, MSEC)
 # Stop the autonomous control tasks
 state_task.stop()
 brainupdate_thread.stop()
 playback_task.stop()
 auton_task_0.stop()




def vexcode_driver_function():
 ctrlclear()
 cprint("Driver control started")
 # Start the driver control tasks
 rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)
 drive_control_task_0 = Thread( ondriver_drivercontrol_0 )
 # wait for the driver control period to end
 while( competition.is_driver_control() and competition.is_enabled() ):
     # wait 10 milliseconds before checking again
     wait(10, MSEC)
 # Stop the driver control tasks
 drive_control_task_0.stop()
 rc_auto_loop_thread_controller_1.stop()




# register the competition functions
competition = Competition( vexcode_driver_function, vexcode_auton_function )
#vexcode_auton_function()
# Yo Yo Yo What's Up Saxe Middle School?!
# what's up!!



