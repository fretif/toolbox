# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.Coverage import Coverage
from coverage.operator.interpolator.models.MesoNh import resample_type_1
from coverage.io.netcdf.mesonh.MesoNhReader import MesoNhReader
import logging

if __name__ == "__main__":
    print("Transform/Interpole Meso-nh to GMT")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file
    reader = MesoNhReader('/home/retf/work/fieldsites/med-cruesim/modelling/atmosphere/AOC_500M_V2.nc')      
        
    coverage = Coverage(reader); 
    
    resample_type_1(coverage,0.005,0.005,'/home/retf/work/fieldsites/med-cruesim/modelling/atmosphere/regular.nc')  
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
