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
from coverage.io.netcdf.symphonie.SymphonieReader import SymphonieReader
from timeserie.io.ascii.sirocco.SiroccoWriter import SiroccoWriter
from timeserie.io.MemoryReader import MemoryReader
import logging
from pandas import Series, DataFrame
from datetime import datetime
import math


if __name__ == "__main__":
    """
    Cette routine permet d'extraire une série temporelle en un point donné et d'écrire les résultats dans un fichier texte.
    """
    print("Extraction d'une série temporelle en un point à partir des résultats de SYMPHONIE")

    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

    ######################################
    ## Configuration ##
    ######################################

    reader = SymphonieReader('/home/fabien/grille.nc',
                             '/home/fabien/symphonie_var.nc')

    coverage = TimeLevelCoverage(reader);

    metadata = {};
    metadata['name_station'] = "Jiangjun"
    metadata['data_source'] = "Simu FULL-HYDRO"
    metadata['vertical_datum'] = "TWVD2001"
    metadata['x_coord'] = 120.0167
    metadata['y_coord'] = 23.2125

    memReader = MemoryReader(metadata)
    serie = TimeSerie(memReader, freq='30min', start='2012-06-19T18:00:00', end='2012-06-19T23:00:00');

    serie.data = DataFrame(index=serie.time_range,
                           columns=(
    #                                'sea_surface_wave_significant_height',
    #                                'sea_surface_wave_mean_period',
    #                                'sea_surface_wave_to_direction',
    #                                'sea_surface_wave_from_direction',
    #                                'sea_surface_wave_peak_from_direction',
    #                                'sea_surface_wave_peak_to_direction',
                                    'sea_surface_height',
    #                                'sea_surface_elevation',
    #                                'sea_surface_current_speed',
    #                                'sea_surface_current_from_direction',
    #                                'sea_surface_current_to_direction',
    #                                'wind_speed_10m',
    #                                'wind_to_direction_10m',
    #                                'sea_surface_pressure',
    #                                'water_volume_transport_into_sea_water_from_rivers',
                                    ))

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

        # at time
        #u_cur = coverage.read_variable_current_at_time(myDate)[0][nearestPoint[1], nearestPoint[0]]
        #v_cur = coverage.read_variable_current_at_time(myDate)[1][nearestPoint[1], nearestPoint[0]]
        # at time and depth
        #depth=50.0 #m
        #u_cur = coverage.read_variable_current_at_time_and_depth(myDate,depth)[0][nearestPoint[1], nearestPoint[0]]
        #v_cur = coverage.read_variable_current_at_time_and_depth(myDate,depth)[1][nearestPoint[1], nearestPoint[0]]

        #u_wind = coverage.read_variable_wind_at_time(myDate)[0][nearestPoint[1], nearestPoint[0]]
        #v_wind = coverage.read_variable_wind_at_time(myDate)[1][nearestPoint[1], nearestPoint[0]]

        # append to the DataFrame
        serie.data.loc[date] = [
            #                                'sea_surface_wave_significant_height',
            #coverage.read_variable_hs_at_time(myDate)[nearestPoint[1], nearestPoint[0]],
            #                               'sea_surface_wave_mean_period',
            #coverage.read_variable_waves_mean_period_at_time(myDate)[nearestPoint[1], nearestPoint[0]],
            #                                'sea_surface_wave_to_direction',
            #                                'sea_surface_wave_from_direction',
            #                                'sea_surface_wave_peak_from_direction',
            #                                'sea_surface_wave_peak_to_direction',
            #coverage.read_variable_waves_dir_at_time(myDate)[nearestPoint[1], nearestPoint[0]],
            #                                'sea_surface_height',
            #                                'sea_surface_elevation',
            coverage.read_variable_ssh_at_time(myDate)[nearestPoint[1], nearestPoint[0]],
            #                                'sea_surface_current_speed',
            #math.sqrt(u_cur ** 2 + v_cur ** 2),
            #                                'sea_surface_current_from_direction',
            #                                'sea_surface_current_to_direction',
            #math.atan2(v_cur,u_cur),
            #                                'wind_speed_10m',
            #math.sqrt(u_cur ** 2 + v_cur ** 2),
            #                                'wind_to_direction_10m',
            #math.atan2(v_cur, u_cur),
            #                                'sea_surface_pressure',
            #coverage.read_variable_ssp_at_time(myDate)[nearestPoint[1], nearestPoint[0]],
            #                                'water_volume_transport_into_sea_water_from_rivers',
        ]

    outputFile = '/tmp/' + str(serie.name_station) + '-ssh-' + str(serie.time_range[0].strftime("%Y")) + '_to_' + str(
            serie.time_range[serie.time_range.size - 1].strftime("%Y")) + '.dat'

    writer = SiroccoWriter(outputFile);
    #writer.write_waves(serie)
    writer.write_tide(serie)
    #writer.write_currents(serie)

    print('End of programm')

