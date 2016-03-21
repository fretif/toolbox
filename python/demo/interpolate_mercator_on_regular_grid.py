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

from coverage.TimeLevelCoverage import TimeLevelCoverage
from coverage.operator.interpolator.CoverageInterpolator import CoverageInterpolator
from coverage.io.netcdf.mercator.MercatorReader import MercatorReader
import logging

if __name__ == "__main__":
    print("Transform/Interpole Symphonie to GMT")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file
    reader = MercatorReader('/home/retf/work/fieldsites/med-cruesim/modelling/mercator/grid/mercator_grid.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/pool/ext-PSY2V4R4_1dAV_20120706_20120707_grid2D_R20120711.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/pool/ext-PSY2V4R4_1dAV_20120706_20120707_gridT_R20120711.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/pool/ext-PSY2V4R4_1dAV_20120706_20120707_gridU_R20120711.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/pool/ext-PSY2V4R4_1dAV_20120706_20120707_gridV_R20120711.nc')


        
    coverage = TimeLevelCoverage(reader);

    interpolator = CoverageInterpolator(coverage,0.01,0.01,'/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/pool/test_resample.nc') # résolution voulue en degrès
    interpolator.resample_variable_current_at_level(coverage,150.0) # on peut donner la profondeur en mètres positifs ou en index de couche verticale.
    interpolator.resample_variable_ssh(coverage)
    interpolator.close()
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
