#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# CoverageProcessing is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# CoverageProcessing is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

from coverage.Coverage import Coverage
from datetime import timedelta
from datetime import datetime

class TimeCoverage(Coverage):
    """La classe TimeCoverage est une extension de la classe Coverage.
Elle rajoute une dimension temporelle à la couverture horizontale classique.
    """
    
    TIME_DATUM = datetime(1970, 1, 1)    
    TIME_DELTA = timedelta(minutes = 15)    

    def __init__(self, myReader):          
            
        Coverage.__init__(self,myReader);  
        self.times = self.read_axis_t();
   
    # Axis
    def find_time_index(self,t):
        """Retourne l'index de la date la plus proche à TIME_DELTA prêt.
    @type t: datetime
    @param t: date souhaitée
    @return:  l'index de la date la plus proche à TIME_DELTA prêt ou une erreur si aucune date n'a pu être trouvée."""

        for i in xrange(self.get_t_size()):
            if self.times[i] - t > TimeCoverage.TIME_DELTA:
                return i

        raise ValueError(""+str(t)+" was not found. Maybe the TimeCoverage.TIME_DELTA ("+ str(TimeCoverage.TIME_DELTA)+") is too small or the date is out the range.")
    
    def read_axis_t(self,timestamp=0):
        """Retourne les valeurs de l'axe t.
    @param timestamp: égale 1 si le temps est souhaité en timestamp depuis TIME_DATUM.
    @return:  un tableau à une dimensions [z] au format datetime ou timestamp si timestamp=1."""
        return self.reader.read_axis_t(timestamp);  
    
    def get_t_size(self):
        """Retourne la taille de l'axe t.
    @return:  un entier correspondant à la taille de l'axe t."""
        return len(self.times);
    
    # Variables
    
    # HYDRO   
    def read_variable_ssh_at_time(self,t):
        """Retourne l'élévation de la surface libre à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;            
       
        return self.reader.read_variable_ssh_at_time(index)
    
    def read_variable_u_current_at_time(self,t):
        """Retourne la composante u du courant à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
            
        return self.reader.read_variable_u_current_at_time(index)
    
    def read_variable_v_current_at_time(self,t):
        """Retourne la composante v du courant à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
       
        return self.reader.read_variable_v_current_at_time(index)
    
    # WAVES
    def read_variable_hs_at_time(self,t):    
        """Retourne la hauteur significative des vagues à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
       
        return self.reader.read_variable_hs_at_time(index) 
    
    def read_variable_waves_dir_at_time(self,t):    
        """Retourne la direction des vagues à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
       
        return self.reader.read_variable_waves_dir_at_time(index) 
    
    def read_variable_waves_mean_period_at_time(self,t):    
        """Retourne la période moyenne des vagues à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
       
        return self.reader.read_variable_waves_mean_period_at_time(index) 
    
    def read_variable_j_pressure_at_time(self,t):    
        """Retourne la pression J due aux vagues à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
       
        return self.reader.read_variable_j_pressure_at_time(index) 
    
    def read_variable_u_surface_stokes_drift_at_time(self,t):    
        """Retourne la composante u de la dérive de Stokes en surface à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
            
        return self.reader.read_variable_u_surface_stokes_drift_at_time(index)  
    
    def read_variable_v_surface_stokes_drift_at_time(self,t):    
        """Retourne la composante v de la dérive de Stokes en surface à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
       
        return self.reader.read_variable_v_surface_stokes_drift_at_time(index) 
    
    def read_variable_u_taw_at_time(self,t):    
        """Retourne la composante u du tau atmosphere->vagues à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
            
        return self.reader.read_variable_u_taw_at_time(index)  
    
    def read_variable_v_taw_at_time(self,t):    
        """Retourne la composante v du tau atmosphere->vagues à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
       
        return self.reader.read_variable_v_taw_at_time(index) 
    
    def read_variable_u_two_at_time(self,t):    
        """Retourne la composante u du tau vagues->ocean à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
            
        return self.reader.read_variable_u_two_at_time(index)  
    
    def read_variable_v_two_at_time(self,t):    
        """Retourne la composante v du tau vagues->ocean à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
       
        return self.reader.read_variable_v_two_at_time(index) 
    
    # METEO 

            
        
        
    

