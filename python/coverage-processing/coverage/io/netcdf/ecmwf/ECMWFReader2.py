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
# Author : Fabien Rétif - fabien.retif@zoho.com
#
from __future__ import division, print_function, absolute_import
from coverage.io.File import File
from coverage.TimeCoverage import TimeCoverage
from netCDF4 import Dataset, num2date
import numpy as np
from datetime import datetime
from time import strftime
import logging

class ECMWFReader2 (File):

    def __init__(self, myFile):
        File.__init__(self,myFile);         
        self.ncfile = Dataset(self.filename, 'r')
        # Pour tester les scale_factor
        #self.ncfile.variables["u10"].set_auto_maskandscale(False)
        #print self.ncfile.variables["u10"].maskandscale
        
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
        return self.ncfile.variables['longitude'][:]
    
    def read_axis_y(self):        
        return self.ncfile.variables['latitude'][:]
    
    # Scalar 
    def read_variable_2D_mask(self):
        mask = self.ncfile.variables["lsm"][0][:]
        mask += 1.0 # inverse le mask
        mask %= 2 # inverse le mask
        return mask
    
    def read_variable_sp_at_time(self,t):
        sp = self.ncfile.variables["sp"][t][:]
        sp *= 0.01 # Pa to hPa
        return sp

    def read_variable_ssp_at_time(self,t):
        sp = self.ncfile.variables["msl"][t][:]
        sp *= 0.01 # Pa to hPa
        return sp
    
    # Vector
    def read_variable_wind_at_time(self,t):
        return [self.ncfile.variables["u10"][t][:], self.ncfile.variables["v10"][t][:]]
    