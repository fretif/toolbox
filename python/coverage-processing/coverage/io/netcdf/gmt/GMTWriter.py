# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.io.File import File
from netCDF4 import Dataset
from netCDF4 import date2num
from numpy import float32
from numpy import float64
import numpy as np

class GMTWriter (File):

    def __init__(self, myFile):   
        File.__init__(self,myFile); 
        self.ncfile = None
        
    def close(self):
        self.ncfile.close() 
        
    def write_axis(self,coverage):
        
        #assert
        if coverage.is_regular_grid()== False:
            raise IOError("This GMT writer is designed for regular grid. Please process to an interpolation")   
        
        self.ncfile = Dataset(self.filename, 'w', format='NETCDF4')
        self.ncfile.description = 'GMT Writer. Generated with Coverage Processing tools'

        # dimensions
        self.ncfile.createDimension('time', None)
        self.ncfile.createDimension('latitude', coverage.get_y_size())
        self.ncfile.createDimension('longitude', coverage.get_x_size())

        # variables
        times = self.ncfile.createVariable('time', float64, ('time',))
        times.units= 'seconds since 1970-01-01 00:00:00' 
        times.calendar= 'gregorian'
        times.standard_name= 'time'
        times.axis='T'
        times.conventions = "UTC time"
        
        latitudes = self.ncfile.createVariable('latitude', float32, ('latitude',))
        latitudes.units = "degree_north" ;
        latitudes.long_name = "latitude" ;
        latitudes.standard_name = "latitude" ;
        latitudes.valid_min = "-90.f";
        latitudes.valid_max = "90.f" ;
        latitudes.axis = "Y" ;
        
        longitudes = self.ncfile.createVariable('longitude', float32, ('longitude',))
        longitudes.units = "degree_east" ;
        longitudes.long_name = "longitude" ;
        longitudes.standard_name = "longitude" ;
        longitudes.valid_min = "-180.f" ;
        longitudes.valid_max = "180.f" ;
        longitudes.axis = "X" ; 
        
         # data  
        latitudes[:] = coverage.read_axis_y();        
        longitudes[:] = coverage.read_axis_x(); 
        times[:] = date2num(coverage.read_axis_t(), units = times.units, calendar = times.calendar)        
            
    def write_variable_wlv(self,coverage):
        if self.ncfile == None:
            raise IOError("Please call write_axis() first")   
            
        wlv = self.ncfile.createVariable('wlv', float32, ('time', 'latitude', 'longitude',),fill_value="NaN")
        wlv.long_name = "sea surface height above sea level" ;
        wlv.standard_name = "sea_surface_height_above_sea_level" ;
        wlv.globwave_name = "sea_surface_height_above_sea_level" ;
        wlv.units = "m" ;        
        #wlv.scale_factor = "1.f" ;
        #wlv.add_offset = "0.f" ;
        #wlv.valid_min = "0f" ;
        #wlv.valid_max = 10000f ; 
        
        time_index=0
        for time in coverage.read_axis_t():            
            wlv[time_index:time_index+1,:,:] = coverage.read_variable_wlv_at_time(time)
            time_index += 1
        
      
       
    