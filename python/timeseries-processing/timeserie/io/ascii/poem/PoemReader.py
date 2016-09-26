# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os.path
import pandas
import logging
import math
import numpy as np
from datetime import datetime

def parse(y,m,d,H,M,S):
    return datetime(int(y) + 2000,int(m),int(d),int(H),int(M),int(S))

class PoemReader:

    def __init__(self, myFilename):
        self.filename = myFilename   
        
    def read_data(self):
        
        if not os.path.isfile(self.filename):
            raise IOError(self.filename+" doesn't exists. Abort")   

        data = pandas.read_csv(self.filename,usecols=[0,1,2,3,4,5,6,10,13,14,16],names=['year','month','day','hour','minute','second','sea_surface_wave_significant_height','sea_surface_wave_mean_period','sea_surface_wave_peak_period','sea_surface_wave_peak_to_direction','sea_surface_height'],sep=',',na_values={"-3072.0","2048.0","-2130.5",},keep_default_na=False,parse_dates={'time':['year','month','day','hour','minute','second']},date_parser=parse,comment='#')
        #data = pandas.read_csv(self.filename,usecols=[1,2,3,4,5,6,9],names=['year','month','day','hour','minute','second','sea_surface_wave_significant_height'],sep=',',na_values={"-99",},keep_default_na=False,parse_dates={'time':['year','month','day','hour','minute','second']},date_parser=parse,comment='#')
      
        # we process time record (drop duplicate...)
        duplicates = np.where(data.time.duplicated()== True)[0]       
        count = np.shape(duplicates)[0]    
        if count > 0:
            logging.warn('[PoemReader] '+str(count)+' dates are duplicated. We drop them by keeping the first.')
            data= data.drop_duplicates(subset='time',keep='first')
            
        data = data.set_index(pandas.DatetimeIndex(data['time'])) 
        data = data.drop('time',1)

        return data