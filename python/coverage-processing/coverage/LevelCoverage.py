# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.Coverage import Coverage

class LevelCoverage(Coverage):
    
    LEVEL_DELTA = 100; #meters
    
    def __init__(self, myReader):          
            
        Coverage.__init__(self,myReader);         
        
    def read_axis_z(self):         
        return self.reader.read_axis_z(); 
    
    def get_z_size(self):
        return len(self.read_axis_z());
        
    def find_level_index(self,z):   
        """
        TODO
        """
        print len(self.levels)
        for i in xrange(len(self.levels)):     
            print self.levels[i]
            if self.levels[i] - z > LevelCoverage.LEVEL_DELTA:
                return i
        
    def read_data_at_level(self,var,z):     
        """
        #Read data at a specified level. We find the index index at TIME_DELTA
        """
        
        #index = self.find_level_index(z);
        index = z
        return self.reader.read_data_at_level(var,index)           
        
        
    

