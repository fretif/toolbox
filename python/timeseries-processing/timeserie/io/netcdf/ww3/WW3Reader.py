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

import os.path
from netCDF4 import Dataset, num2date
import numpy as np
from datetime import datetime
from time import strftime
import logging
import pandas

class WW3Reader:

    def __init__(self, myFilename):
        self.filename = Dataset(myFilename, 'r')

    def read_data(self):

        data = self.filename.variables['time'][:]
        temp = num2date(data, units = self.filename.variables['time'].units, calendar = "julian")

        time = [ datetime.strptime(str(t), '%Y-%m-%d %H:%M:%S') \
                for t in temp];

        index = pandas.DatetimeIndex(time)

        hs = self.filename.variables['hs'][:,0]
        #sea_surface_wave_mean_period
        dir = self.filename.variables['th1m'][:,0]

        data = pandas.DataFrame({'sea_surface_wave_significant_height' : pandas.Series(hs, index=index),'sea_surface_wave_from_direction' : pandas.Series(dir, index=index)})
        print data
        return data


           
    