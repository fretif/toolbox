# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import numpy as np
import math
 
def distance_on_unit_sphere(long1, lat1,long2, lat2):
 
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
 
    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc

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
        
    def find_point_index(self,x,y):
        """Return array[nearest_i_index,nearest_j_index,nearest_lon,nearest_lat,min_dist_in_km]"""
        min_dist=10000000
        lon = self.read_axis_x()
        lat = self.read_axis_y()
        
        nearest_i_index = 0
        nearest_j_index = 0
        
        for i in range(0, self.get_x_size()):
            for j in range(0, self.get_y_size()):    
        
                dist = distance_on_unit_sphere(x,y,lon[j,i],lat[j,i])
                if dist < min_dist:
                    min_dist = dist
                    nearest_lon = lon[j,i]
                    nearest_lat = lat[j,i]
                    nearest_i_index = i
                    nearest_j_index = j
		
        return [nearest_i_index,nearest_j_index,nearest_lon,nearest_lat,min_dist*6373]
    
    # Variables
    # HYDRO    
    def read_variable_bathymetry(self):     
        """
        Read bathymetry
        """        
        return self.reader.read_variable_bathymetry()
    
    def read_variable_mesh_size(self):     
        """
        Read mesh size
        """        
        return self.reader.read_variable_mesh_size()
    
    def read_variable_mask(self):     
        """
        Read mask
        """        
        return self.reader.read_variable_mask()
    
    # ATMOS    
    def read_variable_topography(self):     
        """
        Read topography
        """        
        return self.reader.read_variable_topography()
        
        