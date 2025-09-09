#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

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

# ------------------------------------------
# 
# 	Project:      FileReader
#	Author:       py660
#	Created:      Feb 13, 2025
#	Description:  Debugger for SD Card data
# 
# ------------------------------------------

fin = open("sequence0.txt", "r")
data = fin.readlines()
fin.close()
groups = [data[x:x+10] for x in range(0, len(data))] # the 10 in "x+10" controls the buffer size
for group in groups:
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    for line in group:
        brain.screen.print("\t".join(map(str,line)))
        brain.screen.next_row()
    wait(750, MSEC) # 750ms controls scrolling speed