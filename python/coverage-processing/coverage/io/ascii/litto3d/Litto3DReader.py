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
import re
import array
from coverage.TimeCoverage import TimeCoverage
import numpy as np
from datetime import datetime
from time import strftime
import logging

class Litto3DReader (File):

    def __init__(self, myFile):
        File.__init__(self,myFile);
        self.metadata= {}

    # Meta data
    def read_metadata(self):
        count=0
        with open(self.filename) as f:
            line = f.readline().strip()
            while line and count < 6:

                if "ncols" in line:
                    self.metadata['ncols'] = int(re.sub('[^0-9-.]', '',line.rsplit(' ', 1)[1]))

                if "nrows" in line:
                    self.metadata['nrows'] = int(re.sub('[^0-9-.]', '',line.rsplit(' ', 1)[1]))

                if "xllcenter" in line:
                    self.metadata['xllcenter'] = float(re.sub('[^0-9-.]', '',line.rsplit(' ', 1)[1]))

                if "yllcenter" in line:
                    self.metadata['yllcenter'] = float(re.sub('[^0-9-.]', '',line.rsplit(' ', 1)[1]))

                if "cellsize" in line:
                    self.metadata['cellsize'] = float(re.sub('[^0-9-.]', '',line.rsplit(' ', 1)[1]))

                if "nodata_value" in line:
                    self.metadata['nodata_value'] = int(re.sub('[^0-9-.]', '',line.rsplit(' ', 1)[1]))

                line = f.readline()
                count += 1

        return self.metadata

    # Axis
    def read_axis_x(self):
        axis_x = np.zeros([self.metadata['ncols']])
        for i in range(len(axis_x)):
            axis_x[i] = self.metadata['xllcenter'] + i+1*self.metadata['cellsize']

        return axis_x
    
    def read_axis_y(self):        
        axis_y = np.zeros([self.metadata['nrows']])
        for i in range(len(axis_y)):
            axis_y[i] = self.metadata['yllcenter'] + i+1*self.metadata['cellsize']

        return axis_y
    
    # Scalar 
    def read_variable_bathymetry(self):
        var = np.zeros([self.metadata['ncols'],self.metadata['nrows']])
        var[:] = np.nan

        count=0
        nrows=0
        with open(self.filename) as f:
            line = f.readline().strip()
            while line:

                if count > 6 :

                    data = line.rsplit(' ')
                    var[nrows:]=data[1:]

                line = f.readline()
                count += 1
                nrows += 1

        return var
    

    