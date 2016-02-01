# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from datetime import timedelta

class TYXCoverage:
    
    TIME_DELTA = timedelta(minutes = 15)

    def __init__(self, myReader):          
            
        self.reader = myReader; 
        self.times = myReader.read_axis_t();
        
    def get_times(self): 
        return self.times
        
    def find_time_index(self,t):
       
        for i in xrange(len(self.times)):        
            if self.times[i] - t > TYXCoverage.TIME_DELTA:
                return i
    
    def read_axis_x(self): 
        return self.reader.read_axis_x()
        
    def read_axis_y(self): 
        return self.reader.read_axis_y()
        
    def read_data_at_time(self,var,t):     
        """
        Read data at a specified time. We find the index index at TIME_DELTA
        """
        
        index = self.find_time_index(t);
        return self.reader.read_data_at_time(var,index)
       

            
        
        
    

