#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# CoverageProcessing is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# CoverageProcessing is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

from coverage.io.File import File
from coverage.TimeCoverage import TimeCoverage
from netCDF4 import Dataset, num2date
import numpy as np
from datetime import datetime
from time import strftime
import logging

class ECMWFReader (File):

    def __init__(self, myFile):
        File.__init__(self,myFile);         
        self.ncfile = Dataset(self.filename, 'r')
        
    # Axis
    def read_axis_t(self,timestamp):
        data = self.ncfile.variables['time'][:]        
        result = num2date(data, units = self.ncfile.variables['time'].units, calendar = "gregorian")

        if timestamp ==1:
            return [ (t - TimeCoverage.TIME_DATUM).total_seconds() \
                for t in result];
        else:            
            return result;
    
    def read_axis_x(self):        
        return self.ncfile.variables['lon'][:]
    
    def read_axis_y(self):        
        return self.ncfile.variables['lat'][:]
    
    # Scalar 
    def read_variable_2D_mask(self):
        mask = self.ncfile.variables["LSM"][0][:]
        mask += 1.0 # inverse le mask
        mask %= 2 # inverse le mask
        return mask
    
    def read_variable_sp_at_time(self,t):
        sp = self.ncfile.variables["SP"][t][:]
        sp *= 0.01 # Pa to hPa
        return sp

    def read_variable_ssp_at_time(self,t):
        sp = self.ncfile.variables["MSL"][t][:]
        sp *= 0.01 # Pa to hPa
        return sp
    
    # Vector
    def read_variable_wind_at_time(self,t):
        return [self.ncfile.variables["U10M"][t][:], self.ncfile.variables["V10M"][t][:]]
    