import time
import math
import numpy as np
from kinematics import Kinematics

class Wheel_Kinematics(Kinematics):
    # State is of the form: [x_pos, y_pos, x_vel, y_vel, x_accel, y_accel]
    def __init__(self, state = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])):
        super().__init__(state)
    
    # data is: [ang_vel_rightwheel, ang_vel_leftwheel, deltaT]
    def increment_step(self, data):
        omega_rwheel = data[0]
        omega_lwheel = data[1]
        deltaT = data[2]
        
#         self.state[4] = x_accel
#         self.state[5] = y_accel
#         state_transition_matrix = np.array([[1.0, 0.0, 1.0 * deltaT, 0.0, 0.5 * (deltaT * deltaT), 0.0],
#                                             [0.0, 1.0, 0.0, 1.0 * deltaT, 0.0, 0.5 * (deltaT * deltaT)],
#                                             [0.0, 0.0, 1.0, 0.0, 1.0 * deltaT, 0.0],
#                                             [0.0, 0.0, 0.0, 1.0, 0.0, 1.0 * deltaT],
#                                             [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#                                             [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])
        
        self.state = state_transition_matrix @ self.state
    
        