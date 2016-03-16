# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.TimeLevelCoverage import TimeLevelCoverage
from coverage.io.netcdf.mercator.MercatorReader import MercatorReader
from coverage.io.netcdf.ww3.WW3Writer import WW3Writer
import logging

if __name__ == "__main__":
    print("Transform MERCATOR to WW3")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file
    reader = MercatorReader('/home/retf/work/fieldsites/med-cruesim/modelling/mercator/grid/mercator_grid.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/mercator-grid2D-2012-2013.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/mercator-gridT-2012-2013.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/mercator-gridU-2012-2013.nc',
                            '/home/retf/work/fieldsites/med-cruesim/modelling/mercator/netcdf/mercator-gridV-2012-2013.nc')      
        
    coverage = TimeLevelCoverage(reader); 
    
    writer = WW3Writer('/home/retf/work/fieldsites/med-cruesim/modelling/waves/med/config/cur/mercator-2012-2013.nc')  
    writer.write_axis(coverage);    
    writer.write_variable_wlv(coverage);
    writer.write_variable_current_at_level(coverage,0);   
    writer.close()    
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
