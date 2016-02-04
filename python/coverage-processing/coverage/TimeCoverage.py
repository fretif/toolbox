# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.Coverage import Coverage
from datetime import timedelta
from datetime import datetime

class TimeCoverage(Coverage):
    """"""
    
    TIME_DATUM = datetime(1970, 1, 1)    
    TIME_DELTA = timedelta(minutes = 15)    

    def __init__(self, myReader):          
            
        Coverage.__init__(self,myReader);  
        self.times = self.read_axis_t();
   
    # Axis
    def find_time_index(self,t):
        """
        Si on trouve pas l'index, on retourne le premier
        """
        for i in xrange(self.get_t_size()):             
            if self.times[i] - t > TimeCoverage.TIME_DELTA:
                return i
        return 0
    
    def read_axis_t(self,timestamp=0):         
        return self.reader.read_axis_t(timestamp);  
    
    def get_t_size(self):
        return len(self.times);
    
    # Variables
    
    # HYDRO    
    def read_variable_wlv_at_time(self,t):    
        """
        Lecture de ssh
        """        
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
            
        index=0
        return self.reader.read_variable_wlv_at_time(index)  
    
    # METEO 

            
        
        
    

