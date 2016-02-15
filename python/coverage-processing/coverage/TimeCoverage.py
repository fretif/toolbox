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
       
        return self.reader.read_variable_wlv_at_time(index)  
    
    def read_variable_u_surface_current_at_time(self,t):    
        """
        Lecture de la composante u du courant de surface
        """        
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
            
        return self.reader.read_variable_u_surface_current_at_time(index)  
    
    def read_variable_v_surface_current_at_time(self,t):    
        """
        Lecture de la composante v du courant de surface
        """        
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
       
        return self.reader.read_variable_v_surface_current_at_time(index)  
    
    # WAVES
    def read_variable_hs_at_time(self,t):    
        """
        Lecture de la hauteur significative des vagues
        """        
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
       
        return self.reader.read_variable_hs_at_time(index) 
    
    def read_variable_waves_dir_at_time(self,t):    
        """
        Lecture de la direction des vagues
        """        
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
       
        return self.reader.read_variable_waves_dir_at_time(index) 
    
    def read_variable_waves_mean_period_at_time(self,t):    
        """
        Lecture de la periode moyenne des vagues
        """        
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
       
        return self.reader.read_variable_waves_mean_period_at_time(index) 
    
    def read_variable_j_pressure_at_time(self,t):    
        """
        Lecture de la pression J
        """        
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
       
        return self.reader.read_variable_j_pressure_at_time(index) 
    
    def read_variable_u_surface_stokes_drift_at_time(self,t):    
        """
        Lecture de la composante u de la derive de Stokes en surface
        """        
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
            
        return self.reader.read_variable_u_surface_stokes_drift_at_time(index)  
    
    def read_variable_v_surface_stokes_drift_at_time(self,t):    
        """
        Lecture de la composante v de la derive de Stokes en surface
        """        
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
       
        return self.reader.read_variable_v_surface_stokes_drift_at_time(index) 
    
    def read_variable_u_taw_at_time(self,t):    
        """
        Lecture de la composante u du tau atmosphere->vagues
        """        
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
            
        return self.reader.read_variable_u_taw_at_time(index)  
    
    def read_variable_v_taw_at_time(self,t):    
        """
        Lecture de la composante v du tau atmosphere->vagues
        """        
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
       
        return self.reader.read_variable_v_taw_at_time(index) 
    
    def read_variable_u_two_at_time(self,t):    
        """
        Lecture de la composante u du tau vagues->ocean
        """        
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
            
        return self.reader.read_variable_u_two_at_time(index)  
    
    def read_variable_v_two_at_time(self,t):    
        """
        Lecture de la composante v du tau vagues->ocean
        """        
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
       
        return self.reader.read_variable_v_two_at_time(index) 
    
    # METEO 

            
        
        
    

