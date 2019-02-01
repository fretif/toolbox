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
     
    