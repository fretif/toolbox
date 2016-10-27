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

class WW3UnstructuredReader (File):

    def __init__(self, xsize, ysize,myFile):
        File.__init__(self,myFile);         
        self.ncfile = Dataset(self.filename, 'r')
        self.x_size = xsize
        self.y_size = ysize
        
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
        return np.reshape(self.ncfile.variables['longitude'][:], (self.x_size, self.y_size))
    
    def read_axis_y(self):
        return np.reshape(self.ncfile.variables['latitude'][:], (self.x_size, self.y_size))
    
    # Scalar 
    def read_variable_2D_mask(self):
        return np.reshape(self.ncfile.variables["MAPSTA"][:], (self.x_size, self.y_size))
    
    def read_variable_bathymetry(self):
        return np.reshape(self.ncfile.variables["dpt"][0][:], (self.x_size, self.y_size))

    def read_variable_bathymetry_at_time(self,t):
        return np.reshape(self.ncfile.variables["dpt"][t][:], (self.x_size, self.y_size))
    
    def read_variable_wlv_at_time(self,t):         
        return np.reshape(self.ncfile.variables["wlv"][t][:], (self.x_size, self.y_size))
    
    def read_variable_hs_at_time(self,t):         
        return np.reshape(self.ncfile.variables["hs"][t][:], (self.x_size, self.y_size))
    
    def read_variable_waves_dir_at_time(self,t):         
        return np.reshape(self.ncfile.variables["dir"][t][:], (self.x_size, self.y_size))
    
    def read_variable_waves_mean_period_at_time(self,t):         
        return np.reshape(self.ncfile.variables["t01"][t][:], (self.x_size, self.y_size))
    
    def read_variable_j_pressure_at_time(self,t):         
        return np.reshape(self.ncfile.variables["bhd"][t][:], (self.x_size, self.y_size))
    
    # Vector
    def read_variable_current_at_time(self,t):
        logging.info('[WW3Reader] Reading surface current')
        return [np.reshape(self.ncfile.variables["ucur"][t][:], (self.x_size, self.y_size)) , np.reshape(self.ncfile.variables["vcur"][t][:], (self.x_size, self.y_size)) ]

    def read_variable_taw_at_time(self,t):
        return [np.reshape(self.ncfile.variables["utaw"][t][:], (self.x_size, self.y_size)) ,np.reshape(self.ncfile.variables["vtaw"][t][:], (self.x_size, self.y_size)) ]
    
    def read_variable_two_at_time(self,t):
        return [np.reshape(self.ncfile.variables["utwo"][t][:], (self.x_size, self.y_size)) ,np.reshape(self.ncfile.variables["vtwo"][t][:], (self.x_size, self.y_size)) ]

    def read_variable_surface_stokes_drift_at_time(self,t):
        return [np.reshape(self.ncfile.variables["uuss"][t][:], (self.x_size, self.y_size)) ,np.reshape(self.ncfile.variables["vuss"][t][:], (self.x_size, self.y_size)) ]

    def read_variable_wind_at_time(self,t):
        return [np.reshape(self.ncfile.variables["uwnd"][t][:], (self.x_size, self.y_size)) ,np.reshape(self.ncfile.variables["vwnd"][t][:], (self.x_size, self.y_size)) ]
           
    