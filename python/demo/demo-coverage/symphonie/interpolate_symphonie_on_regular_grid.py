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
from coverage.operator.interpolator.InterpolatorCore import InterpolatorCore
from coverage.io.netcdf.symphonie.SymphonieReader import SymphonieReader
import logging

if __name__ == "__main__":
    print("Transform/Interpole Symphonie to GMT")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file
    reader = SymphonieReader('/home/fabien/grille.nc',
                             '/home/fabien/symphonie_var.nc')

    coverage = TimeLevelCoverage(reader);

    #InterpolatorCore.HORIZONTAL_INTERPOLATION_METHOD = = "linear";
    InterpolatorCore.HORIZONTAL_INTERPOLATION_METHOD = "nearest";
    InterpolatorCore.VERTICAL_INTERPOLATION_METHOD = "linear";

    interpolator = CoverageInterpolator(coverage,0.1,0.1,'/tmp/symphonie_3dcurrent-regular.nc',
                                        [0.0,500.0]) # résoluti1on voulue en degrès

    interpolator.resample_variable_current_at_depths()
    #interpolator.resample_variable_salinity_at_depths()
    #interpolator.resample_variable_ssh()
    #interpolator.resample_variable_current()
    #interpolator.resample_variable_2D_mask()
    #interpolator.resample_variable_waves_dir()
    #interpolator.resample_variable_hs()
    #interpolator.resample_variable_wind()
    #interpolator.resample_variable_mesh_size()
    #interpolator.resample_variable_wetmask()
    interpolator.close()
    
    print('End of programm')
     
    
    
    
       
        
    
    
    
    
    
