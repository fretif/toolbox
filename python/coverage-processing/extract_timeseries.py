# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.TimeLevelCoverage import TimeLevelCoverage
from coverage.operator.interpolator.models.Symphonie import resample_type_1
from coverage.operator.interpolator.models.Symphonie import resample_surface_current
from coverage.io.netcdf.symphonie.SymphonieReader import SymphonieReader
from coverage.io.netcdf.mercator.MercatorReader import MercatorReader
import logging
import pandas
from datetime import datetime

if __name__ == "__main__":
    print("Extract time series from Mercator")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file
    reader = MercatorReader('/home/retf/work/fieldsites/med-cruesim/modelling/mercator/grid/mercator_grid.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/mercator-grid2D-2012-2013.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/mercator-gridT-2012-2013.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/mercator-gridU-2012-2013.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/mercator-gridV-2012-2013.nc')      
        
    coverage = TimeLevelCoverage(reader); 
    
    # Calculate nearest point (Lion buoy lon/lat)    
    nearestPoint = coverage.find_point_index(4.640000,42.060000) 
    logging.info("Nearest point : "+str(nearestPoint[2])+" / "+str(nearestPoint[3])+" at "+str(nearestPoint[2])+" km") 
    
    # Date range to be extracted
    dates = pandas.date_range(start='2012-01-01 12:00:00', end='2012-01-04 12:00:00',freq='24H')
    z_level = 0 #surface
    
    # Prepare file to save
    file = open("/tmp/output", "w")  
    file.write("#date (UTC) \t longitude \t latitude \t u comp (m/s) \t v comp (m/s) \t ssh above geoid (m) \n")         
    
    for date in dates:
        
        logging.info(date) 
        myDate = datetime(date.year,date.month,date.day,date.hour,date.minute,date.second)  
        
        u_cur = coverage.read_variable_u_current_at_time_and_level(myDate,z_level)[nearestPoint[0],nearestPoint[1]]      
        v_cur = coverage.read_variable_v_current_at_time_and_level(myDate,z_level)[nearestPoint[0],nearestPoint[1]]          
        ssh = coverage.read_variable_wlv_at_time(myDate)[nearestPoint[0],nearestPoint[1]]
        
        file.write(str(date)+"\t"+str(nearestPoint[2])+"\t"+str(nearestPoint[3])+"\t"+str(u_cur)+"\t"+str(v_cur)+"\t"+str(ssh)+"\n") 
        
    file.close()
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
