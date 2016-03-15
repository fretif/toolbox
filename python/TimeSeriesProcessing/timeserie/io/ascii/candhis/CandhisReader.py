# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os.path
import pandas
import logging
import math
import numpy as np

class CandhisReader:

    def __init__(self, myFilename):
        self.filename = myFilename   
        
    def read_data(self):
        
        if not os.path.isfile(self.filename):
            raise IOError(self.filename+" doesn't exists. Abort")   

        data = pandas.read_csv(self.filename,usecols=[0,1,23,28],names=['time','sea_surface_wave_significant_height','sea_surface_wave_mean_period','sea_surface_wave_from_direction'],sep=';',header=13)
        
        # we process time record (drop duplicate...)
        duplicates = np.where(data.time.duplicated()== True)[0]       
        count = np.shape(duplicates)[0]             
        if count > 0:
            logging.warn('[CandhisReader] '+str(count)+' dates are duplicated. We drop them by keeping the first.') 
            data= data.drop_duplicates(subset='time',keep='first')
        data = data.set_index(pandas.DatetimeIndex(data['time'])) 
        data = data.drop('time',1)    
        
        # reverse angle
       
        return data