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
    @type t: datetime ou int
    @param t: date souhaitée ou l'index de la date souhaitée
    @return:  l'index de la date la plus proche à TIME_DELTA prêt ou une erreur si aucune date n'a pu être trouvée."""

        if type(t) == int:
            return t;
        elif type(t) == datetime:
            zero_delta = timedelta(minutes = 00)
            for i in range(0,self.get_t_size()):
                if t - self.times[i] == zero_delta or t - self.times[i] < TimeCoverage.TIME_DELTA:
                    return i

            raise ValueError(""+str(t)+" was not found. Maybe the TimeCoverage.TIME_DELTA ("+ str(TimeCoverage.TIME_DELTA)+") is too small or the date is out the range.")
        else:
            raise ValueError(""+str(t)+" have to be an integer or a datetime.")
    
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

        index_t = self.find_time_index(t);
       
        return self.reader.read_variable_ssh_at_time(index_t)

    def read_variable_bathy_ssh_at_time(self,t):
        """Retourne l'élévation de la surface libre + la bathy à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_bathy_ssh_at_time(index_t)
    
    def read_variable_current_at_time(self,t):
        """Retourne les composantes u,v du courant à la date souhaitée
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [u_comp,v_comp] contenant chacun deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_current_at_time(index_t)
    
    # WAVES
    def read_variable_hs_at_time(self,t):    
        """Retourne la hauteur significative des vagues à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_hs_at_time(index_t)
    
    def read_variable_waves_dir_at_time(self,t):    
        """Retourne la direction des vagues à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_waves_dir_at_time(index_t)

    def read_variable_waves_breaking_height_at_time(self,t):
        """Retourne la hauteur de déferlement des vagues à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_waves_breaking_height_at_time(index_t)

    def read_variable_waves_to_ocean_energy_flux_at_time(self,t):
        """Retourne la waves_to_ocean_energy_flux à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_waves_to_ocean_energy_flux_at_time(index_t)
    
    def read_variable_waves_mean_period_at_time(self,t):    
        """Retourne la période moyenne des vagues à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_waves_mean_period_at_time(index_t)

    def read_variable_waves_peak_frequency_at_time(self,t):
        """Retourne la fréquence du pic des vagues à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_waves_peak_frequency_at_time(index_t)
    
    def read_variable_j_pressure_at_time(self,t):    
        """Retourne la pression J due aux vagues à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_j_pressure_at_time(index_t)
    
    def read_variable_surface_stokes_drift_at_time(self,t):
        """Retourne la dérive de Stokes en surface à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_surface_stokes_drift_at_time(index_t)

    def read_variable_waves_bottom_dissipation_at_time(self,t):
        """Retourne la l'énergie des vagues dissipée par le fond à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_waves_bottom_dissipation_at_time(index_t)

    
    def read_variable_taw_at_time(self,t):
        """Retourne la composante u du tau atmosphere->vagues à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_taw_at_time(index_t)
    
    def read_variable_two_at_time(self,t):
        """Retourne la composante u du tau vagues->ocean à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_two_at_time(index_t)
    
    # METEO
    def read_variable_sp_at_time(self,t):
        """Retourne la pression à la surface à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_sp_at_time(index_t)

    def read_variable_ssp_at_time(self,t):
        """Retourne la pression à la surface de la mer (sea surface pressure) à la date souhaitée sur toute la couverture horizontale.
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_ssp_at_time(index_t)

    def read_variable_wind_at_time(self,t):
        """Retourne les composantes u,v du vent à la date souhaitée
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [u_comp,v_comp] contenant chacun deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_wind_at_time(index_t)

    def read_variable_wetmask_at_time(self,t):
        """Retourne le masque de bancs découvrant à la date souhaitée
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_wetmask_at_time(index_t)

    def read_variable_wind_stress_at_time(self, t):
        """Retourne les composantes u,v de la contrainte de vent à la date souhaitée
    @type t: datetime ou l'index
    @param t: date souhaitée
    @return: un tableau en deux dimensions [u_comp,v_comp] contenant chacun deux dimensions [y,x]."""

        index_t = self.find_time_index(t);

        return self.reader.read_variable_wind_stress_at_time(index_t)

            
        
        
    

