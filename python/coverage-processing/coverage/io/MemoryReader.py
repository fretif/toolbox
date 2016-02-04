# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

class MemoryReader: 
    
    def __init__(self,lon,lat,t,dat):         
        self.longitude = lon
        self.latitude = lat 
        self.time = t
        self.data = dat
     
    # Axis    
    def read_axis_x(self):        
        return self.longitude
    
    def read_axis_y(self):        
        return self.latitude
    
    def read_axis_t(self,timestamp): 
        if timestamp ==1:           
            return [ (t - TimeCoverage.TIME_DATUM).total_seconds() \
                for t in self.time];
        else:            
            return self.time
    
    # Data     
    def read_variable_wlv_at_time(self,t): 
        return self.data
