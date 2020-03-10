
class Measured_Value(object):
    
    NO_MEASUREMENT = ['NULL', [],  0.0]
    
    def __init__(self, sensor_key = '', data = [], deltaT = 0.0):
        self.sensor_key = sensor_key              # Identifies which sensor the measurement originated from
        self.data = data                          # holds measurement values from a given sensor
        self.deltaT = deltaT                      # Time difference from last measurement
    
    def __str__(self):                            # string representation of Measured_Value for output purposes
        output = self.sensor_key + ': ['
        
        for value in self.data:
            output += str(value) + ', '
        
        output += str(self.deltaT)
        output += ']'
        return output
        
