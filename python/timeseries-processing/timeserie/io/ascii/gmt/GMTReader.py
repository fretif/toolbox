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
    return datetime(int(time[0:4]),int(time[5:7]),int(time[8:10]),int(time[11:13]),int(time[14:16]),int(time[17:19]))

class GMTReader:

    def __init__(self, myFilename):
        self.filename = myFilename   
        
    def read_data(self):
        
        if not os.path.isfile(self.filename):
            raise IOError(self.filename+" doesn't exists. Abort")   

        data = pandas.read_csv(self.filename,usecols=[0,1],names=['pretime','sea_surface_height'],sep='\s+',na_values={"NaN",},parse_dates={'time':['pretime']},date_parser=parse,keep_default_na=False,comment='#')
        #data = pandas.read_csv(self.filename,usecols=[0,1,2],names=['pretime','sea_surface_wave_significant_height','sea_surface_wave_mean_period'],sep='\s+',na_values={"NaN",},parse_dates={'time':['pretime']},date_parser=parse,keep_default_na=False,comment='#')
        #data = pandas.read_csv(self.filename,usecols=[0,1],names=['pretime','wind_speed_10m'],sep='\s+',na_values={"NaN",},parse_dates={'time':['pretime']},date_parser=parse,keep_default_na=False,comment='#')

        # we process time record (drop duplicate...)
        duplicates = np.where(data.time.duplicated()== True)[0]       
        count = np.shape(duplicates)[0]    
        if count > 0:
            logging.warn('[GMTReader] '+str(count)+' dates are duplicated. We drop them by keeping the first.')
            data= data.drop_duplicates(subset='time',keep='first')
            
        data = data.set_index(pandas.DatetimeIndex(data['time'])) 
        data = data.drop('time',1)

        print data

        return data