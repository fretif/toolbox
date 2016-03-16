# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.TimeLevelCoverage import TimeLevelCoverage
from coverage.operator.interpolator.models.Symphonie import resample_type_1
from coverage.operator.interpolator.models.Symphonie import resample_surface_current
from coverage.io.netcdf.symphonie.SymphonieReader import SymphonieReader
from coverage.io.netcdf.symphonie.SymphonieOfflineReader import SymphonieOfflineReader
from coverage.io.ascii.gmt.GMTWriter import GMTWriter
import logging
from datetime import datetime

if __name__ == "__main__":
    print("Transform/Interpole Symphonie to GMT")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file
    reader = SymphonieOfflineReader('/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/graphiques/leo/grid.nc',
                             '/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/graphiques/leo/20130224_120000.nc')      
        
    coverage = TimeLevelCoverage(reader); 
    
    print coverage.read_variable_u_current_at_time_and_level(datetime(2013,02,24,12),0)
    
    
    
    writer = GMTWriter('/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/graphiques/leo/fevrier-2013.dat')
    
    writer.write_variable_current_at_time_and_level(coverage,0,39)
    
    #resample_surface_current(coverage,1,1,'/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/graphiques/leo/fevrier-2013.nc')  
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
