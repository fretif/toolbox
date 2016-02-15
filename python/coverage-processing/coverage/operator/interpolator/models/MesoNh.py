# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import numpy as np
from netCDF4 import Dataset
from netCDF4 import date2num
from numpy import float32
from numpy import float64
from coverage.TimeCoverage import TimeCoverage
from coverage.Coverage import Coverage
from coverage.io.netcdf.gmt.GMTReader import GMTReader
from coverage.operator.interpolator.Interpolator import resample_2d_to_grid
from coverage.operator.interpolator.Interpolator import resample_2d
import tempfile

def resample_type_1(coverage,targetResX,targetResY,targetFile=""):
    """Resample TOPO """
    # we compute the destination grid   
    Ymin=np.min(coverage.read_axis_y())
    Ymax=np.max(coverage.read_axis_y())
    Xmin=np.min(coverage.read_axis_x())
    Xmax=np.max(coverage.read_axis_x())

    res=np.mean([targetResX,targetResY])
    lon_reg,lat_reg=np.meshgrid(np.arange(Xmin, Xmax, res),np.arange(Ymin, Ymax, res))
    targetAxisX = lon_reg[0,:]
    targetAxisY= lat_reg[:,0]
    
    if(targetFile==""):    
        filename = tempfile.TemporaryFile().name
    else:
        filename = targetFile

    ncfile = Dataset(filename, 'w', format='NETCDF4')
    ncfile.description = 'GMT Writer. Generated with Coverage Processing tools'

    # dimensions   
    ncfile.createDimension('latitude', np.shape(targetAxisY)[0])
    ncfile.createDimension('longitude', np.shape(targetAxisX)[0])
   
    # variables  
    latitudes = ncfile.createVariable('latitude', float32, ('latitude',))
    latitudes.units = "degree_north" ;
    latitudes.long_name = "latitude" ;
    latitudes.standard_name = "latitude" ;
    latitudes.valid_min = "-90.f";
    latitudes.valid_max = "90.f" ;
    latitudes.axis = "Y" ;

    longitudes = ncfile.createVariable('longitude', float32, ('longitude',))
    longitudes.units = "degree_east" ;
    longitudes.long_name = "longitude" ;
    longitudes.standard_name = "longitude" ;
    longitudes.valid_min = "-180.f" ;
    longitudes.valid_max = "180.f" ;
    longitudes.axis = "X" ; 

     # data      
    latitudes[:] = targetAxisY;        
    longitudes[:] = targetAxisX;     
          
    # Topo
    topo = ncfile.createVariable('topo', float32, ('latitude', 'longitude',),fill_value="NaN")
    topo.long_name = "topo" ;
    topo.standard_name = "topo" ;
    topo.globwave_name = "topo" ;
    topo.units = "m" ;        
    #wlv.scale_factor = "1.f" ;
    #wlv.add_offset = "0.f" ;
    #wlv.valid_min = "0f" ;
    #wlv.valid_max = 10000f ; 
    
    topo[:,:] = resample_2d_to_grid(coverage.read_axis_x(),coverage.read_axis_y(),lon_reg,lat_reg,coverage.read_variable_topography())

    # Close and return
    ncfile.close() 
    
    reader = GMTReader(filename)
    return Coverage(reader)
    