# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.Coverage import Coverage
from datetime import timedelta
from datetime import date

class TimeCoverage(Coverage):
    
    TIME_DELTA = timedelta(minutes = 15)    

    def __init__(self, myReader):          
            
        Coverage.__init__(self,myReader);  
        
    def find_time_index(self,t):
       
        for i in xrange(self.get_t_size()):        
            if self.times[i] - t > TimeCoverage.TIME_DELTA:
                return i
    
    def read_axis_t(self,raw=0):         
        return self.reader.read_axis_t(raw);  
    
    def get_t_size(self):
        return len(self.read_axis_t());
        
    def read_data_at_time(self,var,t):     
        """
        Read data at a specified time. We find the index index at TIME_DELTA
        """
        if type(t) == date:
            index = self.find_time_index(t);
        else:
            index = t;
            
        return self.reader.read_data_at_time(var,index)  

            
        
        
    

