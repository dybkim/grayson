import time
import math
import threading


# Abstract class for specific Sensor types, meant to be overridden
class Sensor(object):
    # Keys used to identify each sensor in a dict
    KEY_BNO055 = 'BNO055'
    KEY_WENC_RIGHT = 'WENC_R'
    KEY_WENC_LEFT = 'WENC_L'

    # init_sense: Runs as a thread in the background, constantly updating the value self.measured_value
    def init_sense(self, is_running):
        sensor_thread = threading.Thread(target=self.sense, args=(lambda: is_running,))
        sensor_thread.start()

    # measures sensor value depending on type of sensor (to be overridden in subclasses)
    def sense(self, is_running):
        pass

    # returns if sensor is ready to read values (to be overridden in subclasses)
    def sensor_state(self):
        pass
    
    def sensor_id(self):
        pass
    
    def get_measurement(self):
        pass
    
    def set_output_mode(self, state):
        pass
    
    def callback(self):
        pass


    
    
    