import csv
from imu_kinematics import IMU_Kinematics
from sensor import Sensor

class Spreadsheet(object):
    def __init__(self, directory_path, sensor_key, test_data):
        file_path = directory_path + '/' + test_data.title + '.csv'
        self.strategy = self.spreadsheet_strategy_factory(file_path, sensor_key, test_data)
        
    def write_to_file(self):
        self.strategy.write_to_file()
        pass
    
    def spreadsheet_strategy_factory(self, file_path, sensor_key, test_data):
        if sensor_key == Sensor.KEY_BNO055:
            return IMU_Data_Spreadsheet_Strategy(file_path, test_data)
        
        elif sensor_key == Sensor.KEY_WENC_RIGHT or sensor_key == Sensor.KEY_WENC_LEFT:
            return Wheel_Encoder_Data_Spreadsheet_Strategy(file_path, test_data)
        
class Data_Spreadsheet_Strategy(object):
    def __init__(self, file_path = '', test_data = None, service = None):
        self.file_path = file_path
        self.test_data = test_data
        self.service = service
        
class Wheel_Encoder_Data_Spreadsheet_Strategy(Data_Spreadsheet_Strategy):
    
    def write_to_file(self):
        with open(self.file_path, 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['Time (Total): (s)', 'time (delta): (s)', 'Ticks: (ticks / s)', 'Revolutions: (rev / s)'])
            
            for i in range(len(self.test_data.measured_values)):
                
                if self.test_data.measured_values[i].sensor_key == 'NULL':
                    filewriter.writerow([0.0, 0.0, 0.0, 0.0])
                
                else:
                    measured_value = self.test_data.measured_values[i]
                    total_time = self.test_data.measured_times[i]
                    filewriter.writerow([total_time, measured_value.deltaT, measured_value.data[0], measured_value.data[1]])
        
        

class IMU_Data_Spreadsheet_Strategy(Data_Spreadsheet_Strategy):
    
    def __init__(self, file_path, test_data):
        super(IMU_Data_Spreadsheet_Strategy,self).__init__(file_path, test_data)
        self.imu_kinematics = IMU_Kinematics()
    
    def write_to_file(self):
        if self.imu_kinematics is not None:
            with open(self.file_path, 'w') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(['Time (Total): (s)', 'time (delta): (s)', 'x position (pred) (m)',  'y position (pred) (m)',  'x velocity (pred) (m/s)',  'y velocity (pred) (m/s)',  'x acceleration (pred) (m/s^2)',  'y acceleration (pred) (m/s^2)'])

                for i in range(len(self.test_data.measured_values)):

                    if self.test_data.measured_values[i].sensor_key == 'NULL':
                        filewriter.writerow([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

                    else:
                        measured_value = self.test_data.measured_values[i]
                        total_time = self.test_data.measured_times[i]
                        self.imu_kinematics.increment_step(measured_value)
                        current_state = self.imu_kinematics.state
                        filewriter.writerow([total_time, measured_value.deltaT, current_state[0], current_state[1], current_state[2], current_state[3], current_state[4], current_state[5]])
                        
        else:
            print('Failed to write IMU data! Must initialize imu_kinematics! in IMU_Kinematics_Strategy!')

    