from spreadsheet import Spreadsheet
import datetime
import pathlib
import os

class Test_Data_Persistence(object):
    test_data_path = os.getcwd() + ('/test-data/')
    
    # Initializes path in directory for where test data files will be stored
    def __init__(self, test_setup_info, test_data_collection):
        self.path = Test_Data_Persistence.test_data_path + str(test_setup_info)
        self.test_data_collection = test_data_collection
        self.spreadsheet_mode = True
        self.data_plot_mode = True
        self.tzero_mode = True
        self.spreadsheets = {}
        
        for key, value in self.test_data_collection.items():
            self.spreadsheets[key] = Spreadsheet(self.path, key, value)
    
    # Exports data by having spreadsheets write and save to a specified directory
    def export_data(self):
        self.create_directory()
        for key, value in self.spreadsheets.items():
            value.write_to_file()
    
    # Creates a new directory for a test if no appropriate directory exists
    def create_directory(self):
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True) 
        
    
    
        
    