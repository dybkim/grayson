from jetbot import Robot
import time
from grayson_bot import Grayson
from sensor_state_manager import Sensor_State_Manager


class Test:
    sensor_state_manager = None

    @staticmethod
    def initialize_sensors():
        sensor_state_manager = Sensor_State_Manager
        sensor_state_manager.init_sensors()

    @staticmethod
    def run_individual_command_test(left_input, right_input, deltaT):
        if sensor_state_manager is None:
            initialize_sensors()
            
        grayson = Grayson()
        inputs = [left_input, right_input, deltaT]
        grayson.move(inputs)

    @staticmethod
    def run_incremental_commands_test():
        pass
    
    
    