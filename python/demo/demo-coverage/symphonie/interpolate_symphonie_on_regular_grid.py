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

from coverage.TimeLevelCoverage import TimeLevelCoverage
from coverage.operator.interpolator.CoverageInterpolator import CoverageInterpolator
from coverage.io.netcdf.symphonie.SymphonieReader import SymphonieReader
import logging

if __name__ == "__main__":
    print("Transform/Interpole Symphonie to GMT")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file
    reader = SymphonieReader('GRAPHIQUES/grid.nc',
                             'GRAPHIQUES/20110320_000002.nc')

    coverage = TimeLevelCoverage(reader);

    interpolator = CoverageInterpolator(coverage,0.02,0.02,'GRAPHIQUES/20110220_regular.nc',
                                        []) # résolution voulue en degrès
    #interpolator = CoverageInterpolator(coverage,0.02,0.02,'GRAPHIQUES/20110220_regular.nc',
    #                                    [0.0,10.0,50.0,150.0,200.0,250.0,300.0,350.0,400.0,450.0,500.0,550.0,600.0,650.0,700.0,750.0,850.0,900.0,950.0,1000.0,1100.0,1200.0,1300.0,1400.0,1500.0,1600.0,1700.0,1800.0,1900.0,2000.0,2300.0,2400.0,2500.0,2600.0,2700.0,2850.0,2870.0]) # résolution voulue en degrès


    #interpolator.resample_variable_current_at_depths()
    interpolator.resample_variable_salinity_at_depths()
    #interpolator.resample_variable_ssh()
    #interpolator.resample_variable_current()
    #interpolator.resample_variable_2D_mask()
    #interpolator.resample_variable_waves_dir()
    #interpolator.resample_variable_hs()
    #interpolator.resample_variable_wind()
    #interpolator.resample_variable_mesh_size()
    #interpolator.resample_variable_wetmask()
    interpolator.close()
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
