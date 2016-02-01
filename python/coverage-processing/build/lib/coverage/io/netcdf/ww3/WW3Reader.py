# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from netCDF4 import Dataset
from utils.jdutil import jd_to_datetime
from utils.jdutil import date_to_jd
from numpy import ndarray
import datetime as datetime

class WW3Reader:
    
    TIME_DATUM = date_to_jd(1990,01,01)

    def __init__(self, myFile):   
        self.filename = myFile; 
        
    def read_axis_t(self):       
        myFile = Dataset(self.filename, 'r')
        data = myFile.variables['time'][:]
        result = ndarray((len(data),),datetime.datetime)
        for i in xrange(len(data)):
            result[i] = jd_to_datetime(data[i]+WW3Reader.TIME_DATUM)
            
        return result
    
    def read_axis_x(self):
        myFile = Dataset(self.filename, 'r')
        return myFile.variables['longitude'][:]
    
    def read_axis_y(self):
        myFile = Dataset(self.filename, 'r')
        return myFile.variables['latitude'][:]
        
    def read_data_at_time(self,var,t):     
        myFile = Dataset(self.filename, 'r')
        return myFile.variables[var][t][:]
    
    