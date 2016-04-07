# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import numpy as np
import pandas

class TimeSerie:  
    """"""
   
    def __init__(self,myReader,freq,start=None,end=None):
            
        self.reader = myReader;

        if start is None or end is None:
            self.time_range = None
            self.freq =freq
        else:
            self.time_range = pandas.date_range(start=start, end=end,freq=freq)

        self.data = None
        self.data_source = "Undefined"
        self.name_station = "Undefined"
        self.x_coord = "Undefined"
        self.y_coord = "Undefined"
        self.vertical_datum = "Undefined"
        self.meta_data = "Undefined"

        # try to fill metadata
        self.read_metadata()

    # Read metadata
    def read_metadata(self):
        m = self.reader.read_metadata()

        if 'name_station' in m:
            self.name_station = m['name_station']
        if 'data_source' in m:
            self.data_source = m['data_source']
        if 'x_coord' in m:
            self.x_coord = float(m['x_coord'])
        if 'y_coord' in m:
            self.y_coord = float(m['y_coord'])
        if 'vertical_datum' in m:
            self.vertical_datum = m['vertical_datum']

    # Axis
    def read_axis_time(self):         
        return self.time_range;
    
    def get_time_size(self):
        return np.shape(self.time_range)[0]; 
    
    def read_data(self):

        self.data = self.reader.read_data();

        if self.time_range is None:
            self.time_range = pandas.date_range(start=self.data.index[0], end=self.data.index[self.data.index.size-1],freq=self.freq);

        self.data = self.data.reindex(self.time_range, fill_value=np.nan);

        return self.data;
        
    def read_variable_sea_surface_height(self):
        """
        Read sea_surface_height
        """   
        if self.data == None:
            self.read_data();
        
        if 'sea_surface_height' in self.data:
            return self.data.sea_surface_height;
        else:
            raise ValueError("None sea_surface_height variable")
        
    def read_variable_sea_surface_wave_significant_height(self):     
        """
        Read ssh
        """   
        if self.data is None:
            self.read_data();
        
        if 'sea_surface_wave_significant_height' in self.data:
            return self.data.sea_surface_wave_significant_height;
        else:
            raise ValueError("None sea_surface_wave_significant_height variable")

    def read_variable_sea_surface_wave_mean_period(self):
        """
        Read sea_surface_wave_mean_period
        """
        if self.data is None:
            self.read_data();

        if 'sea_surface_wave_mean_period' in self.data:
            return self.data.sea_surface_wave_mean_period;
        else:
            raise ValueError("None sea_surface_wave_mean_period variable")
    
    def resample(self,startTime,endTime):
        idx = pandas.date_range(start=startTime, end=endTime,freq='H')
        
        data = self.read_data()      
        return data.reindex(idx, fill_value=np.nan)

        