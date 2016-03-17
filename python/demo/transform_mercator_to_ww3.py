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
from coverage.io.netcdf.mercator.MercatorReader import MercatorReader
from coverage.io.netcdf.ww3.WW3Writer import WW3Writer
import logging

if __name__ == "__main__":
    """
    Cette routine permet de transformer les données du format Mercator à WaveWatch III en vu de forcer le modèle de vagues.
    """
    print("Transform MERCATOR to WW3")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file
    reader = MercatorReader('/home/retf/work/fieldsites/med-cruesim/modelling/mercator/grid/mercator_grid.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/mercator-grid2D-2012-2013.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/mercator-gridT-2012-2013.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/mercator-gridU-2012-2013.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/mercator-gridV-2012-2013.nc')      
        
    coverage = TimeLevelCoverage(reader); 
    
    writer = WW3Writer('/home/retf/work/fieldsites/med-cruesim/modelling/waves/med/config/cur/mercator-2012-2013.nc')
    writer.write_axis(coverage);    
    writer.write_variable_ssh(coverage);
    writer.write_variable_current_at_level(coverage,0);   
    writer.close()    
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
