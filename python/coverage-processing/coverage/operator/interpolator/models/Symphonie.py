# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import numpy as np
from netCDF4 import Dataset
from netCDF4 import date2num
from numpy import float32
from numpy import float64
from coverage.TimeCoverage import TimeCoverage
from coverage.io.netcdf.gmt.GMTReader import GMTReader
from coverage.operator.Interpolator import resample_2d_to_grid
import tempfile

def resample_type_1(coverage,targetResX,targetResY,targetFile=""):
    """Resample WLV and CURRENT """
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
    ncfile.createDimension('time', None)
    ncfile.createDimension('latitude', np.shape(targetAxisY)[0])
    ncfile.createDimension('longitude', np.shape(targetAxisX)[0])
   
    # variables
    times = ncfile.createVariable('time', float64, ('time',))
    times.units= 'seconds since 1970-01-01 00:00:00' 
    times.calendar= 'gregorian'
    times.standard_name= 'time'
    times.axis='T'
    times.conventions = "UTC time"

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
    times[:] = date2num(coverage.read_axis_t(), units = times.units, calendar = times.calendar)   
    
    # Water level
    wlv = ncfile.createVariable('wlv', float32, ('time', 'latitude', 'longitude',),fill_value="NaN")
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
        print np.shape(coverage.read_variable_wlv_at_time(time))
        print np.shape(coverage.read_axis_x())
        wlv[time_index:time_index+1,:,:] = resample_2d_to_grid(coverage.read_axis_x(),coverage.read_axis_y(),lon_reg,lat_reg,coverage.read_variable_wlv_at_time(time))
        time_index += 1
      
    #Surface current
    z=0
    ucur = ncfile.createVariable('surface_ucur', float32, ('time', 'latitude', 'longitude',),fill_value="NaN")
    ucur.long_name = "eastward current" ;
    ucur.standard_name = "eastward_sea_water_velocity" ;
    ucur.globwave_name = "eastward_sea_water_velocity" ;
    ucur.units = "m s-1" ;
    #ucur.scale_factor = 1.f ;
    #ucur.add_offset = 0.f ;
    #ucur.valid_min = -990 ;
    #ucur.valid_max = 990 ;
    ucur.comment = "cur=sqrt(U**2+V**2)" ;

    vcur = ncfile.createVariable('surface_vcur', float32, ('time', 'latitude', 'longitude',),fill_value="NaN")
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
        ucur[time_index:time_index+1,:,:] = resample_2d_to_grid(coverage.read_axis_x(),coverage.read_axis_y(),lon_reg,lat_reg,coverage.read_variable_u_current_at_time_and_level(time,z))
        vcur[time_index:time_index+1,:,:] = resample_2d_to_grid(coverage.read_axis_x(),coverage.read_axis_y(),lon_reg,lat_reg,coverage.read_variable_v_current_at_time_and_level(time,z))
        time_index += 1  


    # Close and return
    ncfile.close() 
    
    reader = GMTReader(filename)
    return TimeCoverage(reader)
    
    