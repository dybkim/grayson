from sensor_state_manager import Sensor_State_Manager
from test_data_persistence import Test_Data_Persistence
from test_data import Test_Settings
from test_data import Test_Data
import datetime
import threading


# Test_Data_Manager receives all data from Sensor_State_Manager and organizes measurement readings for each sensor
# All recorded measurement readings are then stored in individual Test_Data instances
# All recorded measurements can then be exported by a Test_Data_Persistence instance
class Test_Data_Manager(object):
    def __init__(self, sensor_state_manager):
        self.test_datetime = datetime.datetime.now()
        self.test_settings = {}
        self.test_data_collection = {}
        self.init_test_setup(sensor_state_manager)
        self.is_running = False
        self.observers = []
    
    
    def init_test_setup(self, sensor_state_manager):
        self.set_test_settings(sensor_state_manager)    # Collects and stores sensor settings (periods for each measurement)
        self.init_test_data_collection()                # Initializes a collection of Test_Data instances for each sensor/servvice
        
    def set_test_settings(self, sensor_state_manager):
        for key, value in sensor_state_manager.get_sensor_settings().items():
            self.test_settings[key] = Test_Settings(key, value, self.test_datetime)   
        
    def init_test_data_collection(self):
        for key, value in self.test_settings.items():
            self.test_data_collection[key] = Test_Data(value)
    
    # Sets is_running to true, which allows callbacks to be recorded in Test_Data instances
    def begin_recording(self):
        self.is_running = True
    
    # Sets is_running to false, which prevents callbacks from being recorded in Test_Data instances
    def stop_recording(self):
        self.is_running = False
    
    # Receives measurements from Sensor_State_Manager and stores each measurement in the appropriate Test_Data instance
    def handle_callback(self, callback):
        if self.is_running:
            self.record_data(callback.data)
            self.callback(callback)
    
    # Adds a measurement reading from a callback to the appropriate Test_Data instance
    def record_data(self, measured_value):
        self.test_data_collection[measured_value.sensor_key].add_measurement(measured_value)
    
    # export_data() causes a Test_Data_Persistence instance to write csv files of measurements obtained from each sensor
    def export_data(self):
        test_datetime_string = str(self.test_datetime.today().date()) + '_(' + str(self.test_datetime.today().time()) + ')'
        test_data_persistence = Test_Data_Persistence(test_datetime_string, self.test_data_collection)
        test_data_persistence.export_data()
    
    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)
    
    def callback(self, callback):
        for observer in self.observers:
            observer.handle_callback(callback)
        

        
        
        