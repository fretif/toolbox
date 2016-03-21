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
import logging
import pandas
from datetime import datetime

if __name__ == "__main__":
    """
    Cette routine permet d'extraire une série temporelle en un point donné et d'écrire les résultats dans un fichier texte.
    """
    print("Extract time series from Mercator")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file
    reader = MercatorReader('/home/retf/work/fieldsites/med-cruesim/modelling/mercator/grid/mercator_grid.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/mercator-grid2D-2012-2013.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/mercator-gridT-2012-2013.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/mercator-gridU-2012-2013.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/mercator-gridV-2012-2013.nc')

    coverage = TimeLevelCoverage(reader);
    
    # Calculate nearest point (Lion buoy lon/lat)    
    nearestPoint = coverage.find_point_index(4.640000,42.060000) 
    logging.info("Nearest point : "+str(nearestPoint[2])+" / "+str(nearestPoint[3])+" at "+str(nearestPoint[2])+" km") 
    
    # Date range to be extracted
    dates = pandas.date_range(start='2012-01-01 12:00:00', end='2012-01-04 12:00:00',freq='24H')
    z_level = 0 #surface
    
    # Prepare file to save
    file = open("/tmp/output", "w")  
    file.write("#date (UTC) \t longitude \t latitude \t u comp (m/s) \t v comp (m/s) \t ssh above geoid (m) \n")         
    
    for date in dates:
        
        logging.info(date) 
        myDate = datetime(date.year,date.month,date.day,date.hour,date.minute,date.second)  
        
        cur = coverage.read_variable_current_at_time_and_level(myDate,z_level)
        u_cur = cur[0][nearestPoint[0],nearestPoint[1]]
        v_cur = cur[1][nearestPoint[0],nearestPoint[1]]
        ssh = coverage.read_variable_ssh_at_time(myDate)[nearestPoint[0],nearestPoint[1]]
        
        file.write(str(date)+"\t"+str(nearestPoint[2])+"\t"+str(nearestPoint[3])+"\t"+str(u_cur)+"\t"+str(v_cur)+"\t"+str(ssh)+"\n") 
        
    file.close()
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
