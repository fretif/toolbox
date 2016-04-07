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
import pandas
import logging
import numpy as np
from datetime import datetime

def parse(y,m,d,H):
    return datetime(int(y),int(m),int(d),int(H))

class PuertosWavesReader:
    """
    Lecteur des données de vagues du format PUERTOS
    """

    def __init__(self, myFilename):
        self.filename = myFilename   
        
    def read_data(self):
        
        if not os.path.isfile(self.filename):
            raise IOError(self.filename+" doesn't exists. Abort")   

        data = pandas.read_csv(self.filename,usecols=[0,1,2,3,4,7,8,12,13,18],names=['year','month','day','hour','sea_surface_wave_significant_height','sea_surface_wave_mean_period','sea_surface_wave_peak_period','sea_surface_wave_from_direction','sea_surface_wave_peak_from_direction','sea_surface_temperature'],sep='\s+',header=85,na_values={"-99.9"},keep_default_na=False,parse_dates={'time':['year','month','day','hour']},date_parser=parse)
        
        # we process time record (drop duplicate...)
        duplicates = np.where(data.time.duplicated()== True)[0]       
        count = np.shape(duplicates)[0]             
        if count > 0:
            logging.warn('[PuertosOceanReader] '+str(count)+' dates are duplicated. We drop them by keeping the first.')
            data= data.drop_duplicates(subset='time',keep='first')
        data = data.set_index(pandas.DatetimeIndex(data['time'])) 
        data = data.drop('time',1)
       
        return data