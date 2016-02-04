# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import numpy as np

class Coverage:  
    """"""
   
    def __init__(self, myReader):          
            
        self.reader = myReader; 
        
    # Axis        
    def read_axis_x(self): 
        """Return array[y:x]"""
        return self.reader.read_axis_x()
        
    def read_axis_y(self): 
        return self.reader.read_axis_y()
    
    def get_x_size(self):
        if self.is_regular_grid():
            return np.shape(self.read_axis_x())[0];
        else:
            return np.shape(self.read_axis_x())[1];
    
    def get_y_size(self):
        if self.is_regular_grid():
            return np.shape(self.read_axis_y())[0];
        else:
            return np.shape(self.read_axis_y())[0];
    
    def is_regular_grid(self):        
        if self.read_axis_x().ndim == 1:
            return True
        else:
            return False
    
    # Variables
    # HYDRO    
    def read_variable_bathymetry(self):     
        """
        Read data
        """        
        return self.reader.read_variable_bathymetry()
        
        