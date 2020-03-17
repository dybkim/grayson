import numpy as np
from jetbot import Robot
from plant import PLANT
import time
from sensor import Sensor
import math

class Controller(object):
    
    def __init__(self, goal_vel = 0.0):
        self.goal_ticks = self.convert_to_ticks(goal_vel)
        self.plant = PLANT()
        self.wheel_controllers = {Sensor.KEY_WENC_RIGHT: Wheel_PID_Controller(True, 0.01),
                                  Sensor.KEY_WENC_LEFT: Wheel_PID_Controller(False, 0.01)}
        self.wheel_inputs = [0.0, 0.0]
        self.jetbot = Robot()
    
    def input_actions(self, inputs):
        for i in range(len(inputs)):
                    self.jetbot.set_motors(inputs[i][0], inputs[i][1])
                    time.sleep(inputs[i][2])
                    self.jetbot.stop()
        pass
    
    def handle_callback(self, callback):
        ticks_per_second = self.calculate_velocity(callback.data)
        
        if callback.key == Sensor.KEY_WENC_RIGHT:
            output = self.right_wheel_controller.calculate_output()
            
        
#         elif callback.key == Sensor.KEY_WENC_LEFT:
    
    def convert_to_ticks(self, goal_vel):
        return (goal_vel / (2 * math.pi) * 8)
        
        
        


class Wheel_PID_Controller(object):
    
    WHEEL_RADIUS_LEFT = .03
    WHEEL_RADIUS_RIGHT = .03
    
    def __init__(self, is_right_wheel = True, kp = 0.0, ki = 0.0, kd = 0.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error_previous = 0.0
        self.error_total = 0.0
        self.is_right_wheel = is_right_wheel
    
    
    def calculate_output(self, ticks_target, ticks_measured, deltaT):
        error = ticks_target - ticks_measured
        
        output = ticks_measured + self.kp * error + self.kd * (error - self.error_previous)/deltaT + self.ki*(self.error_total)
        
#         if abs(output) < 0.2 and output < 0:
#             output = - 0.2
        
#         elif abs(output) < 0.2 and output > 0:
#             output = 0.2
            
#         elif abs(output) > 0.8 and output < 0:
#             output = 0.8
        
#         elif abs(output) > 0.8 and output > 0:
#             output = 0.8
        
        #Add clamping to avoid integral windup if needed
        
        return output
    

# class Wheel_Action(object):
    
#     def __init__(self):
#         self.input = 