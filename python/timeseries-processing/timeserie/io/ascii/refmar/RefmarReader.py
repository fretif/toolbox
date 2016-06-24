# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os.path
import pandas
import logging
import numpy as np
from datetime import datetime

def parse(date):
    return datetime(int(date[6:10]),int(date[3:5]),int(date[0:2]),int(date[11:13]),int(date[14:16]),int(date[17:18]))

class RefmarReader:

    def __init__(self, myFilename):
        self.filename = myFilename   
        
    def read_data(self):
        
        if not os.path.isfile(self.filename):
            raise IOError(self.filename+" doesn't exists. Abort")   

        data = pandas.read_csv(self.filename,usecols=[0,1],names=['date','sea_surface_height'],sep=';',header=13,parse_dates={'time':['date']},date_parser=parse)
        
        # we process time record (drop duplicate...)
        duplicates = np.where(data.time.duplicated()== True)[0]
        count = np.shape(duplicates)[0]
        if count > 0:
            logging.warn('[RefmarReader] '+str(count)+' dates are duplicated. We drop them by keeping the first.')
            data= data.drop_duplicates(subset='time',keep='first')
        data = data.set_index(pandas.DatetimeIndex(data['time']))
        data = data.drop('time',1)
       
        return data