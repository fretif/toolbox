#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# TimeSeriesProcessing is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# TimeSeriesProcessing is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
import os.path
import pandas
import logging
import numpy as np
import re

class SiroccoReader:

    def __init__(self, myFilename):
        self.filename = myFilename   

    def read_metadata(self):
        metadata = {};
        with open(self.filename) as f:
            line = f.readline()
            while line and line.startswith("#"):

                #TODO : gérer les espaces blancs

                if "Station" in line:
                    metadata['name_station'] = re.sub('[^a-zA-Z0-9-_*.]', '',line.rsplit(':', 1)[1])

                if "Longitude" in line:
                    metadata['x_coord'] = re.sub('[^a-zA-Z0-9-_*.]', '',line.rsplit(':', 1)[1])

                if "Latitude" in line:
                    metadata['y_coord'] = re.sub('[^a-zA-Z0-9-_*.]', '',line.rsplit(':', 1)[1])

                if "Vertical datum" in line:
                    metadata['vertical_datum'] = re.sub('[^a-zA-Z0-9-_*.]', '',line.rsplit(':', 1)[1])

                if "Data source" in line:
                    metadata['data_source'] = re.sub('[^a-zA-Z0-9-_*.]', '',line.rsplit(':', 1)[1])

                line = f.readline()

        return metadata

    def read_data(self):
        
        if not os.path.isfile(self.filename):
            raise IOError(self.filename+" doesn't exists. Abort")

        # TODO Lire et décoder l'entête pour trouver les colonnes.
        #with open(self.filename) as f:
        #    line = f.readline()
        #    while line and line.startswith("#"):
        #         if "Columns" in line:
        #            metadata['name_station'] = re.sub('[^a-zA-Z0-9-_*.]', '',line.rsplit(':', 1)[1])

        # waves
        data = pandas.read_csv(self.filename,usecols=[0,1,2],names=['time','sea_surface_wave_significant_height','sea_surface_wave_mean_period'],sep='\t',index_col=0,parse_dates=True,comment='#')
        # sea-level
        #data = pandas.read_csv(self.filename,usecols=[0,1],names=['time','sea_surface_height'],sep='\t',index_col=0,parse_dates=True,comment='#')

        # we process time record (drop duplicate...)
        #duplicates = np.where(data.time.duplicated()== True)[0]
        #count = np.shape(duplicates)[0]
        #if count > 0:
        #    logging.warn('[SiroccoReader] '+str(count)+' dates are duplicated. We drop them by keeping the first.')
        #    data= data.drop_duplicates(subset='time',keep='first')
        ##data = data.set_index(pandas.DatetimeIndex(data['time']))
        #data = data.drop('time',1)

        return data