import numpy as np

class Kinematics(object):
    def __init__(self, state = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), heading = 0.0, test_data = None):
        self.state = state #[x_pos, y_pos, x_vel, y_vel, x_accel, y_accel]
        self.states = []
        self.states.append(state)
        self.total_times = []
        self.total_times.append(0.0)
        self.heading = heading
        self.test_data = test_data
        self.current_time = 0.0
    
    def increment_step(self):
        pass
    
    def calculate_states(self):
        pass
    
    def check_state(self):
        return [self.state, self.heading]
    
    def get_x_pos(self):
        return self.state[0]
    
    def get_y_pos(self):
        return self.state[1]
    
    def get_x_vel(self):
        return self.state[2]
    
    def get_y_vel(self):
        return self.state[3]
    
    def get_x_acc(self):
        return self.state[4]
    
    def get_y_acc(self):
        return self.state[5]
    
    def get_heading(self):
        return self.heading
    
        
    
        