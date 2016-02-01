# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.Coverage import Coverage
from coverage.LevelCoverage import LevelCoverage
from coverage.TimeCoverage import TimeCoverage


class TimeLevelCoverage(Coverage,LevelCoverage,TimeCoverage):    
    
    def __init__(self, myReader):          
            
        Coverage.__init__(self,myReader);  
        LevelCoverage.__init__(self,myReader);  
        TimeCoverage.__init__(self,myReader);         
        
    
       

            
        
        
    

