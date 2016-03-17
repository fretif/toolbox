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
from coverage.LevelCoverage import LevelCoverage
from coverage.TimeCoverage import TimeCoverage
from datetime import datetime


class TimeLevelCoverage(Coverage,LevelCoverage,TimeCoverage): 
    """La classe TimeLevelCoverage est une extension de la classe Coverage, LevelCoverage, TimeCoverage.
Elle rajoute les dimensions temporelle et verticale à la couverture horizontale classique.
    """
    def __init__(self, myReader):          
            
        Coverage.__init__(self,myReader);  
        LevelCoverage.__init__(self,myReader);  
        TimeCoverage.__init__(self,myReader);
        
    # Variables

    # HYDRO
    def read_variable_u_current_at_time_and_level(self,t,z):    
        """Retourne la composante u du courant à la date souhaitée et au niveau souhaité sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @type z: number
    @param z: profondeur souhaitée - index de la couche
    @return: un tableau en deux dimensions [y,x]."""
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;

        return self.reader.read_variable_u_current_at_time_and_level(index,z) 
    
    def read_variable_v_current_at_time_and_level(self,t,z):    
        """Retourne la composante v du courant à la date souhaitée et au niveau souhaité sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @type z: number
    @param z: profondeur souhaitée - index de la couche
    @return: un tableau en deux dimensions [y,x]."""
        if type(t) == datetime:
            index = self.find_time_index(t);
        else:
            index = t;
            
        return self.reader.read_variable_v_current_at_time_and_level(index,z)
    
       

            
        
        
    

