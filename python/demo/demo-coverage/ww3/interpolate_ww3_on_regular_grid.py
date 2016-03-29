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
sys.path.append('../../../coverage-processing')

from coverage.TimeCoverage import TimeCoverage
from coverage.operator.interpolator.CoverageInterpolator import CoverageInterpolator
from coverage.io.netcdf.ww3.WW3Reader import WW3Reader
import logging

if __name__ == "__main__":
    """
    Cette routine permet d'interpoler des résultats de WaveWatchIII sur une grille régulière.
    """
    print("Transform/Interpole WW3 to GMT ")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file
    reader = WW3Reader('/home/retf/work/fieldsites/med-cruesim/modelling/waves/med/outputs/netcdf/ww3.201103.nc')
        
    coverage = TimeCoverage(reader);

    interpolator = CoverageInterpolator(coverage,0.01,0.01,'/home/retf/work/fieldsites/med-cruesim/modelling/waves/med/outputs/netcdf/regular/ww3.201103.nc') # résolution voulue en degrès
    interpolator.resample_variable_current(coverage)
    interpolator.resample_variable_ssh(coverage)
    interpolator.close()
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
