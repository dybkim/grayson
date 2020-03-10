import Jetson.GPIO as GPIO
import time
import math
import threading
from sensor import Sensor
from callback import Callback
from measured_value import Measured_Value

# Right Wheel GPIO input is pin 31
# Left Wheel GPIO input is pin 32

RIGHT_CHANNEL = 'GPIO_PZ0'
LEFT_CHANNEL = 'LCD_BL_PW'

class Wheel_Encoder(Sensor):

    # Period is defined in milliseconds
    def __init__(self, is_right, period = 0.20, sensor_state_manager = None, sensor_key = ''):
        global RIGHT_CHANNEL
        global LEFT_CHANNEL
        
        if GPIO.getmode() != GPIO.TEGRA_SOC:
            GPIO.setmode(GPIO.TEGRA_SOC)    # Initialization of GPIO pin identification mode
            
        self.period = period            # Sampling time period (each measurement is taken at every <period>). Default set to 1 millisecond
        self.current_time = 0.0         # Used to store current time in UTC ms from epoch (1/1/1970 00:00)
        self.channel = RIGHT_CHANNEL    # Left or right channel identification for left/right wheel
        self.he_value = 0.0

        #Measured value is instantaneous angular velocity (approximation)
        self.measured_value = [0.0, 0.0, 0.0]

        if is_right:
            GPIO.setup(self.channel, GPIO.IN)

        else:
            self.channel = LEFT_CHANNEL
            GPIO.setup(self.channel, GPIO.IN)

        self.he_value = GPIO.input(self.channel)    #Initialize hall effect sensor value
        self.is_ready = True
        self.sensor_key = sensor_key
        self.sensor_state_manager = sensor_state_manager

    # Method sense detects current angular velocity
    # tick_count: Counts how many magnets the HE sensor detected. Wheel encoder contains 8 magnets, so 8 ticks = 1 revolution
    def sense(self, is_running):
        tick_count = 0  # Initialize tick_count to 0
        deltaT = 0.0
        self.current_time = time.time()
        while True:  # Infinitely loops and measures angular velocity
            if not is_running():  # is_running() is a boolean but is passed as a lambda when the thread is created
                break

            input = GPIO.input(self.channel)  # Read new input from GPIO
            if self.he_value != input:  # If the input is different (which means that the he sensor picked up a different magnet)
                self.he_value = input  # Change state of he sensor value
                tick_count += 1  # Add 1 to tick count
                #print(self.channel, ' tick: ', tick_count)

            now = time.time()
            deltaT += now - self.current_time  # Calculate time from previous loop and add to deltaT

            if deltaT >= self.period:  # If enough time passed by for one period
                self.measured_value = Measured_Value(self.sensor_key, [(tick_count / 8.0) / (deltaT), tick_count],  deltaT)  # Calculate revolutions per second (rev/s) by taking (ticks/8/seconds)
#                 tick_count = 0  # Reset tick_count
                deltaT = 0  # Reset deltaT
                self.callback()

            self.current_time = now

    def set_ang_velocity(self, period):
        self.period = period

    def sensor_state(self):
        return self.is_ready
    
    def sensor_id(self):
        global RIGHT_CHANNEL
        output = 'Sensor: Wheel Encoder (Right)' if self.channel == RIGHT_CHANNEL else 'Sensor: Wheel Encoder (Left)'
        return output
    
    def get_measurement(self):
        return self.measured_value

    def callback(self):
        self.sensor_state_manager.handle_callback(Callback(self.sensor_key, self.measured_value))





