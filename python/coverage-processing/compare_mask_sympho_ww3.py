# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.io.netcdf.ww3.WW3Reader import WW3Reader
from coverage.io.netcdf.symphonie.SymphonieReader import SymphonieReader
from coverage.TimeLevelCoverage import TimeLevelCoverage
from coverage.LevelCoverage import LevelCoverage
import numpy as np
import logging

if __name__ == "__main__":
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file
    ww3Reader = WW3Reader('/home/retf/work/fieldsites/med-cruesim/modelling/waves/gulf-of-lion/graphiques/ww3.20120701.nc')     
    ww3Coverage = TimeLevelCoverage(ww3Reader);
    
    symphonieReader = SymphonieReader('/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/simulation/grid.nc','/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/simulation/grid.nc')     
    symphonieCoverage = LevelCoverage(symphonieReader);
    
    ww3Lon = ww3Coverage.read_axis_x()
    ww3Lat = ww3Coverage.read_axis_y()
    ww3Mask = ww3Coverage.reader.read_variable_mask();
    ww3Bathy = ww3Coverage.reader.read_variable_bathy_at_time(0);    
    symphonieLon = symphonieCoverage.read_axis_x()
    symphonieLat = symphonieCoverage.read_axis_y()
    symphonieMask = symphonieCoverage.reader.read_variable_mask();
    symphonieBathy = symphonieCoverage.reader.read_variable_bathy();
    
    logging.info("Grille Symphonie : "+str(symphonieCoverage.get_x_size())+"/"+str(symphonieCoverage.get_y_size()))
    logging.info("Grille WaveWatch III : "+str(ww3Coverage.get_x_size())+"/"+str(ww3Coverage.get_y_size()))
    
    for i in range(0, ww3Coverage.get_x_size()):
        for j in range(0, ww3Coverage.get_y_size()):
            
            if ww3Mask[j,i] == 2:
                ww3Mask[j,i] = 1                
            
            try:            
                np.testing.assert_approx_equal(symphonieLon[j,i],ww3Lon[j,i], 7)
                np.testing.assert_approx_equal(symphonieLat[j,i],ww3Lat[j,i],7)
                np.testing.assert_approx_equal(symphonieBathy[j,i],ww3Bathy[j,i],7)      
                np.testing.assert_approx_equal(symphonieMask[0,j,i],ww3Mask[j,i],0)                
            except AssertionError:
                logging.warning(str(symphonieLon[j,i])+" "+str(symphonieLat[j,i])+" "+str(symphonieBathy[j,i])+" "+str(symphonieMask[j,i])+" !=  "+str(ww3Lon[j,i])+" "+str(ww3Lat[j,i])+" "+str(ww3Bathy[j,i])+" "+str(ww3Mask[j,i]))                
   
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
