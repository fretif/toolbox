# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.io.File import File
from coverage.TimeCoverage import TimeCoverage
from netCDF4 import Dataset, num2date
import numpy as np
from datetime import datetime
from time import strftime

class WW3Reader (File): 

    def __init__(self, myFile):
        File.__init__(self,myFile);         
        self.ncfile = Dataset(self.filename, 'r')
        
    # Axis
    def read_axis_t(self,timestamp):
        data = self.ncfile.variables['time'][:]        
        temp = num2date(data, units = self.ncfile.variables['time'].units, calendar = "julian")
        
        result = [ datetime.strptime(str(t), '%Y-%m-%d %H:%M:%S') \
                for t in temp];
      
        if timestamp ==1:           
            return [ (t - TimeCoverage.TIME_DATUM).total_seconds() \
                for t in result];
        else:            
            return result;
    
    def read_axis_x(self):        
        return self.ncfile.variables['longitude'][:]
    
    def read_axis_y(self):        
        return self.ncfile.variables['latitude'][:]
    
    # Scalar 
    def read_variable_mask(self):         
        return self.ncfile.variables["MAPSTA"][:]
    
    def read_variable_bathy_at_time(self,t):         
        return self.ncfile.variables["dpt"][t][:]
    
    def read_variable_wlv_at_time(self,t):         
        return self.ncfile.variables["wlv"][t][:]
    
    def read_variable_hs_at_time(self,t):         
        return self.ncfile.variables["hs"][t][:]
    
    def read_variable_waves_dir_at_time(self,t):         
        return self.ncfile.variables["dir"][t][:]
    
    def read_variable_waves_mean_period_at_time(self,t):         
        return self.ncfile.variables["t01"][t][:]
    
    def read_variable_j_pressure_at_time(self,t):         
        return self.ncfile.variables["bhd"][t][:]
    
    # Vector
    def read_variable_u_surface_current_at_time(self,t):         
        return self.ncfile.variables["ucur"][t][:]
    
    def read_variable_v_surface_current_at_time(self,t):         
        return self.ncfile.variables["vcur"][t][:]
    
    def read_variable_u_taw_at_time(self,t):         
        return self.ncfile.variables["utaw"][t][:]
    
    def read_variable_v_taw_at_time(self,t):         
        return self.ncfile.variables["vtaw"][t][:]
    
    def read_variable_u_two_at_time(self,t):         
        return self.ncfile.variables["utwo"][t][:]
    
    def read_variable_v_two_at_time(self,t):         
        return self.ncfile.variables["vtwo"][t][:]
    
    def read_variable_u_surface_stokes_drift_at_time(self,t):         
        return self.ncfile.variables["uuss"][t][:]
    
    def read_variable_v_surface_stokes_drift_at_time(self,t):         
        return self.ncfile.variables["vuss"][t][:]
           
    