# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.io.netcdf.mercator.MercatorReader import MercatorReader
from coverage.TimeLevelCoverage import TimeLevelCoverage
from coverage.TimeCoverage import TimeCoverage
from coverage.io.netcdf.ww3.WW3Writer import WW3Writer
from coverage.io.netcdf.ww3.WW3Reader import WW3Reader
#from coverage.io.ascii.gmt.GMTWriter import GMTWriter
from coverage.io.netcdf.gmt.GMTWriter import GMTWriter
from coverage.operator.Interpolator import resample2d
import numpy as np
from utils.Mercator import resampleTXY

if __name__ == "__main__":
    print("Hello World !")
    
    # Read file
    reader = MercatorReader('/home/retf/work/fieldsites/taiwan/modelling/mercator/ext-PSY4V1R3_mask.nc',
                            '/home/retf/work/fieldsites/taiwan/modelling/mercator/ext-PSY4V1R3_1dAV_20120620_20120621_gridT_R20120704.nc',
                            '/home/retf/work/fieldsites/taiwan/modelling/mercator/ext-PSY4V1R3_1dAV_20120620_20120621_gridU_R20120704.nc',
                            '/home/retf/work/fieldsites/taiwan/modelling/mercator/ext-PSY4V1R3_1dAV_20120620_20120621_gridV_R20120704.nc')      
        
    coverage = TimeLevelCoverage(reader); 
   
    resampledCoverage = resampleTXY(coverage);    
    #writer = WW3Writer('/home/retf/work/fieldsites/taiwan/modelling/mercator/test.nc')  
    #writer.write_axis(resampledCoverage);    
    #writer.write_variable_wlv(resampledCoverage);
    #writer.close() 
    
    #writer = GMTWriter('/home/retf/work/fieldsites/taiwan/modelling/mercator/ww3.ascii') 
    #writer.write_variable_current_at_time_and_level(coverage,0,0);
    
    #writer = GMTWriter('/home/retf/work/fieldsites/taiwan/modelling/mercator/ww3.ascii') 
    #writer.write_variable_current_at_time_and_level(coverage,0,0);
    
    writer = WW3Writer('/home/retf/work/fieldsites/taiwan/modelling/mercator/ww3.nc')  
    writer.write_axis(coverage);    
    writer.write_variable_wlv(coverage);
    writer.write_variable_current_at_level(coverage,0);   
    writer.close() 
    
    #ww3Reader = WW3Reader('/home/retf/work/fieldsites/med-cruesim/modelling/waves/large-scale/outputs/netcdf/ww3.201207.nc')     
    #ww3Coverage = TimeCoverage(ww3Reader);  
    #writer = WW3Writer('/home/retf/work/fieldsites/taiwan/modelling/mercator/ww3.nc')  
    #writer.write_axis(ww3Coverage);    
    #writer.write_variable_wlv(ww3Coverage);    
    #writer.close() 
    
    writer = GMTWriter('/home/retf/work/fieldsites/taiwan/modelling/mercator/gmt/surface-current.nc')  
    writer.write_axis(resampledCoverage);    
    writer.write_variable_wlv(resampledCoverage);   
    writer.write_variable_surface_current(resampledCoverage)
    writer.close() 
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
