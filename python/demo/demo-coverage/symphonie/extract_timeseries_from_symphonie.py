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
from coverage.io.netcdf.symphonie.SymphonieReader import SymphonieReader
import logging
import pandas
from datetime import datetime

if __name__ == "__main__":
    """
    Cette routine permet d'extraire une série temporelle en un point donné et d'écrire les résultats dans un fichier texte.
    """
    print("Extract time series from Symphonie")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file
    reader = SymphonieReader('/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/graphiques/grid.nc','/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/graphiques/20110320_000002.nc')

    coverage = TimeLevelCoverage(reader);
    
    # Calculate nearest point (Lion buoy lon/lat)    
    nearestPoint = coverage.find_point_index(4.640000,42.060000) 
    logging.info("Nearest point : "+str(nearestPoint[2])+" / "+str(nearestPoint[3])+" at "+str(nearestPoint[2])+" km") 
    
    # Date range to be extracted
    dates = pandas.date_range(start='2011-03-19 23:00:00', end='2011-03-20 12:00:00',freq='3H')
    depth = 500.0 # 500 mètres de profondeur
    
    # Prepare file to save
    file = open("/tmp/output", "w")  
    file.write("#date (UTC) \t longitude \t latitude \t u comp (m/s) \t v comp (m/s) \t ssh above geoid (m) \n")         
    
    for date in dates:
        
        logging.info(date) 
        myDate = datetime(date.year,date.month,date.day,date.hour,date.minute,date.second)  
        
        cur = coverage.read_variable_current_at_time_and_level(myDate,depth)
        u_cur = cur[0][nearestPoint[0],nearestPoint[1]]
        v_cur = cur[1][nearestPoint[0],nearestPoint[1]]
        ssh = coverage.read_variable_ssh_at_time(myDate)[nearestPoint[0],nearestPoint[1]]
        
        file.write(str(date)+"\t"+str(nearestPoint[2])+"\t"+str(nearestPoint[3])+"\t"+str(u_cur)+"\t"+str(v_cur)+"\t"+str(ssh)+"\n") 
        
    file.close()
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
