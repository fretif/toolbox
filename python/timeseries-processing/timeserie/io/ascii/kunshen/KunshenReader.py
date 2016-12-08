# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os.path
import pandas
import logging
import math
import numpy as np
from datetime import datetime

def parse(time):
    return datetime(int(time[0:4]),int(time[4:6]),int(time[6:8]),int(time[8:10]),int(time[10:12]),int(time[12:14]))

class KunshenReader:

    def __init__(self, myFilename):
        self.filename = myFilename   
        
    def read_data(self):
        
        if not os.path.isfile(self.filename):
            raise IOError(self.filename+" doesn't exists. Abort")   

        data = pandas.read_csv(self.filename,usecols=[1,4],names=['pretime','sea_surface_height'],sep='\t',na_values={"NaN",},parse_dates={'time':['pretime']},date_parser=parse,keep_default_na=False,comment='#')
        #data = pandas.read_csv(self.filename,usecols=[1,3,5],names=['pretime','sea_surface_wave_significant_height','sea_surface_wave_mean_period'],sep='\t',na_values={"NaN",},parse_dates={'time':['pretime']},date_parser=parse,keep_default_na=False,comment='#')

        # we process time record (drop duplicate...)
        duplicates = np.where(data.time.duplicated()== True)[0]       
        count = np.shape(duplicates)[0]    
        if count > 0:
            logging.warn('[KunshenReader] '+str(count)+' dates are duplicated. We drop them by keeping the first.')
            data= data.drop_duplicates(subset='time',keep='first')
            
        data = data.set_index(pandas.DatetimeIndex(data['time'])) 
        data = data.drop('time',1)

        #toMeters = lambda x:x*0.1
        #data['sea_surface_wave_mean_period'] = data['sea_surface_wave_mean_period'].apply(toMeters)

        return data