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
from timeserie.io.ascii.candhis.CandhisReader import CandhisReader
from timeserie.io.ascii.bessete.BesseteReader import BesseteReader
from timeserie.io.ascii.hymex.HymexReader import HymexReader
from timeserie.io.ascii.puertos.PuertosOceanReader import PuertosOceanReader
from timeserie.io.ascii.puertos.PuertosWavesReader import PuertosWavesReader
from timeserie.io.ascii.sirocco.SiroccoWriter import SiroccoWriter
import logging

if __name__ == "__main__":
    print("Transform waves data to SIROCCO format")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)

    sourceDir = "./"
    outDir="/tmp/"

    ## Bouée_1
    reader = CandhisReader(sourceDir+'CANDHIS_wave_data.csv')
    serie = TimeSerie(reader,'30min','2013-12-09 00:00:00','2013-12-10 00:00:00');
    serie.name_station = "Bouée_1"
    serie.data_source = "CANDHIS"
    serie.meta_data="Burst = 26 min\n" \
                    "# Ligne 1 \n" \
                    "# Ligne 2"
    serie.x_coord="3.65"
    serie.y_coord="41.92"
    logging.info(str(serie.name_station))
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_wave_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_waves(serie)
      
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
