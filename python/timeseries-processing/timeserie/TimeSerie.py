# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import numpy as np
import pandas

class TimeSerie:  
    """"""
   
    def __init__(self,myReader,start,end,freq):          
            
        self.reader = myReader;   
        self.time_range = pandas.date_range(start=start, end=end,freq=freq)
        self.data = None
        self.data_source = "Undefined"
        self.name_station = "Undefined"
        self.x_coord = "Undefined"
        self.y_coord = "Undefined"
        self.vertical_datum = "Undefined"
        
    # Axis        
    def read_axis_time(self):         
        return self.time_range;
    
    def get_time_size(self):
        return np.shape(self.time_range)[0]; 
    
    def read_data(self):     
        self.data = self.reader.read_data().reindex(self.time_range, fill_value='NaN');
        return self.data; 
        
    def read_variable_ssh(self):     
        """
        Read ssh
        """   
        if self.data == None:
            self.read_data();
        
        if 'ssh' in self.data:
            return self.data.ssh;
        else:
            raise ValueError("None ssh variable")         
        
    def read_variable_sea_surface_wave_significant_height(self):     
        """
        Read ssh
        """   
        if self.data == None:
            self.read_data();
        
        if 'sea_surface_wave_significant_height' in self.data:
            return self.data.sea_surface_wave_significant_height;
        else:
            raise ValueError("None sea_surface_wave_significant_height variable")   
    
    def resample(self,startTime,endTime):
        idx = pandas.date_range(start=startTime, end=endTime,freq='H')
        
        data = self.read_data()      
        return data.reindex(idx, fill_value='NaN')       

        