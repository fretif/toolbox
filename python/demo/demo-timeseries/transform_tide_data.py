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
sys.path.append('../../timeseries-processing')

from timeserie.TimeSerie import TimeSerie
from timeserie.io.ascii.refmar.RefmarReader import RefmarReader
from timeserie.io.ascii.bessete.BesseteReader import BesseteReader
from timeserie.io.ascii.sirocco.SiroccoWriter import SiroccoWriter
from timeserie.io.ascii.puertos.PuertosTideReader import PuertosTideReader
import logging
import numpy as np

if __name__ == "__main__":
    print("Transform tide data to SIROCCO format")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    outDir="/tmp/"
    
    ## AJACCIO_ASPRETTO Données REFMAR

    reader = RefmarReader('/home/retf/work/fieldsites/med-cruesim/observations/sea-level/raw-data/REFMAR/Ajaccio_aspretto.txt')
    serie = TimeSerie(reader,'H','2010-01-01','2016-01-01');
    serie.name_station = "AJACCIO_ASPRETTO"
    serie.data_source = "SHOM / OCA / Marine nationale"
    serie.vertical_datum = "zero_hydrographique"
    serie.x_coord="8.76284981"
    serie.y_coord="41.92279816"
    logging.info(str(serie.name_station))  
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_tide_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_tide(serie)
      
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
