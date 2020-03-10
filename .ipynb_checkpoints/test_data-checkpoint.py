import datetime
from measured_value import Measured_Value

# Test_Data stores all the measurements for a given sensor for a test
class Test_Data(object):
    def __init__(self, test_settings):
        self.title = str(test_settings)
        self.test_settings = test_settings
        self.sensor_key = test_settings.sensor_key
        self.measured_values = []
        self.measured_times = []
        self.running_time = 0.0 
        
        self.measured_values.append(Measured_Value(Measured_Value.NO_MEASUREMENT[0], Measured_Value.NO_MEASUREMENT[1], Measured_Value.NO_MEASUREMENT[2]))
        self.measured_times.append(self.running_time)
    
    def add_measurement(self, measured_value):
        if measured_value.sensor_key == self.sensor_key:    # Check to see that the data is coming from the right sensor)
            self.running_time += measured_value.deltaT      # Add deltaT to total time
            self.measured_values.append(measured_value)     # Add current measured value to list of all measured values
            self.measured_times.append(self.running_time)   # Mark the time in the test when the current measured value was added

class Test_Settings(object):
    def __init__(self, key, frequency, datetime):
        self.sensor_key = key
        self.measurement_frequency = frequency
        self.datetime = datetime
                                  
    def __str__(self):
        output = self.sensor_key + '-(measurement frequency: ' + str(self.measurement_frequency) + ')-' + str(self.datetime)
        return output
    