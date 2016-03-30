# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.io.File import File
from coverage.TimeCoverage import TimeCoverage
from netCDF4 import Dataset, num2date
import numpy as np
import logging

class GMTReader (File): 

    def __init__(self, myFile):
        File.__init__(self,myFile);         
        self.ncfile = Dataset(self.filename, 'r')
        
    # Axis
    def read_axis_t(self,timestamp):
        data = self.ncfile.variables['time'][:]        
        result = num2date(data, units = self.ncfile.variables['time'].units, calendar = self.ncfile.variables['time'].calendar)
        
        if timestamp ==1:           
            return [ (t - TimeCoverage.TIME_DATUM).total_seconds() \
                for t in result];
        else:            
            return result
    
    def read_axis_x(self):        
        return self.ncfile.variables['longitude'][:]
    
    def read_axis_y(self):        
        return self.ncfile.variables['latitude'][:]
    
    def read_variable_ssh_at_time(self,t):
        return self.ncfile.variables["ssh"][t][:]
    
    def read_variable_current_at_time(self,t):
        logging.info('[GMTReader] Reading surface current')
        return [self.ncfile.variables["surface_ucur"][t][:],self.ncfile.variables["surface_vcur"][t][:]]
           
    