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
sys.path.append('../../../timeseries-processing')

from timeserie.TimeSerie import TimeSerie
from coverage.TimeLevelCoverage import TimeLevelCoverage
from coverage.io.netcdf.mercator.MercatorReader import MercatorReader
from timeserie.io.ascii.sirocco.SiroccoWriter import SiroccoWriter
from timeserie.io.MemoryReader import MemoryReader
import logging
from pandas import Series, DataFrame
from datetime import datetime

if __name__ == "__main__":
    """
    Cette routine permet d'extraire une série temporelle en un point donné et d'écrire les résultats dans un fichier texte.
    """
    print("Extract time series from Mercator")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Création du lecteur Mercator
    reader = MercatorReader('/home/fabien/mercator/ext-PSY2V4R4_mask.nc',
                            '/home/fabien/mercator/ext-PSY2V4R4_1dAV_20130201_20130202_grid2D_R20130213.nc',
                            '/home/fabien/mercator/ext-PSY2V4R4_1dAV_20130201_20130202_gridT_R20130213.nc',
                            '/home/fabien/mercator/ext-PSY2V4R4_1dAV_20130201_20130202_gridU_R20130213.nc',
                            '/home/fabien/mercator/ext-PSY2V4R4_1dAV_20130201_20130202_gridV_R20130213.nc')

    # Création de la coverage
    coverage = TimeLevelCoverage(reader);

    # Calculate nearest point (Lion buoy lon/lat)    
    memReader = MemoryReader('')
    serie = TimeSerie(memReader, freq='H', start='2013-02-01T00:00:00', end='2013-02-01T12:00:00');
    serie.name_station = "Lion"
    serie.data_source = "MERCATOR PSY2V4R4"
    serie.vertical_datum = "Inconnue"
    serie.x_coord = 4.640000
    serie.y_coord = 42.060000
    serie.data = DataFrame(index=serie.time_range,
                           columns=('sea_surface_height',
                                ))

    outputFile = '/tmp/' + str(serie.name_station) + '-tide-' + str(serie.time_range[0].strftime("%Y")) + '_to_' + str(
        serie.time_range[serie.time_range.size - 1].strftime("%Y")) + '.dat'

    ######################################
    ## Début ##
    ######################################
    nearestPoint = coverage.find_point_index(serie.x_coord, serie.y_coord)
    logging.info("Nearest point : " + str(nearestPoint[2]) + " / " + str(nearestPoint[3]) + " at " + str(
        nearestPoint[4]) + " km")
    logging.info("Nearest point (i,j) : " + str(nearestPoint[0]) + " / " + str(nearestPoint[1]))

    for date in serie.read_axis_time():
        logging.info(date)
        myDate = datetime(date.year, date.month, date.day, date.hour, date.minute, date.second)

        # cur = coverage.read_variable_current_at_time_and_level(myDate,z_level)
        # cur = coverage.read_variable_current_at_time(myDate)
        # u_cur = cur[0][nearestPoint[0],nearestPoint[1]]
        # v_cur = cur[1][nearestPoint[0],nearestPoint[1]]
        ssh = coverage.read_variable_ssh_at_time(myDate)[nearestPoint[1],nearestPoint[0]]
        # hssh = coverage.read_variable_bathy_ssh_at_time(myDate)[nearestPoint[1],nearestPoint[0]]
        # wetmask = coverage.read_variable_wetmask_at_time(myDate)[nearestPoint[1],nearestPoint[0]]
        #hs = coverage.read_variable_hs_at_time(myDate)[nearestPoint[1], nearestPoint[0]]
        #period = coverage.read_variable_waves_mean_period_at_time(myDate)[nearestPoint[1], nearestPoint[0]]
        #dir = coverage.read_variable_waves_dir_at_time(myDate)[nearestPoint[1], nearestPoint[0]]
        # wind_u = coverage.read_variable_wind_at_time(myDate)[0][nearestPoint[1],nearestPoint[0]]
        # wind_v = coverage.read_variable_wind_at_time(myDate)[1][nearestPoint[1],nearestPoint[0]]

        serie.data.loc[date] = [ssh]

    writer = SiroccoWriter(outputFile);
    writer.write_tide(serie)

    print('End of programm')

    
    
    
       
        
    
    
    
    
    
