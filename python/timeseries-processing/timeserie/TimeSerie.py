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

import numpy as np
import pandas
from pandas import DatetimeIndex
from datetime import timedelta

class TimeSerie:
    """"""

    TIME_DELTA = timedelta(minutes = 15)

    def __init__(self,myReader,freq,start=None,end=None):
            
        self.reader = myReader;

        if start is None or end is None:
            self.time_range = None
            self.freq =freq
        else:
            self.time_range = pandas.date_range(start=start, end=end,freq=freq)

        self.data = None
        self.data_source = "Undefined"
        self.name_station = "Undefined"
        self.x_coord = "Undefined"
        self.y_coord = "Undefined"
        self.vertical_datum = "Undefined"
        self.meta_data = "Undefined"

        # try to fill metadata
        self.read_metadata()

    # Read metadata
    def read_metadata(self):
        """
        Lit la metadonnée du fichier si le lecteur contient une fonction read_metadata()
        Returns
        -------

        """

        if  "read_metadata" in dir(self.reader):
            m = self.reader.read_metadata()

            if 'name_station' in m:
                self.name_station = m['name_station']
            if 'data_source' in m:
                self.data_source = m['data_source']
            if 'x_coord' in m:
                self.x_coord = float(m['x_coord'])
            if 'y_coord' in m:
                self.y_coord = float(m['y_coord'])
            if 'vertical_datum' in m:
                self.vertical_datum = m['vertical_datum']

    # Axis
    def read_axis_time(self):         
        return self.time_range;
    
    def get_time_size(self):
        return np.shape(self.time_range)[0]; 
    
    def read_data(self,force=False,raw=False):
        """

        Parameters
        ----------
        force : Force la lecture, sinon on retourne la donnée en mémoire self.data
        raw : Force à renvoyer la donnes brute du lecteur, sans bouchage des trous, sans reindexation du temps.

        Returns
        -------

        """

        if self.data is None or force == True:

            self.data = self.reader.read_data();

            if raw == True:
                return self.data;

            if self.time_range is None:
                self.time_range = pandas.date_range(start=self.data.index[0], end=self.data.index[self.data.index.size-1],freq=self.freq);

            if isinstance(self.data.index,DatetimeIndex):
                self.data = self.data.reindex(self.time_range,method="nearest", fill_value=np.nan, tolerance=TimeSerie.TIME_DELTA);
            else:
                self.data = self.data.set_index(pandas.DatetimeIndex(self.time_range))

        print self.data

        return self.data;
        
    def read_variable_sea_surface_height(self):
        """
        Read sea_surface_height
        """   
        if self.data == None:
            self.read_data();
        
        if 'sea_surface_height' in self.data:
            return self.data.sea_surface_height;
        else:
            raise ValueError("None sea_surface_height variable")
        
    def read_variable_sea_surface_wave_significant_height(self):     
        """
        Read ssh
        """   
        if self.data is None:
            self.read_data();
        
        if 'sea_surface_wave_significant_height' in self.data:
            return self.data.sea_surface_wave_significant_height;
        else:
            raise ValueError("None sea_surface_wave_significant_height variable")

    def read_variable_sea_surface_wave_mean_period(self):
        """
        Read sea_surface_wave_mean_period
        """
        if self.data is None:
            self.read_data();

        if 'sea_surface_wave_mean_period' in self.data:
            return self.data.sea_surface_wave_mean_period;
        else:
            raise ValueError("None sea_surface_wave_mean_period variable")
    
    def resample(self,freq,start,end,method="fill_na"):

        if self.data is None:
            self.data = self.reader.read_data();

        self.time_range = pandas.date_range(start=start, end=end,freq=freq)
        self.data = self.data.reindex(self.time_range,method="nearest", fill_value=np.nan, tolerance=TimeSerie.TIME_DELTA);

        if method=="linear":
            self.data = self.data.interpolate(method='linear')

        return self.data

