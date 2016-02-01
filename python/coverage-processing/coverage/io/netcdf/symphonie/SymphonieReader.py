# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from netCDF4 import Dataset
from numpy import ndarray
import datetime as datetime

class SymphonieReader:    


    def __init__(self, myFile):   
        self.filename = myFile; 
        
    def read_axis_t(self):       
        myFile = Dataset(self.filename, 'r')
        data = myFile.variables['time'][:]
        result = ndarray((len(data),),datetime.datetime)
        for i in xrange(len(data)):
            result[i] = jd_to_datetime(data[i])
            
        return result
    
    def read_axis_x(self):
        myFile = Dataset(self.filename, 'r')
        return myFile.variables['longitude_t'][:]
    
    def read_axis_y(self):
        myFile = Dataset(self.filename, 'r')
        return myFile.variables['latitude_t'][:]
    
    def read_axis_z(self):
        myFile = Dataset(self.filename, 'r')
        return myFile.variables['depth_t'][::]
        
    def read_data_at_level(self,var,z):     
        myFile = Dataset(self.filename, 'r')
        return myFile.variables[var][z][:]
    
    def read_data(self,var):     
        myFile = Dataset(self.filename, 'r')
        return myFile.variables[var][:]    
    