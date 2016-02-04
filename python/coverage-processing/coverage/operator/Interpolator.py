# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import numpy as np
from scipy.interpolate import griddata
from coverage.io.MemoryReader import MemoryReader
from coverage.TimeCoverage import TimeCoverage
from datetime import datetime

def resample2d(coverage,time,data):
    
    size=np.shape(data)
    Ymin=np.min(coverage.read_axis_y())
    Ymax=np.max(coverage.read_axis_y())
    Xmin=np.min(coverage.read_axis_x())
    Xmax=np.max(coverage.read_axis_x())

    xres_mean=((Xmax-Xmin)/size[1])
    yres_mean=((Ymax-Ymin)/size[0])

    res=np.mean([xres_mean,yres_mean])
    
    lon_reg,lat_reg=np.meshgrid(np.arange(Xmin, Xmax, res),np.arange(Ymin, Ymax, res))

    data=griddata((coverage.read_axis_x().ravel(),coverage.read_axis_y().ravel()), data.ravel(),(lon_reg, lat_reg), method='nearest')
    
    reader = MemoryReader(lon_reg[0,:],lat_reg[:,0],[time],data)
    
    return TimeCoverage(reader)

