# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os.path
import pandas
import logging
import numpy as np
from utils.jdutil import jd_to_datetime
from utils.jdutil import date_to_jd

def parse(jd):
    return jd_to_datetime(float(jd)+HymexReader.TIME_DATUM)
    

class HymexReaderJulian:
    
    TIME_DATUM = date_to_jd(1999,01,01)

    def __init__(self, myFilename):
        self.filename = myFilename   
        
    def read_data(self):
        
        if not os.path.isfile(self.filename):
            raise IOError(self.filename+" doesn't exists. Abort")   

        data = pandas.read_csv(self.filename,sep="\s+",usecols=[0,12,13],names=['jd_time','sea_surface_wind_wave_significant_height','sea_surface_wind_wave_period'],na_values={"-9999.0","-9999.0000"},keep_default_na=False,parse_dates={'time':['jd_time']},date_parser=parse)
      
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