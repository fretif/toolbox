# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from netCDF4 import Dataset
from datetime import date
from datetime import timedelta

class MercatorReader:    
    
    TIME_DATUM = date(2007, 10, 31)

    def __init__(self, myFile):   
        self.filename = myFile; 
        
    def read_axis_t(self,raw):       
        myFile = Dataset(self.filename, 'r')
        data = myFile.variables['time_counter'][:]  
        if raw ==1:
            return data
        else:
            return [MercatorReader.TIME_DATUM  + timedelta(seconds=t.astype(int)) \
                for t in data];
    
    def read_axis_x(self):
        myFile = Dataset(self.filename, 'r')
        return myFile.variables['nav_lon'][:]
    
    def read_axis_y(self):
        myFile = Dataset(self.filename, 'r')
        return myFile.variables['nav_lat'][:]
    
    def read_axis_z(self):
        myFile = Dataset(self.filename, 'r')
        return myFile.variables['deptht'][::] 
    
    def read_data(self,var):     
        myFile = Dataset(self.filename, 'r')
        return myFile.variables[var][:] 
    
    def read_data_at_level(self,var,z):     
        myFile = Dataset(self.filename, 'r')
        return myFile.variables[var][z][:]
    
    def read_data_at_time(self,var,t):     
        myFile = Dataset(self.filename, 'r')
        return myFile.variables[var][t][:]
    
    def read_data_at_time_at_level(self,var,t,z):     
        myFile = Dataset(self.filename, 'r')
        return myFile.variables[var][t][z][:]

    