# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.io.netcdf.mercator.MercatorReader import MercatorReader
from coverage.TimeCoverage import TimeCoverage
from coverage.io.netcdf.ww3.WW3Writer import WW3Writer

if __name__ == "__main__":
    print("Hello World !")
    
     #Read file
    reader = MercatorReader('/home/retf/work/fieldsites/taiwan/modelling/mercator/ext-PSY4V1R3_1dAV_20120620_20120621_gridT_R20120704.nc')      
    
    coverage = TimeCoverage(reader);    
    
    writer = WW3Writer('/home/retf/work/fieldsites/taiwan/modelling/mercator/ww3.nc')  
    writer.write_coverage(coverage,"sossheig");
   
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
