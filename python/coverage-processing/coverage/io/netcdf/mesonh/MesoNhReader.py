# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.io.File import File
from netCDF4 import Dataset, num2date
import numpy as np

class MesoNhReader(File):

    def __init__(self,myFile):   
        File.__init__(self,myFile);
        self.ncfile = Dataset(self.filename, 'r')
        
    # Axis
    def read_axis_t(self,timestamp): 
        raise RuntimeError("No implemented yet.")
        data = self.ncfile.variables['time'][:]         
        result = num2date(data, units = self.ncfile.variables['time'].units, calendar = "gregorian")
        
        if timestamp ==1:           
            return [ (t - TimeCoverage.TIME_DATUM).total_seconds() \
                for t in result];
        else:            
            return result
    
    def read_axis_x(self):       
        return self.ncfile.variables['LON'][:]
    
    def read_axis_y(self):      
        return self.ncfile.variables['LAT'][:]
    
    def read_axis_z(self):
        raise RuntimeError("No implemented yet.")   
        return self.ncfile.variables['depth_t'][::]
        
    # Data    
    def read_variable_mask(self): 
        raise RuntimeError("No implemented yet.")   
        return self.ncfile.variables["mask_t"][0][:]
    
    def read_variable_mesh_size(self): 
        raise RuntimeError("No implemented yet.")   
        return self.ncfile.variables["sqrt_dxdy"][:]    
    
    def read_variable_topography(self): 
        return self.ncfile.variables["ZS"][:]
     
    