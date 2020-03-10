import numpy as np
from jetbot import Robot

class Controller(object):
    def __init__(self):
        self.right_wheel_controller = Wheel_PID_Controller(True)
        self.left_wheel_controller = Wheel_PID_Controller(False)
    
    def handle_callback(self, callback):
        if callback.key == Sensor.KEY_WENC_RIGHT:
            output = self.right_wheel_controller.calculate_output()
            
        
        elif callback.key == Sensor.KEY_WENC_LEFT:


class Wheel_PID_Controller(object):
    
    def __init__(self, is_right_wheel = True):
        self.kp = 0.0
        self.ki = 0.0
        self.kd = 0.0
        self.error_previous = 0.0
        self.error_total = 0.0
        self.is_right_wheel = is_right_wheel
    
    def 
    
    def calculate_output(self, v_target, v_measured, deltaT):
        error = v_target - v_measured
        
        output = self.kp * error + self.kd * (error - self.error_previous)/deltaT + self.ki*(self.error_total)
        
        if abs(output) < 0.2 and output < 0:
            output = - 0.2
        
        elif abs(output) < 0.2 and output > 0:
            output = 0.2
            
        elif abs(output) > 0.8 and output < 0:
            output = 0.8
        
        elif abs(output) > 0.8 and output > 0:
            output = 0.8
        
        #Add clamping to avoid integral windup if needed
        
        return output
    

class Wheel_Action(object):
    
    def __init__(self):
        self.input = 