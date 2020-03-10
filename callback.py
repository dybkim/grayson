
class Callback(object):
    
    def __init__(self, key, data):
        self.key = key      # key is to identify where the data originated from (sensors, services, etc)
        self.data = data    # data is usually a Measured_Value object