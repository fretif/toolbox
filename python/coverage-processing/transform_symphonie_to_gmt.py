# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.TimeLevelCoverage import TimeLevelCoverage
from coverage.operator.interpolator.models.Symphonie import resample_type_1
from coverage.io.netcdf.symphonie.SymphonieReader import SymphonieReader
import logging

if __name__ == "__main__":
    print("Transform/Interpole Symphonie to GMT")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file
    reader = SymphonieReader('/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/graphiques/grid.nc',
                             '/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/graphiques/20110330_000033.nc')      
        
    coverage = TimeLevelCoverage(reader); 
    
    resample_type_1(coverage,0.01,0.01,'/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/graphiques/regular/mars-2011.nc')  
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
