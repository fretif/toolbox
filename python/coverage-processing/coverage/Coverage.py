# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

class Coverage:  
    """Coverage is a XY coverage."""
   
    def __init__(self, myReader):          
            
        self.reader = myReader; 
        
    def read_axis_x(self): 
        return self.reader.read_axis_x()
        
    def read_axis_y(self): 
        return self.reader.read_axis_y()
    
    def get_x_size(self):
        return len(self.read_axis_x()[0]);
    
    def get_y_size(self):
        return len(self.read_axis_y());
    
    def read_data(self,var):     
        """
        Read data
        """        
        return self.reader.read_data(var)
        
        