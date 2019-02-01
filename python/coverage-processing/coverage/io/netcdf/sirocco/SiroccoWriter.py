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
# Author : Fabien Rétif - fabien.retif@zoho.com
#
from __future__ import division, print_function, absolute_import
from coverage.io.File import File
from netCDF4 import Dataset
from netCDF4 import date2num
from numpy import float32
from numpy import float64
import numpy as np
import logging
from coverage.TimeCoverage import TimeCoverage
from coverage.LevelCoverage import LevelCoverage
from coverage.TimeLevelCoverage import TimeLevelCoverage

class SiroccoWriter (File):

    def __init__(self,cov,myFile,depths):
        File.__init__(self,myFile);
        self.coverage = cov;
        self.targetDepths = depths
        self.ncfile = Dataset(self.filename, 'w', format='NETCDF4')
        self.ncfile.description = 'Sirocco Writer. Generated with Coverage Processing tools'

        # dimensions
        self.ncfile.createDimension('latitude', self.coverage.get_y_size())
        self.ncfile.createDimension('longitude', self.coverage.get_x_size())

        if self.coverage.is_regular_grid()==True:

            # variables
            latitudes = self.ncfile.createVariable('latitude', float32, ('latitude',))
            latitudes.units = "degree_north" ;
            latitudes.long_name = "latitude" ;
            latitudes.standard_name = "latitude" ;
            latitudes.valid_min = -90.;
            latitudes.valid_max = 90. ;
            latitudes.axis = "Y" ;

            longitudes = self.ncfile.createVariable('longitude', float32, ('longitude',))
            longitudes.units = "degree_east" ;
            longitudes.long_name = "longitude" ;
            longitudes.standard_name = "longitude" ;
            longitudes.valid_min = -180. ;
            longitudes.valid_max = 180. ;
            longitudes.axis = "X" ;

            # data
            latitudes[:] = self.coverage.read_axis_y();
            longitudes[:] = self.coverage.read_axis_x();

        else:

            latitudes = self.ncfile.createVariable('latitude', float32, ('latitude','longitude',))
            latitudes.units = "degree_north" ;
            latitudes.long_name = "latitude" ;
            latitudes.standard_name = "latitude" ;
            latitudes.valid_min = -90.;
            latitudes.valid_max = 90. ;
            latitudes.axis = "Y" ;

            longitudes = self.ncfile.createVariable('longitude', float32, ('latitude','longitude',))
            longitudes.units = "degree_east" ;
            longitudes.long_name = "longitude" ;
            longitudes.standard_name = "longitude" ;
            longitudes.valid_min = -180. ;
            longitudes.valid_max = 180. ;
            longitudes.axis = "X" ;

            # data
            latitudes[:,:] = self.coverage.read_axis_y();
            longitudes[:,:] = self.coverage.read_axis_x();


        if(isinstance(self.coverage, TimeCoverage) or isinstance(self.coverage, TimeLevelCoverage)):

            self.ncfile.createDimension('time', None)
            times = self.ncfile.createVariable('time', float64, ('time',))
            times.units= 'seconds since 1970-01-01 00:00:00'
            times.calendar= 'gregorian'
            times.standard_name= 'time'
            times.axis='T'
            times.conventions = "UTC time"

            times[:] = date2num(self.coverage.read_axis_t(), units = times.units, calendar = times.calendar)

        if(isinstance(self.coverage, LevelCoverage) or isinstance(self.coverage, TimeLevelCoverage)):

            self.ncfile.createDimension('depth', np.size(self.targetDepths))
            levels = self.ncfile.createVariable('depth', float64, ('depth',))
            levels.standard_name= 'depth'
            levels.long_name="Positive depth"
            levels.axis='Z'

            levels[:] = self.targetDepths

        
    def close(self):
        self.ncfile.close()


    def write_variable_bathymetry(self):
        if self.ncfile == None:
            raise IOError("Please call write_axis() first")

        logging.info('[SiroccoWriter] Write variable \'bathymetry\'.')

        var = self.ncfile.createVariable('bathy', float32, ('latitude', 'longitude',),fill_value=9.96921e+36)
        var.long_name = "bathymetry" ;
        var.standard_name = "bathymetry" ;
        var.globwave_name = "bathymetry" ;

        var[:] = self.coverage.read_variable_bathymetry()
            
    def write_variable_ssh(self):
        if self.ncfile == None:
            raise IOError("Please call write_axis() first") 
            
        wlv = self.ncfile.createVariable('ssh', float32, ('time', 'latitude', 'longitude',),fill_value=9.96921e+36)
        wlv.long_name = "sea surface height above sea level" ;
        wlv.standard_name = "sea_surface_height_above_sea_level" ;
        wlv.globwave_name = "sea_surface_height_above_sea_level" ;
        wlv.units = "m" ;        
        #wlv.scale_factor = "1.f" ;
        #wlv.add_offset = "0.f" ;
        #wlv.valid_min = "0f" ;
        #wlv.valid_max = 10000f ;
        
        time_index=0
        for time in self.coverage.read_axis_t():
            logging.info('[SiroccoWriter] Writing variable \'ssh\' at time \''+str(time)+'\'')
            wlv[time_index:time_index+1,:] = self.coverage.read_variable_ssh_at_time(time)
            time_index += 1

    def write_variable_hs(self):
        if self.ncfile == None:
            raise IOError("Please call write_axis() first")

        var = self.ncfile.createVariable('hs', float32, ('time', 'latitude', 'longitude',),fill_value=9.96921e+36)
        var.long_name = "sea surface wave height" ;
        var.standard_name = "sea_surface_wave_height" ;
        var.globwave_name = "sea_surface_wave_height" ;
        var.units = "m" ;
        #wlv.scale_factor = "1.f" ;
        #wlv.add_offset = "0.f" ;
        #wlv.valid_min = "0f" ;
        #wlv.valid_max = 10000f ;

        time_index=0
        for time in self.coverage.read_axis_t():
            logging.info('[SiroccoWriter] Writing variable \'hs\' at time \''+str(time)+'\'')
            var[time_index:time_index+1,:] = self.coverage.read_variable_hs_at_time(time)
            time_index += 1

    def write_variable_taw(self):
        if self.ncfile == None:
            raise IOError("Please call write_axis() first")

        var = self.ncfile.createVariable('hs', float32, ('time', 'latitude', 'longitude',),fill_value=9.96921e+36)
        var.long_name = "sea surface wave height" ;
        var.standard_name = "sea_surface_wave_height" ;
        var.globwave_name = "sea_surface_wave_height" ;
        var.units = "m" ;
        #wlv.scale_factor = "1.f" ;
        #wlv.add_offset = "0.f" ;
        #wlv.valid_min = "0f" ;
        #wlv.valid_max = 10000f ;

        time_index=0
        for time in self.coverage.read_axis_t():
            logging.info('[SiroccoWriter] Writing variable \'hs\' at time \''+str(time)+'\'')
            var[time_index:time_index+1,:] = self.coverage.read_variable_hs_at_time(time)
            time_index += 1

    def write_variable_two(self):
        if self.ncfile == None:
            raise IOError("Please call write_axis() first")

        var = self.ncfile.createVariable('hs', float32, ('time', 'latitude', 'longitude',),fill_value=9.96921e+36)
        var.long_name = "sea surface wave height" ;
        var.standard_name = "sea_surface_wave_height" ;
        var.globwave_name = "sea_surface_wave_height" ;
        var.units = "m" ;
        #wlv.scale_factor = "1.f" ;
        #wlv.add_offset = "0.f" ;
        #wlv.valid_min = "0f" ;
        #wlv.valid_max = 10000f ;

        time_index=0
        for time in self.coverage.read_axis_t():
            logging.info('[SiroccoWriter] Writing variable \'hs\' at time \''+str(time)+'\'')
            var[time_index:time_index+1,:] = self.coverage.read_variable_hs_at_time(time)
            time_index += 1

    def write_variable_2D_mask(self):
        if self.ncfile == None:
            raise IOError("Please call write_axis() first")

        var = self.ncfile.createVariable('mask', int, ( 'latitude', 'longitude',),fill_value=-9999)
        var.long_name = "land/sea mask" ;
        var.standard_name = "land_sea_mask" ;
        var.globwave_name = "land_sea_mask" ;
        var.units = "m" ;
        #wlv.scale_factor = "1.f" ;
        #wlv.add_offset = "0.f" ;
        #wlv.valid_min = "0f" ;
        #wlv.valid_max = 10000f ;

        logging.info('[WW3Writer] Writing variable \'2D mask\'')
        var[:] = self.coverage.read_variable_2D_mask()
            
    def write_variable_current_at_depths(self):
        
        if self.ncfile == None:
            raise IOError("Please call write_axis() first")   
            
        ucur = self.ncfile.createVariable('ucur', float32, ('time','depth', 'latitude', 'longitude',),fill_value=9.96921e+36)
        ucur.long_name = "eastward current" ;
        ucur.standard_name = "eastward_sea_water_velocity" ;
        ucur.globwave_name = "eastward_sea_water_velocity" ;
        ucur.units = "m s-1" ;
        #ucur.scale_factor = 1.f ;
        #ucur.add_offset = 0.f ;
        #ucur.valid_min = -990 ;
        #ucur.valid_max = 990 ;
        ucur.comment = "cur=sqrt(U**2+V**2)" ;
        
        vcur = self.ncfile.createVariable('vcur', float32, ('time', 'depth', 'latitude', 'longitude',),fill_value=9.96921e+36)
        vcur.long_name = "northward current" ;
        vcur.standard_name = "northward_sea_water_velocity" ;
        vcur.globwave_name = "northward_sea_water_velocity" ;
        vcur.units = "m s-1" ;
        #ucur.scale_factor = 1.f ;
        #ucur.add_offset = 0.f ;
        #ucur.valid_min = -990 ;
        #ucur.valid_max = 990 ;
        vcur.comment = "cur=sqrt(U**2+V**2)" ;

        time_index=0
        for time in self.coverage.read_axis_t():

             logging.info('[SiroccoWriter] Writing variable \'current\' at time \''+str(time)+'\'')

             level_index = 0
             for level in self.targetDepths:

                cur = self.coverage.read_variable_current_at_time_and_depth(time,level)

                ucur[time_index:time_index+1,level_index:level_index+1,:,:] = cur[0]
                vcur[time_index:time_index+1,level_index:level_index+1,:,:] = cur[1]
                level_index+= 1

             time_index += 1

    def write_variable_surface_stokes_drift(self):

        if self.ncfile == None:
            raise IOError("Please call write_axis() first")

        ucur = self.ncfile.createVariable('uss', float32, ('time','latitude', 'longitude',),fill_value=9.96921e+36)
        ucur.long_name = "eastward current" ;
        ucur.standard_name = "eastward_sea_water_velocity" ;
        ucur.globwave_name = "eastward_sea_water_velocity" ;
        ucur.units = "m s-1" ;
        #ucur.scale_factor = 1.f ;
        #ucur.add_offset = 0.f ;
        #ucur.valid_min = -990 ;
        #ucur.valid_max = 990 ;


        vcur = self.ncfile.createVariable('vss', float32, ('time', 'latitude', 'longitude',),fill_value=9.96921e+36)
        vcur.long_name = "northward current" ;
        vcur.standard_name = "northward_sea_water_velocity" ;
        vcur.globwave_name = "northward_sea_water_velocity" ;
        vcur.units = "m s-1" ;
        #ucur.scale_factor = 1.f ;
        #ucur.add_offset = 0.f ;
        #ucur.valid_min = -990 ;
        #ucur.valid_max = 990 ;

        time_index=0
        for time in self.coverage.read_axis_t():

            logging.info('[SiroccoWriter] Writing variable \'surface_stokes_drift\' at time \''+str(time)+'\'')

            cur = self.coverage.read_variable_surface_stokes_drift_at_time(time)

            ucur[time_index:time_index+1,:,:] = cur[0]
            vcur[time_index:time_index+1,:,:] = cur[1]
            time_index += 1

    def write_variable_taw(self):

        if self.ncfile == None:
            raise IOError("Please call write_axis() first")

        ucur = self.ncfile.createVariable('utaw', float32, ('time','latitude', 'longitude',),fill_value=9.96921e+36)
        ucur.long_name = "eastward current" ;
        ucur.standard_name = "eastward_sea_water_velocity" ;
        ucur.globwave_name = "eastward_sea_water_velocity" ;
        ucur.units = "m s-1" ;
        #ucur.scale_factor = 1.f ;
        #ucur.add_offset = 0.f ;
        #ucur.valid_min = -990 ;
        #ucur.valid_max = 990 ;


        vcur = self.ncfile.createVariable('vtaw', float32, ('time', 'latitude', 'longitude',),fill_value=9.96921e+36)
        vcur.long_name = "northward current" ;
        vcur.standard_name = "northward_sea_water_velocity" ;
        vcur.globwave_name = "northward_sea_water_velocity" ;
        vcur.units = "m s-1" ;
        #ucur.scale_factor = 1.f ;
        #ucur.add_offset = 0.f ;
        #ucur.valid_min = -990 ;
        #ucur.valid_max = 990 ;

        time_index=0
        for time in self.coverage.read_axis_t():

            logging.info('[SiroccoWriter] Writing variable \'taw\' at time \''+str(time)+'\'')

            cur = self.coverage.read_variable_taw_at_time(time)

            ucur[time_index:time_index+1,:,:] = cur[0]
            vcur[time_index:time_index+1,:,:] = cur[1]
            time_index += 1

    def write_variable_two(self):

        if self.ncfile == None:
            raise IOError("Please call write_axis() first")

        ucur = self.ncfile.createVariable('utwo', float32, ('time','latitude', 'longitude',),fill_value=9.96921e+36)
        ucur.long_name = "eastward current" ;
        ucur.standard_name = "eastward_sea_water_velocity" ;
        ucur.globwave_name = "eastward_sea_water_velocity" ;
        ucur.units = "m s-1" ;
        #ucur.scale_factor = 1.f ;
        #ucur.add_offset = 0.f ;
        #ucur.valid_min = -990 ;
        #ucur.valid_max = 990 ;


        vcur = self.ncfile.createVariable('vtwo', float32, ('time', 'latitude', 'longitude',),fill_value=9.96921e+36)
        vcur.long_name = "northward current" ;
        vcur.standard_name = "northward_sea_water_velocity" ;
        vcur.globwave_name = "northward_sea_water_velocity" ;
        vcur.units = "m s-1" ;
        #ucur.scale_factor = 1.f ;
        #ucur.add_offset = 0.f ;
        #ucur.valid_min = -990 ;
        #ucur.valid_max = 990 ;

        time_index=0
        for time in self.coverage.read_axis_t():

            logging.info('[SiroccoWriter] Writing variable \'two\' at time \''+str(time)+'\'')

            cur = self.coverage.read_variable_two_at_time(time)

            ucur[time_index:time_index+1,:,:] = cur[0]
            vcur[time_index:time_index+1,:,:] = cur[1]
            time_index += 1

    def write_variable_wind(self):

        if self.ncfile == None:
            raise IOError("Please call write_axis() first")

        ucur = self.ncfile.createVariable('uwind', float32, ('time','latitude', 'longitude',),fill_value=9.96921e+36)
        ucur.long_name = "eastward wind 10m" ;
        ucur.standard_name = "eastward_wind_velocity" ;
        ucur.globwave_name = "eastward_wind_velocity" ;
        ucur.units = "m s-1" ;
        #ucur.scale_factor = 1.f ;
        #ucur.add_offset = 0.f ;
        #ucur.valid_min = -990 ;
        #ucur.valid_max = 990 ;


        vcur = self.ncfile.createVariable('vwind', float32, ('time', 'latitude', 'longitude',),fill_value=9.96921e+36)
        vcur.long_name = "northward wind 10m" ;
        vcur.standard_name = "northward_wind_velocity" ;
        vcur.globwave_name = "northward_wind_velocity" ;
        vcur.units = "m s-1" ;
        #ucur.scale_factor = 1.f ;
        #ucur.add_offset = 0.f ;
        #ucur.valid_min = -990 ;
        #ucur.valid_max = 990 ;

        time_index=0
        for time in self.coverage.read_axis_t():

            logging.info('[SiroccoWriter] Writing variable \'wind\' at time \''+str(time)+'\'')

            cur = self.coverage.read_variable_wind_at_time(time)

            ucur[time_index:time_index+1,:,:] = cur[0]
            vcur[time_index:time_index+1,:,:] = cur[1]
            time_index += 1
