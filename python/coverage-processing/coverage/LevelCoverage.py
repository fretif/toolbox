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

class LevelCoverage(Coverage):    
    """
La classe LevelCoverage est une extension de la classe Coverage.
Elle rajoute une dimension verticale à la couverture horizontale classique.
"""
    LEVEL_DELTA = 0.1; #meters
    
    def __init__(self, myReader):
        Coverage.__init__(self,myReader);
        self.levels = self.read_axis_z();
        
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
    
    def find_level_index(self,z):
        """Retourne l'index de la profondeur la plus proche selon le point le plus proche.
    @type z : integer ou flottant
    @param z: Profondeur en mètre souhaitée ou index de la profondeur souhaitée
    @return:  un tableau de l'indice de la couche verticale la plus proche en chacun point de la grille."""

        xmax=self.get_x_size()
        ymax=self.get_y_size()
        vert_coord = np.zeros([ymax,xmax],dtype=int)
        vert_coord[:] = np.NAN

        if type(z) == int:

            vert_coord[:] = z

        elif self.is_sigma_coordinate() == True: # Cas de grille sigma

            raise RuntimeError("No implemented yet. Please give a vertical index")

            near_vert_layer = np.NAN

            for y in range(0,ymax):

                # On cherche le premier index de grille qui correspond à la profondeur souhaitée
                if (np.isnan(near_vert_layer)): # Si on n'a pas trouvé, on continue

                    for x in range(0,xmax):

                        if (np.isnan(near_vert_layer)): # Si on n'a pas trouvé, on continue

                            # Pour chaque niveau
                            for i in range(0,self.get_z_size()):
                                try:
                                    # On test à la deuxième décimale prêt
                                    print self.levels[i,y,x],z
                                    np.testing.assert_approx_equal(self.levels[i,y,x],z, 2)
                                    near_vert_layer = i
                                    break;
                                except AssertionError:
                                    # Sinon on cherche au delta prêt
                                    if self.levels[i,y,x] - z > LevelCoverage.LEVEL_DELTA:
                                        near_vert_layer = i
                                        break;

                        else:
                            break;
                else:
                    break;

            # Test si on l'a trouvé sinon on lance une erreur
            if (np.isnan(near_vert_layer)):
                 raise ValueError(""+str(z)+" was not found. Maybe the LevelCoverage.LEVEL_DELTA ("+ str(LevelCoverage.LEVEL_DELTA)+"m) is too small or the depth is out the range.")

            # On recommence pour toute la grille
            for y in range(0,ymax):
                for x in range(0,xmax):

                    # Pour chaque niveau entre -5 et +5 du niveau le plus proche
                    for i in range(near_vert_layer-5,near_vert_layer + 5):
                        try:
                            # On test à la deuxième décimale prêt
                            print np.shape(self.levels),i,y,x
                            np.testing.assert_approx_equal(self.levels[i,y,x],z, 2)
                            vert_coord[y,x] = i
                            break;
                        except AssertionError:
                            # Sinon on cherche au delta prêt
                            if self.levels[i,y,x] - z > LevelCoverage.LEVEL_DELTA:
                                vert_coord[y,x] = i
                                break;

        else: # Cas de grille classique

            near_vert_layer = np.NAN

            for i in xrange(self.get_z_size()):

                if (np.isnan(near_vert_layer)):

                    try:
                        # On test à la deuxième décimale prêt
                        np.testing.assert_approx_equal(self.levels[i],z, 2)
                        near_vert_layer= i
                    except AssertionError:
                        # Sinon on cherche au delta prêt
                        if self.levels[i] - z > LevelCoverage.LEVEL_DELTA:
                            near_vert_layer = i
                else:
                    break;

            if (np.isnan(near_vert_layer)):
                raise ValueError(""+str(z)+" was not found. Maybe the LevelCoverage.LEVEL_DELTA ("+ str(LevelCoverage.LEVEL_DELTA)+"m) is too small or the depth is out the range.")
            else:
                vert_coord[:] = near_vert_layer

        # On retourne le tableau d'index
        return vert_coord
        
        
    

