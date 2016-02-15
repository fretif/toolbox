# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import numpy as np
from scipy.interpolate import griddata
import logging

def resample_2d_to_grid(sourceAxisX,sourceAxisY,targetAxisX, targetAixsY,data):
    
    logging.info('[Interpolator] Source grid size : '+str(np.shape(sourceAxisX))) 
    logging.info('[Interpolator] Target grid size : '+str(np.shape(targetAxisX))) 
    
    return griddata((sourceAxisX.ravel(),sourceAxisY.ravel()), data.ravel(),(targetAxisX, targetAixsY), method='nearest')

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
    
    logging.info('[Interpolator] Source grid size : '+str(np.shape(sourceAxisX))) 
    logging.info('[Interpolator] Target grid size : '+str(np.shape(lon_reg))) 

    return griddata((sourceAxisX.ravel(),sourceAxisY.ravel()), data.ravel(),(lon_reg, lat_reg), method='nearest')
