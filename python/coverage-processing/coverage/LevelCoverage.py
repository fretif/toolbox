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
import numpy as np
import logging

class LevelCoverage(Coverage):    
    """
La classe LevelCoverage est une extension de la classe Coverage.
Elle rajoute une dimension verticale à la couverture horizontale classique.
"""
    LEVEL_DELTA = 5; #meters
    
    def __init__(self, myReader):
        Coverage.__init__(self,myReader);
        self.levels = self.read_axis_z();
        self.last_index = None
        
    # Axis
    def read_axis_z(self):
        """Retourne les valeurs (souvent en mètre) de l'axe z.
    @return:  si la grille est en coordonnée sigma alors un tableau à trois dimensions [z,y,x] est retourné sinon
    un tableau une dimension [z]."""
        return self.reader.read_axis_z();

    def is_sigma_coordinate(self):
        """Retourne vrai si la grille verticale est en coordonnée sigma, sinon faux.
    @return:  vrai si la grille verticale est en coordonnée sigma sinon faux."""
        if self.levels.ndim == 3:
            return True
        elif self.levels.ndim == 1:
            return False
        else:
            raise ValueError("Unable to recognize the type of the vertical grid.")
    
    def get_z_size(self):
        """Retourne la taille de l'axe z.
    @return:  un entier correspondant à la taille de l'axe z."""
        return np.shape(self.levels)[0];
    
    def find_level_index(self,depth):
        """Retourne l'index de la profondeur la plus proche selon le point le plus proche.
    @type depth : integer ou flottant
    @param depth: Profondeur en mètre souhaitée ou index de la profondeur souhaitée
    @return:  un tableau de l'indice de la couche verticale inférieur la plus proche en chacun point de la grille. z < vert_coord[y,x] et z > vert_coord[y,x]+1.
    Les valeurs masquées valent -999."""

        xmax=self.get_x_size()
        ymax=self.get_y_size()
        vert_coord = []

        if type(depth) == int:

            if depth < 0 or depth >= self.get_z_size():
                raise ValueError("Depth index have to range between 0 and "+str(self.get_z_size()-1)+". Actually depth index = "+str(depth))

            if depth not in vert_coord:
                vert_coord.append(int(depth))

        elif self.is_sigma_coordinate() == True: # Cas de grille sigma

                for y in range(0,ymax):
                    for x in range(0,xmax):

                        # Pour chaque niveau
                        z=0
                        while z < self.get_z_size()-1 and self.levels[z,y,x] > depth:
                            z = z + 1

                        if self.levels[z,y,x] <= depth and z >= 0 and z < self.get_z_size()-1:

                            if z - 1 >= 0 and z - 1 not in vert_coord:
                                vert_coord.append(int(z - 1))
                            if z not in vert_coord:
                                vert_coord.append(int(z))
                            if z + 1 < self.get_z_size() and z + 1 not in vert_coord:
                                vert_coord.append(int(z + 1))
                        else :
                            logging.debug("[LevelCoverage] " + str(depth) + " m water depth was not found for the point [" + str(x) + "," + str(y) + "]. Max depth found is for this points is " + str(self.levels[z,y,x]))

        else: # Cas de grille classique

            # Pour chaque niveau
            z = 0
            while z < self.get_z_size() - 1 and self.levels[z] > depth:
                z = z + 1

            if self.levels[z] <= depth and z >= 0 and z < self.get_z_size() - 1:

                if z - 1 >= 0 and z - 1 not in vert_coord:
                    vert_coord.append(int(z - 1))
                if z not in vert_coord:
                    vert_coord.append(int(z))
                if z + 1 < self.get_z_size() and z + 1 not in vert_coord:
                    vert_coord.append(int(z + 1))
            else:
                raise ValueError(
                    "[LevelCoverage] " + str(depth) + " m water depth was not found in the grid. Abort.")

        # On retourne le tableau d'index
        return np.array(np.unique(vert_coord))


    def read_variable_3D_mask(self):
        """Retourne le masque terre/mer sur toute la couverture selon la profondeur z
    @return: un tableau en deux dimensions [z,y,x].
            0 = Terre
            1 = Mer
    """
        return self.reader.read_variable_3D_mask()
        
        
    

