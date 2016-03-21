# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os.path
import pandas
import logging
import math
import numpy as np
from datetime import datetime

def parse(y,m,d,H,M,S,SS):
    return datetime(int(y) + 2000,int(m),int(d),int(H),int(M),int(S),int(SS))    

class BesseteReader:

    def __init__(self, myFilename):
        self.filename = myFilename   
        
    def read_data(self):
        
        if not os.path.isfile(self.filename):
            raise IOError(self.filename+" doesn't exists. Abort")   

        data = pandas.read_csv(self.filename,usecols=[1,2,3,4,5,6,7,8,10,11,12,13],names=['year','month','day','hour','minute','second','millisecond','sea_surface_wave_significant_height','sea_surface_wave_peak_to_direction','sea_surface_height','sea_surface_wave_peak_period','sea_surface_wave_mean_period'],sep=',',na_values={"-1.0","-1.00"},keep_default_na=False,parse_dates={'time':['year','month','day','hour','minute','second','millisecond']},date_parser=parse)
      
        # we process time record (drop duplicate...)
        duplicates = np.where(data.time.duplicated()== True)[0]       
        count = np.shape(duplicates)[0]    
        if count > 0:
            logging.warn('[CandhisReader] '+str(count)+' dates are duplicated. We drop them by keeping the first.') 
            data= data.drop_duplicates(subset='time',keep='first')
            
        data = data.set_index(pandas.DatetimeIndex(data['time'])) 
        data = data.drop('time',1)   
        
        # Change ssh to meters       
        data['sea_surface_height'][data['sea_surface_height'] < 20000] = np.nan       
        toMeters = lambda x:(x - data['sea_surface_height'].mean())*0.001       
        data['sea_surface_height'] = data['sea_surface_height'].apply(toMeters)

        return data