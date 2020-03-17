from sensor_state_manager import Sensor_State_Manager
from test_data_manager import Test_Data_Manager
from imu_kinematics import IMU_Kinematics
from controller import Controller

class Services_Manager(object):
    def __init__(self):
        self.sensor_state_manager = Sensor_State_Manager()
        self.data_manager = Test_Data_Manager(self.sensor_state_manager)
        self.data_manager.add_observer(self)
        self.sensor_state_manager.add_observer(self.data_manager)
        self.imu_kinematics = IMU_Kinematics()
        self.controller = Controller()
    
    def run_test(self, inputs):
        self.initialize_services()
        self.controller.input_actions(inputs)
        self.stop_services()
        
        
    def initialize_services(self):
        self.sensor_state_manager.begin_sense()
        self.data_manager.begin_recording()
    
    def stop_services(self):
        self.data_manager.stop_recording()
        self.sensor_state_manager.stop_sense()

        for key, value in self.sensor_state_manager.sensor_recording_strings.items():
            print('\n')
            for recordings in value:
                print(recordings)

        self.data_manager.export_data()
        
    def handle_callback(self, callback):
        pass
        