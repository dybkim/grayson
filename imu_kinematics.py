import time
import math
import numpy as np
from kinematics import Kinematics

class IMU_Kinematics(Kinematics):
    # State is of the form: [x_pos, y_pos, x_vel, y_vel, x_accel, y_accel]
    def __init__(self, state = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), test_data = None):
        super().__init__(state, test_data)
    
    def calculate_states(self):
        self.total_times = self.test_data.measured_times
        for i in range(len(self.test_data.measured_values)):
            if self.test_data.measured_values[i].sensor_key != 'NULL':
                self.increment_step(self.test_data.measured_values[i])
                self.states.append(self.state)
    
    # measured_value is: [x_accel, y_accel, yaw, deltaT]
    def increment_step(self, measured_value):
        x_accel = measured_value.data[0]
        y_accel = measured_value.data[1]
        self.heading = measured_value.data[2]
        deltaT = measured_value.deltaT
        self.state[4] = x_accel
        self.state[5] = y_accel
        self.current_time += deltaT
        self.total_times.append(self.current_time)
        state_transition_matrix = np.array([[1.0, 0.0, 1.0 * deltaT, 0.0, 0.5 * (deltaT * deltaT), 0.0],
                                            [0.0, 1.0, 0.0, 1.0 * deltaT, 0.0, 0.5 * (deltaT * deltaT)],
                                            [0.0, 0.0, 1.0, 0.0, 1.0 * deltaT, 0.0],
                                            [0.0, 0.0, 0.0, 1.0, 0.0, 1.0 * deltaT],
                                            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                                            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])
        
        self.state = state_transition_matrix @ self.state
    
    def handle_callback(self, callback):
        if callback.key == Sensor.KEY_BNO055:
            self.increment_step(callback.data)
        
    
        