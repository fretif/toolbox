# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.TimeCoverage import TimeCoverage
from coverage.operator.interpolator.models.WW3 import resample_type_1
from coverage.io.netcdf.ww3.WW3Reader import WW3Reader
import logging

if __name__ == "__main__":
    print("Transform/Interpole WW3 to GMT ")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file
    reader = WW3Reader('/home/retf/work/fieldsites/med-cruesim/modelling/waves/large-scale/outputs/netcdf/ww3.201103.nc')      
        
    coverage = TimeCoverage(reader); 
    
    resample_type_1(coverage,0.01,0.01,'/home/retf/work/fieldsites/med-cruesim/modelling/waves/large-scale/outputs/netcdf/regular/ww3-mars-2011.nc')  
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
