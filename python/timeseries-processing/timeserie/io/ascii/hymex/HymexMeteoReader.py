# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os.path
import pandas
import logging
import numpy as np
from datetime import datetime

def parse(date):
    #print date[4:6]
    return datetime(int(date[0:4]),int(date[4:6]),int(date[6:8]),int(date[8:10]))

class HymexMeteoReader:
       

    def __init__(self, myFile):
        self.file = myFile
        
    def read_data(self):
        
        if not os.path.isfile(self.file):
            raise IOError(self.file+" doesn't exists. Abort")


        data = pandas.read_csv(self.file,sep=" ",usecols=[1,12,14,22],names=['date','wind_to_direction_10m','wind_speed_10m','sea_surface_pressure'],na_values={-999},parse_dates={'time':['date']},date_parser=parse)
              
        # we process time record (drop duplicate...)
        duplicates = np.where(data.time.duplicated()== True)[0]       
        count = np.shape(duplicates)[0]             
        if count > 0:
            logging.warn('[HymexMeteoReader] '+str(count)+' dates are duplicated. We drop them by keeping the first.')
            data= data.drop_duplicates(subset='time',keep='first')
        data = data.set_index(pandas.DatetimeIndex(data['time'])) 
        data = data.drop('time',1)
        
        return data