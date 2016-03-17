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

from coverage.io.netcdf.ww3.WW3Reader import WW3Reader
from coverage.io.netcdf.symphonie.SymphonieReader import SymphonieReader
from coverage.TimeLevelCoverage import TimeLevelCoverage
from coverage.TimeCoverage import TimeCoverage
import numpy as np
import logging

if __name__ == "__main__":
    """
    Cette routine permet de comparer les différences entre des grilles WaveWatch III et des grilles Symphonie
    """
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file
    ww3Reader = WW3Reader('/home/retf/work/fieldsites/med-cruesim/modelling/waves/gulf-of-lion/graphiques/ww3.20120701.nc')     
    ww3Coverage = TimeCoverage(ww3Reader);
    
    symphonieReader = SymphonieReader('/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/graphiques/grid.nc','/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/graphiques/20110320_000002.nc')
    symphonieCoverage = TimeLevelCoverage(symphonieReader);
    
    ww3Lon = ww3Coverage.read_axis_x()
    ww3Lat = ww3Coverage.read_axis_y()
    ww3Mask = ww3Coverage.reader.read_variable_mask();
    ww3Bathy = ww3Coverage.reader.read_variable_bathy_at_time(0);    
    symphonieLon = symphonieCoverage.read_axis_x()
    symphonieLat = symphonieCoverage.read_axis_y()
    symphonieMask = symphonieCoverage.reader.read_variable_mask();
    symphonieBathy = symphonieCoverage.reader.read_variable_bathymetry();
    
    logging.info("Grille Symphonie : "+str(symphonieCoverage.get_x_size())+"/"+str(symphonieCoverage.get_y_size()))
    logging.info("Grille WaveWatch III : "+str(ww3Coverage.get_x_size())+"/"+str(ww3Coverage.get_y_size()))
    
    for i in range(0, ww3Coverage.get_x_size()):
        for j in range(0, ww3Coverage.get_y_size()):
            
            if ww3Mask[j,i] == 2:
                ww3Mask[j,i] = 1                
            
            try:            
                np.testing.assert_approx_equal(symphonieLon[j,i],ww3Lon[j,i], 7)
                np.testing.assert_approx_equal(symphonieLat[j,i],ww3Lat[j,i],7)
                np.testing.assert_approx_equal(symphonieBathy[j,i],ww3Bathy[j,i],7)      
                np.testing.assert_approx_equal(symphonieMask[j,i],ww3Mask[j,i],0)
            except AssertionError:
                logging.warning(str(symphonieLon[j,i])+" "+str(symphonieLat[j,i])+" "+str(symphonieBathy[j,i])+" "+str(symphonieMask[j,i])+" !=  "+str(ww3Lon[j,i])+" "+str(ww3Lat[j,i])+" "+str(ww3Bathy[j,i])+" "+str(ww3Mask[j,i]))                
   
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
