
import Jetson.GPIO as GPIO
import time
import math
import threading
import numpy as np
from services_manager import Services_Manager

class Grayson(object):
    def __init__(self):
        self.state = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                               0.0])                  # x (meters), y (meters), x_vel (meters/s), y_vel (meters/s), x_accel (meters/s^2), y_accel (meters/s^2), heading (radians) 
        self.services_manager = Services_Manager()    # Services_Manager initializes and manages sensor_state_managers, test_data_managers, etc.
    
    def run_test(self, inputs):
        self.services_manager.run_test(inputs)

        
    
        
    
    
