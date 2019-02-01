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
# Author : Fabien Rétif - fabien.retif@zoho.com
#
from __future__ import division, print_function, absolute_import
from coverage.LevelCoverage import LevelCoverage
from coverage.TimeCoverage import TimeCoverage
from coverage.operator.interpolator.InterpolatorCore import vertical_interpolation
import numpy as np



class TimeLevelCoverage(LevelCoverage,TimeCoverage):
    """La classe TimeLevelCoverage est une extension de la classe Coverage, LevelCoverage, TimeCoverage.
Elle rajoute les dimensions temporelle et verticale à la couverture horizontale classique.
    """
    def __init__(self, myReader):

        LevelCoverage.__init__(self,myReader);  
        TimeCoverage.__init__(self,myReader);
        
    # Variables

    # HYDRO
    def read_variable_current_at_time_and_depth(self,time,depth):
        """Retourne les composantes u,v du courant à la date souhaitée et au niveau souhaité sur toute la couverture horizontale.
    @type time: datetime ou l'index
    @param time: date souhaitée
    @type depth: profondeur en mètre (float) ou index (integer)
    @param depth: profondeur souhaitée. Si le z est un entier, on considère qu'il s'agit de l'index,
    si c'est un flottant on considère qu'il s'agit d'une profondeur
    @return: un tableau en deux dimensions [u_comp,v_comp] contenant chacun deux dimensions [y,x]."""

        index_t = self.find_time_index(time);
        index_z = self.find_level_index(depth);

        xmax = self.get_x_size()
        ymax = self.get_y_size()
        layers = np.zeros([np.shape(index_z)[0],2, ymax, xmax])
        layers[::] = np.NAN

        results = np.zeros([2,ymax, xmax])
        results[:] = np.NAN

        targetDepth = [depth]
        candidateDepths = np.zeros([np.shape(index_z)[0]])

        for z in range(0, len(index_z)):
            layers[z] = self.reader.read_variable_current_at_time_and_depth(index_t, index_z[z])

        if np.shape(layers)[0] == 1:
            # Il n'y a qu'une seule couche donc pas d'interpolation possible
            results = layers[0,::]
        else:

            for y in range(0, ymax):
                for x in range(0, xmax):
                    for z in range(0, len(index_z)):
                        candidateDepths[z] = self.levels[index_z[z], y, x]

                    results[0][y, x] = vertical_interpolation(candidateDepths, targetDepth, layers[:,0, y, x])
                    results[1][y, x] = vertical_interpolation(candidateDepths, targetDepth, layers[:,1, y, x])

        return results

    def read_variable_salinity_at_time_and_depth(self,time,depth):
        """Retourne la salinité à la date souhaitée et au niveau souhaité sur toute la couverture horizontale.
    @type time: datetime ou l'index
    @param time: date souhaitée
    @type depth: profondeur en mètre (float) ou index (integer)
    @param depth: profondeur souhaitée. Si le z est un entier, on considère qu'il s'agit de l'index,
    si c'est un flottant on considère qu'il s'agit d'une profondeur
    @return: un tableau en deux dimensions [y,x]."""

        index_t = self.find_time_index(time);
        index_z = self.find_level_index(depth);

        xmax = self.get_x_size()
        ymax = self.get_y_size()
        layers = np.zeros([np.shape(index_z)[0],ymax, xmax])
        layers[::] = np.NAN

        results = np.zeros([ymax, xmax])
        results[:] = np.NAN

        targetDepth= [depth]
        candidateDepths = np.zeros([np.shape(index_z)[0]])

        for z in range(0, len(index_z)):
            layers[z] = self.reader.read_variable_salinity_at_time_and_depth(index_t, index_z[z])

        if np.shape(layers)[0] == 1:
            # Il n'y a qu'une seule couche donc pas d'interpolation possible
            results = layers[0,:]
        else:

            for y in range(0, ymax):
                for x in range(0, xmax):
                    for z in range(0,len(index_z)):
                        candidateDepths[z] = self.levels[index_z[z],y,x]

                    results[y, x] = vertical_interpolation(candidateDepths,targetDepth,layers[:,y,x])

        return results

    def read_variable_temperature_at_time_and_depth(self, time, depth):
        """Retourne la salinité à la date souhaitée et au niveau souhaité sur toute la couverture horizontale.
    @type time: datetime ou l'index
    @param time: date souhaitée
    @type depth: profondeur en mètre (float) ou index (integer)
    @param depth: profondeur souhaitée. Si le z est un entier, on considère qu'il s'agit de l'index,
    si c'est un flottant on considère qu'il s'agit d'une profondeur
    @return: un tableau en deux dimensions [y,x]."""

        index_t = self.find_time_index(time);
        index_z = self.find_level_index(depth);

        xmax = self.get_x_size()
        ymax = self.get_y_size()
        layers = np.zeros([np.shape(index_z)[0], ymax, xmax])
        layers[::] = np.NAN

        results = np.zeros([ymax, xmax])
        results[:] = np.NAN

        targetDepth = [depth]
        candidateDepths = np.zeros([np.shape(index_z)[0]])

        for z in range(0, len(index_z)):
            layers[z] = self.reader.read_variable_temperature_at_time_and_depth(index_t, index_z[z])

        if np.shape(layers)[0] == 1:
            # Il n'y a qu'une seule couche donc pas d'interpolation possible
            results = layers[0, :]
        else:

            for y in range(0, ymax):
                for x in range(0, xmax):
                    for z in range(0, len(index_z)):
                        candidateDepths[z] = self.levels[index_z[z], y, x]

                    results[y, x] = vertical_interpolation(candidateDepths, targetDepth, layers[:, y, x])

        return results
    
       

            
        
        
    

