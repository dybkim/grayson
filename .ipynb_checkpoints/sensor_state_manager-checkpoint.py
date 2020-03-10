import time
import threading
from bno055 import BNO055
from wheel_encoder import Wheel_Encoder
from sensor import Sensor
from callback import Callback

PERIOD_IMU = 0.01
PERIOD_WENC = 0.5 

class Sensor_State_Manager(object):
    
    # Instantiates a BNO055 IMU and two wheel encoder sensors (right and left)
    def __init__(self, refresh_rate = 0.01):
        
        # Initialize IMU sensor nd left/right wheel encoders
        bno055 = BNO055(PERIOD_IMU, self, Sensor.KEY_BNO055)                            
        left_wenc = Wheel_Encoder(False, PERIOD_WENC, self, Sensor.KEY_WENC_LEFT)
        right_wenc = Wheel_Encoder(True, PERIOD_WENC, self, Sensor.KEY_WENC_RIGHT)
        
        # Add all sensors
        self.sensors = {Sensor.KEY_BNO055: bno055,
                        Sensor.KEY_WENC_LEFT: left_wenc,
                        Sensor.KEY_WENC_RIGHT: right_wenc}
        
        # Set all sensors to "not ready" state
        self.sensor_states = {Sensor.KEY_BNO055: False,
                            Sensor.KEY_WENC_LEFT: False,
                            Sensor.KEY_WENC_RIGHT: False}
        
        # Set overall state to "not ready" until all individual sensors are ready
        self.sensor_manager_state = False
        
        # Stores latest measurement from each sensor in a dict
        self.sensor_data = {Sensor.KEY_BNO055: [],
                            Sensor.KEY_WENC_LEFT: [],
                            Sensor.KEY_WENC_RIGHT: []}
        self.sensor_recording_strings = {}
        
        # Saves state to indicate if the sensors are current reading measurements
        self.is_sensing = False
        
        # Indicates if measurement readings will be printed out as they are being read
        self.output_mode = {Sensor.KEY_BNO055: True,
                        Sensor.KEY_WENC_LEFT: True,
                        Sensor.KEY_WENC_RIGHT: True}
        
        # DEPRECATED
        self.refresh_rate = refresh_rate
        
        # Observers that will receive measurement readings from sensors
        self.observers = []

    # Checks to see if all the sensors are in ready state
    def validate_sensor_state(self):
        for key, value in self.sensors.items():
            if not value.sensor_state():
                self.sensor_manager_state = False
                return self.sensor_manager_state

        self.sensor_manager_state = True
        return self.sensor_manager_state
    
    # Begins all background measurement threads for all sensors if all sensors are in ready state
    def init_sensors(self):
        while not self.validate_sensor_state():
            time.sleep(1)
        
        # If all sensors are ready, then the sensors will being reading measurements
        for key, value in self.sensors.items():
            self.sensor_states[key] = True
            sensor_thread = threading.Thread(target=value.sense, args=(lambda: self.sensor_states[key],))
            sensor_thread.start()
            
            print('Began', value.sensor_id())
            
    # Calls init_sense() and sets current sensing state to true
    def begin_sense(self):
        self.is_sensing = True
        self.sensor_recording_strings = {Sensor.KEY_BNO055: [],
                                  Sensor.KEY_WENC_LEFT: [],
                                  Sensor.KEY_WENC_RIGHT: []}
        self.init_sensors()
    
    # Terminates all sensor threads by setting each sensing boolean for each sensor thread to false
    def stop_sense(self):
        self.is_sensing = False
        for key in self.sensor_states.keys():
            self.sensor_states[key] = False
        
        print('Stopped sensor readings')
        
    def set_output_mode(self, key, state):
        self.output_mode[key] = state
    
    # Receives data from each sensor, then sends this data to each observer
    def handle_callback(self, callback):
        if self.is_sensing:
            self.sensor_data[callback.key] = callback.data
            self.callback(callback)

            if self.output_mode[callback.key]:
                self.sensor_recording_strings[callback.key].append(str(callback.data))
    
    # Sends data to each observer
    def callback(self, callback):
        for observer in self.observers:
            observer.handle_callback(callback)
            
    def add_observer(self, observer):
        if not observer in self.observers:
            self.observers.append(observer)
        
    # Obtains measurement periods for each sensor
    def get_sensor_settings(self):
        periods = {}
        for key, value in self.sensors.items():
            periods[key] = value.period
        
        return periods