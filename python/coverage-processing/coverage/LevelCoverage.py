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

class LevelCoverage(Coverage):    
    """
La classe LevelCoverage est une extension de la classe Coverage.
Elle rajoute une dimension verticale à la couverture horizontale classique.
"""
    LEVEL_DELTA = 100; #meters
    
    def __init__(self, myReader):
        Coverage.__init__(self,myReader);         
        
    # Axis
    def read_axis_z(self):
        """Retourne les valeurs (souvent en mètre) de l'axe z.
    @return:  un tableau à une dimension [z]."""
        return self.reader.read_axis_z(); 
    
    def get_z_size(self):
        """Retourne la taille de l'axe z.
    @return:  un entier correspondant à la taille de l'axe z."""
        return len(self.read_axis_z());
    
    def find_level_index(self,x,y,z):
        """Retourne l'index de la profondeur la plus proche selon le point le plus proche.
    @param x: Coordonnée en longitude du point souhaité
    @param y: Coordonnée en latitude du point souhaité
    @param z: Profondeur en mètre souhaitée
    @return:  un entier correspondant à l'index de la profondeur la plus proche."""
        raise RuntimeError("No implemented yet.")
        
        
    

