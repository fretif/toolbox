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

from scipy.interpolate import griddata
import logging
import numpy as np

def resample_2d_to_grid(sourceAxisX,sourceAxisY,targetAxisX, targetAixsY,data):
    
    logging.info('[InterpolatorCore] Source grid size : '+str(np.shape(sourceAxisX)))
    logging.info('[InterpolatorCore] Target grid size : '+str(np.shape(targetAxisX)))
    
    return griddata((sourceAxisX.ravel(),sourceAxisY.ravel()), data.ravel(),(targetAxisX, targetAixsY), method='nearest', fill_value=9.96921e+36)

def resample_2d_to_resolution(sourceAxisX,sourceAxisY,targetResX, targetResY,data):
    
    Ymin=np.min(sourceAxisY)
    Ymax=np.max(sourceAxisY)
    Xmin=np.min(sourceAxisX)
    Xmax=np.max(sourceAxisX)

    res=np.mean([targetResX,targetResY])
    
    lon_reg,lat_reg=np.meshgrid(np.arange(Xmin, Xmax, res),np.arange(Ymin, Ymax, res))

    return griddata((sourceAxisX.ravel(),sourceAxisY.ravel()), data.ravel(),(lon_reg, lat_reg), method='nearest')

def resample_2d(sourceAxisX,sourceAxisY,data):
    
    size=np.shape(data)    
    Ymin=np.min(sourceAxisY)
    Ymax=np.max(sourceAxisY)
    Xmin=np.min(sourceAxisX)
    Xmax=np.max(sourceAxisX)

    xres_mean=((Xmax-Xmin)/size[1])
    yres_mean=((Ymax-Ymin)/size[0])

    res=np.mean([xres_mean,yres_mean])
    
    lon_reg,lat_reg=np.meshgrid(np.arange(Xmin, Xmax, res),np.arange(Ymin, Ymax, res))
    
    logging.info('[InterpolatorCore] Source grid size : '+str(np.shape(sourceAxisX)))
    logging.info('[InterpolatorCore] Target grid size : '+str(np.shape(lon_reg)))

    return griddata((sourceAxisX.ravel(),sourceAxisY.ravel()), data.ravel(),(lon_reg, lat_reg), method='nearest')
