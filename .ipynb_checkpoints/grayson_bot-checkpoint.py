
import Jetson.GPIO as GPIO
from jetbot import Robot
import time
import math
import threading
import numpy as np
from services_manager import Services_Manager

class Grayson(object):
    def __init__(self):
        self.state = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                               0.0])                  # x (meters), y (meters), x_vel (meters/s), y_vel (meters/s), x_accel (meters/s^2), y_accel (meters/s^2), heading (radians)
        self.jetbot = Robot()                         # Robot() is jetbot API for inputting motor controls, no need to manage PWM inputs ourselves.
        self.services_manager = Services_Manager()    # Services_Manager initializes and manages sensor_state_managers, test_data_managers, etc.
        
    def initialize_services(self):
        self.services_manager.initialize_services()
    
    def stop_services(self):
        self.services_manager.stop_services()
    
    def run_test(self, inputs):
        self.initialize_services()                    # Start all required services before test begins
        self.move(inputs)                             # Enter motor inputs 
        self.stop_services()                          # Stop all services once testing concludes

        
    
        
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

    
