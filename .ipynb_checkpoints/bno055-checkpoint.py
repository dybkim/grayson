import board
import busio
import adafruit_bno055
import time
import threading
from sensor import Sensor
from callback import Callback
from measured_value import Measured_Value

class BNO055(Sensor):

    #Period is defined in seconds
    def __init__(self, period = 0.025, sensor_state_manager = None, sensor_key = Sensor.KEY_BNO055):
        i2c = busio.I2C(board.SCL_1, board.SDA_1)             # Initialize I2C bus for the BNO055 IMU Sensor
        self.sensor = adafruit_bno055.BNO055(i2c)             # Initialize BNO055 IMU Sensor
        self.measured_value = None                            # self.measured_value stores the latest IMU readings
        test = self.sensor.euler                              # Calls the sensor for initial IMU reading to check that the sensor is in a ready state
        self.is_ready = True                                  # Initializes ready true since the test did receive a valid reading
        self.period = period                                  # Time period (in seconds) for one IMU measurement reading
        self.sensor_key = sensor_key                          # Initialize sensor key to identify that future measurement readings originated from this BNO055 sensor
        
        self.observers = []                                   # Create tuple of observers that are waiting for and will receive measurement readings
        self.observers.append(sensor_state_manager)           # Append sensor_state_manager to receive measurement readings
        
    def sense(self, is_running):
        previous_time = time.time()                           # previous_time represents the time taken from the previous loop
        deltaT = 0.0                                          # deltaT represents the time elapsed between each reading
        while True:                                           # Infinitely loops and measures angular velocity
            current_time = time.time()                        # current_time is the time measured for this current loop
            if not is_running():                              # is_running() is a boolean but is passed as a lambda when the thread is created
                break                                         
           
            deltaT += current_time - previous_time            # Add difference in time between loops to deltaT

            linear_accel = self.sensor.linear_acceleration    # Obtain linear acceleration from IMU reading
            euler_angles = self.sensor.euler                  # Obtain roll, pitch, yaw angles from IMU reading
            self.measured_value = Measured_Value(self.sensor_key, [linear_accel[0], linear_accel[1], euler_angles[2]], deltaT) #Save x-accleration, y-acceleration, and yaw angle
            deltaT = 0.0                                      # reset deltaT for next measurement cycle
            previous_time = current_time                      # Set previous_time to current_time for the next loop iteration
            
            self.callback()                                   # Send measured_value to all observers who need it
                
            time.sleep(self.period)                           # Have the IMU sensor thread sleep for <period> seconds

    def sensor_state(self):
        if self.sensor.euler is None:
            self.is_ready = False
        
        self.is_ready = True
        return self.is_ready
    
    def sensor_id(self):
        return 'Sensor: BNO055 9-Axis IMU'
    
    def get_measurement(self):
        return self.measured_value
    
    def callback(self):
        for observer in self.observers:
            observer.handle_callback(Callback(self.sensor_key, self.measured_value))    # callback sends measured value to observers, and makes observers handle the sent callback
    
    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)