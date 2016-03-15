# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os.path
import pandas
import logging
import numpy as np

class HymexReader:
       

    def __init__(self, hs,period):
        self.fileHS = hs
        self.filePeriod = period
        
    def read_data(self):
        
        if not os.path.isfile(self.fileHS):
            raise IOError(self.fileHS+" doesn't exists. Abort")   
        
        if not os.path.isfile(self.filePeriod):
            raise IOError(self.filePeriod+" doesn't exists. Abort") 

        hs = pandas.read_csv(self.fileHS,sep=";",usecols=[0,1],names=['time','sea_surface_wave_significant_height'])
        period = pandas.read_csv(self.filePeriod,sep=";",usecols=[0,1],names=['time','sea_surface_wave_mean_period'])
       
        data = pandas.merge(hs, period, how='left', on=['time'])
              
         # we process time record (drop duplicate...)
        duplicates = np.where(data.time.duplicated()== True)[0]       
        count = np.shape(duplicates)[0]             
        if count > 0:
            logging.warn('[CandhisReader] '+str(count)+' dates are duplicated. We drop them by keeping the first.') 
            data= data.drop_duplicates(subset='time',keep='first')
        data = data.set_index(pandas.DatetimeIndex(data['time'])) 
        data = data.drop('time',1)  
        
        return data