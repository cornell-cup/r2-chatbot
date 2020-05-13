# locomotion_cmd.py
# Translate chatbot output to actual locomotion commands in order to actuate motors

# NOTE: This is a major work in progress. So far, it has not been tested on the system,
# so distances are likely to be rather inaccurate until testing can resume in the lab

# be sure to pull from the demolocomotion git repo and run:
# python3 setup.py sdist
# pip3 install ./dist/c1c0_locomotion-1.0.tar.gz
# in the demolocomotion directory
from c1c0_locomotion import locomotion

turn_amt = 30 # WARNING: this needs testing. This is a very crude estimate (read: slightly educated guess)
              # for how many jetson->arduino motor control messages need to be sent in order
              # to make a full 90 degree turn

step = 20     # WARNING: also needs testing/consideration. This is equivalent to the jetson registering 20 input
              # values from the xbox controller - until we test, we won't know how much c1c0 actually moves

def chatbot_move(cmd):
    """move locomotion according to chatbot command
    cmd: tuple including direction and movement distance"""

    # get direction - 
    if cmd[1] == -90:
        x = -1.0
        y = 1.0
    elif cmd[1] == 90:
        x = 1.0
        y = 1.0
    elif cmd[1] == 0:
        x = 0.0
        y = 1.0
    elif cmd[1] == 180:
        x = 0.0
        y = -1.0

    # move C1C0
    if x != 0.0:
        # turn left or right using turn_amt
        for i in range(0,turn_amt):
            locomotion.motor_command(x,0)

    for i in range(0,step*cmd[2]):
        # move forward or backward by the number of steps specified
        motor_command(0,y)

