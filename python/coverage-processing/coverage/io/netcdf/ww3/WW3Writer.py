# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from netCDF4 import Dataset
from utils.jdutil import jd_to_datetime
from utils.jdutil import date_to_jd
from numpy import ndarray
import datetime as datetime
from netCDF4 import num2date,date2num
from numpy import float64
from numpy import float32

class WW3Writer:
    
    TIME_DATUM = date_to_jd(1990,01,01)

    def __init__(self, myFile):   
        self.filename = myFile; 
        
    def write_coverage(self,coverage,variables):
        
        ncfile = Dataset(self.filename, 'w', format='NETCDF4')
        ncfile.description = 'Example temperature data'

        # dimensions
        ncfile.createDimension('time', None)
        ncfile.createDimension('latitude', coverage.get_y_size())
        ncfile.createDimension('longitude', coverage.get_x_size())

        # variables
        times = ncfile.createVariable('time', float64, ('time',))
        times.units= 'hours since 0001-01-01 00:00:00' 
        times.calendar= 'gregorian'
        
        latitudes = ncfile.createVariable('latitude', float32, ('latitude','longitude',))
        longitudes = ncfile.createVariable('longitude', float32, ('latitude','longitude',))
                
        var = ncfile.createVariable('lev', float32, ('time', 'latitude', 'longitude',))

        # data
        latitudes[:,:] = coverage.read_axis_y();
        
        print latitudes
        print coverage.read_axis_y().shape
        longitudes[::] = coverage.read_axis_x();
        #times[:] = date2num(coverage.read_axis_t(), units = times.units, calendar = times.calendar)
        #times[:] = 
        
        for time in coverage.read_axis_t(raw=1): 
            var[time,:,:] = coverage.read_data_at_time(variables,time);            
            

        # group
        # my_grp = root_grp.createGroup('my_group')

        ncfile.close()       
       
    