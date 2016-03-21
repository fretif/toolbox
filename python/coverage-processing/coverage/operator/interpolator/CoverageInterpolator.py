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

from coverage.operator.interpolator.InterpolatorCore import resample_2d_to_grid
from coverage.TimeCoverage import TimeCoverage
from coverage.TimeLevelCoverage import TimeLevelCoverage
import logging
from coverage.io.File import File
from netCDF4 import Dataset
from netCDF4 import date2num
from numpy import float32
from numpy import float64
import numpy as np

class CoverageInterpolator(File):

    def __init__(self, cov,resX,resY,myFile):
        File.__init__(self,myFile);
        self.coverage = cov;

        self.targetResX = resX
        self.targetResY = resY;

        # we compute the destination grid
        Ymin=np.min(self.coverage.read_axis_y())
        Ymax=np.max(self.coverage.read_axis_y())
        Xmin=np.min(self.coverage.read_axis_x())
        Xmax=np.max(self.coverage.read_axis_x())

        res=np.mean([self.targetResX,self.targetResY])
        self.lon_reg,self.lat_reg=np.meshgrid(np.arange(Xmin, Xmax, res),np.arange(Ymin, Ymax, res))
        targetAxisX = self.lon_reg[0,:]
        targetAxisY= self.lat_reg[:,0]

        self.ncfile = Dataset(self.filename, 'w', format='NETCDF4')
        self.ncfile.description = 'GMT Writer. Generated with Coverage Processing tools'

        # dimensions
        self.ncfile.createDimension('latitude', np.shape(targetAxisY)[0])
        self.ncfile.createDimension('longitude', np.shape(targetAxisX)[0])

        # variables
        latitudes = self.ncfile.createVariable('latitude', float32, ('latitude',))
        latitudes.units = "degree_north" ;
        latitudes.long_name = "latitude" ;
        latitudes.standard_name = "latitude" ;
        latitudes.valid_min = "-90.f";
        latitudes.valid_max = "90.f" ;
        latitudes.axis = "Y" ;

        longitudes = self.ncfile.createVariable('longitude', float32, ('longitude',))
        longitudes.units = "degree_east" ;
        longitudes.long_name = "longitude" ;
        longitudes.standard_name = "longitude" ;
        longitudes.valid_min = "-180.f" ;
        longitudes.valid_max = "180.f" ;
        longitudes.axis = "X" ;

        # data
        latitudes[:] = targetAxisY;
        longitudes[:] = targetAxisX;

        if(isinstance(self.coverage, TimeCoverage) or isinstance(self.coverage, TimeLevelCoverage)):

            self.ncfile.createDimension('time', None)
            times = self.ncfile.createVariable('time', float64, ('time',))
            times.units= 'seconds since 1970-01-01 00:00:00'
            times.calendar= 'gregorian'
            times.standard_name= 'time'
            times.axis='T'
            times.conventions = "UTC time"

            times[:] = date2num(self.coverage.read_axis_t(), units = times.units, calendar = times.calendar)

    def close(self):
        self.ncfile.close()

    def resample_variable_topography(self,coverage):
        if self.ncfile == None:
            raise IOError("Please call write_axis() first")

        logging.info('[CoverageInterpolator] Resample variable \'topography\' at resolution '+str(self.targetResX)+'/'+str(self.targetResY)+'.')

        wlv = self.ncfile.createVariable('topo', float32, ('latitude', 'longitude',),fill_value="NaN")
        wlv.long_name = "topography" ;
        wlv.standard_name = "topography" ;
        wlv.globwave_name = "topography" ;
        wlv.units = "m" ;
        #wlv.scale_factor = "1.f" ;
        #wlv.add_offset = "0.f" ;
        #wlv.valid_min = "0f" ;
        #wlv.valid_max = 10000f ;

        resample_2d_to_grid(coverage.read_axis_x(),coverage.read_axis_y(),self.lon_reg,self.lat_reg,coverage.read_variable_topography())


    def resample_variable_ssh(self,coverage):
        if self.ncfile == None:
            raise IOError("Please call write_axis() first")

        logging.info('[CoverageInterpolator] Resample variable \'ssh\' at resolution '+str(self.targetResX)+'/'+str(self.targetResY)+'.')

        wlv = self.ncfile.createVariable('ssh', float32, ('time', 'latitude', 'longitude',),fill_value="NaN")
        wlv.long_name = "sea surface height above sea level" ;
        wlv.standard_name = "sea_surface_height_above_sea_level" ;
        wlv.globwave_name = "sea_surface_height_above_sea_level" ;
        wlv.units = "m" ;
        #wlv.scale_factor = "1.f" ;
        #wlv.add_offset = "0.f" ;
        #wlv.valid_min = "0f" ;
        #wlv.valid_max = 10000f ;

        time_index=0
        for time in coverage.read_axis_t():
            wlv[time_index:time_index+1,:,:] = resample_2d_to_grid(coverage.read_axis_x(),coverage.read_axis_y(),self.lon_reg,self.lat_reg,coverage.read_variable_ssh_at_time(time))
            time_index += 1

    def resample_variable_current_at_level(self,coverage,z):

        if self.ncfile == None:
            raise IOError("Please call write_axis() first")

        logging.info('[CoverageInterpolator] Resample variable \'current\' at level '+str(z)+' at resolution '+str(self.targetResX)+'/'+str(self.targetResY)+'.')

        ucur = self.ncfile.createVariable('ucur', float32, ('time', 'latitude', 'longitude',),fill_value="NaN")
        ucur.long_name = "eastward current" ;
        ucur.standard_name = "eastward_sea_water_velocity" ;
        ucur.globwave_name = "eastward_sea_water_velocity" ;
        ucur.units = "m s-1" ;
        #ucur.scale_factor = 1.f ;
        #ucur.add_offset = 0.f ;
        #ucur.valid_min = -990 ;
        #ucur.valid_max = 990 ;
        ucur.comment = "cur=sqrt(U**2+V**2)" ;

        vcur = self.ncfile.createVariable('vcur', float32, ('time', 'latitude', 'longitude',),fill_value="NaN")
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
        for time in coverage.read_axis_t():
            cur = coverage.read_variable_current_at_time_and_level(time,z)
            ucur[time_index:time_index+1,:,:] = resample_2d_to_grid(coverage.read_axis_x(),coverage.read_axis_y(),self.lon_reg,self.lat_reg,cur[0])
            vcur[time_index:time_index+1,:,:] = resample_2d_to_grid(coverage.read_axis_x(),coverage.read_axis_y(),self.lon_reg,self.lat_reg,cur[1])
            time_index += 1

    def resample_variable_current(self,coverage):

        if self.ncfile == None:
            raise IOError("Please call write_axis() first")

        logging.info('[CoverageInterpolator] Resample variable \'current\' at resolution '+str(self.targetResX)+'/'+str(self.targetResY)+'.')

        ucur = self.ncfile.createVariable('ucur', float32, ('time', 'latitude', 'longitude',),fill_value="NaN")
        ucur.long_name = "eastward current" ;
        ucur.standard_name = "eastward_sea_water_velocity" ;
        ucur.globwave_name = "eastward_sea_water_velocity" ;
        ucur.units = "m s-1" ;
        #ucur.scale_factor = 1.f ;
        #ucur.add_offset = 0.f ;
        #ucur.valid_min = -990 ;
        #ucur.valid_max = 990 ;
        ucur.comment = "cur=sqrt(U**2+V**2)" ;

        vcur = self.ncfile.createVariable('vcur', float32, ('time', 'latitude', 'longitude',),fill_value="NaN")
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
        for time in coverage.read_axis_t():
            cur = coverage.read_variable_current_at_time(time)
            ucur[time_index:time_index+1,:,:] = resample_2d_to_grid(coverage.read_axis_x(),coverage.read_axis_y(),self.lon_reg,self.lat_reg,cur[0])
            vcur[time_index:time_index+1,:,:] = resample_2d_to_grid(coverage.read_axis_x(),coverage.read_axis_y(),self.lon_reg,self.lat_reg,cur[1])
            time_index += 1



