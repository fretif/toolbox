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

# Lien vers le dossier de la lib
import sys
sys.path.append('../coverage-processing')

from coverage.Coverage import Coverage
from coverage.operator.interpolator.CoverageInterpolator import CoverageInterpolator
from coverage.io.netcdf.mesonh.MesoNhReader import MesoNhReader
import logging

if __name__ == "__main__":
    """
    Cette routine permet d'interpoler des résultats de Meso-NH sur une grille régulière.
    """
    print("Transform/Interpole WW3 to GMT ")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file
    reader = MesoNhReader('/home/retf/work/fieldsites/med-cruesim/modelling/atmosphere/AOC_500M_MED.nc')
        
    coverage = Coverage(reader);

    interpolator = CoverageInterpolator(coverage,0.005,0.005,'/home/retf/work/fieldsites/med-cruesim/modelling/atmosphere/test.nc') # résolution voulue en degrès
    interpolator.resample_variable_topography(coverage)
    interpolator.close()
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
