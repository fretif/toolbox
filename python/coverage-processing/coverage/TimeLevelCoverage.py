# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.Coverage import Coverage
from coverage.LevelCoverage import LevelCoverage
from coverage.TimeCoverage import TimeCoverage
from datetime import datetime


class TimeLevelCoverage(Coverage,LevelCoverage,TimeCoverage): 
    """"""
    
    def __init__(self, myReader):          
            
        Coverage.__init__(self,myReader);  
        LevelCoverage.__init__(self,myReader);  
        TimeCoverage.__init__(self,myReader);
        
    # Variables
    def read_variable_u_current_at_time_and_level(self,t,z):    
        """
        Lecture de la composante u du courant
        """        
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
            
        return self.reader.read_variable_u_current_at_time_and_level(index,z) 
    
    def read_variable_v_current_at_time_and_level(self,t,z):    
        """
        Lecture de la composante v du courant
        """        
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
            
        return self.reader.read_variable_v_current_at_time_and_level(index,z)
    
       

            
        
        
    

