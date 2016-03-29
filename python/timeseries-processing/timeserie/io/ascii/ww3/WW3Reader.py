#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# TimeSeriesProcessing is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# TimeSeriesProcessing is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

import os.path
import pandas
import logging
import numpy as np
from datetime import datetime

def parse(d,H,M,S):
    return datetime(int(d[0:4]),int(d[4:6]),int(d[6:8]),int(H),int(M),int(S))

class WW3Reader:

    def __init__(self, myFilename):
        self.filename = myFilename   
        
    def read_data(self):
        
        if not os.path.isfile(self.filename):
            raise IOError(self.filename+" doesn't exists. Abort")   

        data = pandas.read_csv(self.filename,usecols=[0,1,2,3,4,6,7],names=['date','hour','minute','second','sea_surface_wave_significant_height','sea_surface_wave_mean_period','sea_surface_wave_from_direction'],sep="\s+",header=2,parse_dates={'time':['date','hour','minute','second']},date_parser=parse,keep_default_na=False)
        
        # we process time record (drop duplicate...)
        duplicates = np.where(data.time.duplicated()== True)[0]       
        count = np.shape(duplicates)[0]             
        if count > 0:
            logging.warn('[WW3Reader] '+str(count)+' dates are duplicated. We drop them by keeping the first.')
            data= data.drop_duplicates(subset='time',keep='first')
        data = data.set_index(pandas.DatetimeIndex(data['time'])) 
        data = data.drop('time',1)     
       
        return data