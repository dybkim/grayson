import time
import math
import numpy as np
from kinematics import Kinematics
from jetbot import Robot


class PLANT(object):
    
    def __init__(self):
        self.jetbot = Robot()                         # Robot() is jetbot API for inputting motor controls, no need to manage PWM inputs ourselves.
    
    
    # Moves jetbot by controlling individual wheels.
    # inputs: 2D tuple with list of motor inputs and time for each motor input
    # inputs[i][0]: Left motor input for ith command
    # inputs[i][1]: Right motor input for ith command
    # inputs[i][2]: DeltaT for ith command
    def move(self, inputs):
        for i in range(len(inputs)):
                    self.jetbot.set_motors(inputs[i][0], inputs[i][1])
                    time.sleep(inputs[i][2])
                    self.jetbot.stop()
        pass


        