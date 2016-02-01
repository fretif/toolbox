# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.io.netcdf.ww3.WW3Reader import WW3Reader
from coverage.io.netcdf.symphonie.SymphonieReader import SymphonieReader
from coverage.TYXCoverage import TYXCoverage
from coverage.ZYXCoverage import ZYXCoverage
import numpy as np

if __name__ == "__main__":
    print("Hello World !")
    
     #Read file
    ww3Reader = WW3Reader('/home/retf/work/fieldsites/med-cruesim/modelling/waves/gulf-of-lion/graphiques/ww3.20120701.nc')     
    ww3Coverage = TYXCoverage(ww3Reader);
    
    symphonieReader = SymphonieReader('/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/simulation/grid.nc')     
    symphonieCoverage = ZYXCoverage(symphonieReader);
    
    ww3Lon = ww3Coverage.read_axis_x()
    ww3Lat = ww3Coverage.read_axis_y()
    ww3Mask = ww3Coverage.read_data("MAPSTA");
    ww3Bathy = ww3Coverage.reader.read_data_at_time("dpt",0);    
    symphonieLon = symphonieCoverage.read_axis_x()
    symphonieLat = symphonieCoverage.read_axis_y()
    symphonieMask = symphonieCoverage.read_data_at_level("mask_t",0);
    symphonieBathy = symphonieCoverage.read_data("hm_w");
    
    print "Grille Symphonie : "+str(len(symphonieLon[1]))+"/"+str(len(symphonieLon))
    print "Grille WaveWatch III : "+str(len(ww3Lon[1]))+"/"+str(len(ww3Lon))
    
    file = open('/home/retf/work/fieldsites/med-cruesim/modelling/grid-comparaison.dat', "w")       
    for i in range(0, len(ww3Lon[1])):
        for j in range(0, len(ww3Lon)):
            
            if ww3Mask[j,i] == 2:
                ww3Mask[j,i] = 1                
            
            try:            
                np.testing.assert_approx_equal(symphonieLon[j,i],ww3Lon[j,i], 7)
                np.testing.assert_approx_equal(symphonieLat[j,i],ww3Lat[j,i],7)
                np.testing.assert_approx_equal(symphonieBathy[j,i],ww3Bathy[j,i],7)      
                np.testing.assert_approx_equal(symphonieMask[j,i],ww3Mask[j,i],0)                
            except AssertionError:
                print str(symphonieLon[j,i])+" "+str(symphonieLat[j,i])+" "+str(symphonieBathy[j,i])+" "+str(symphonieMask[j,i])+" !=  "+str(ww3Lon[j,i])+" "+str(ww3Lat[j,i])+" "+str(ww3Bathy[j,i])+" "+str(ww3Mask[j,i])
                file.write(str(symphonieLon[j,i])+"\t"+str(symphonieLat[j,i])+"\t"+str(symphonieBathy[j,i])+"\t"+str(symphonieMask[j,i])+" !=  "+str(ww3Lon[j,i])+"\t"+str(ww3Lat[j,i])+"\t"+str(ww3Bathy[j,i])+"\t"+str(ww3Mask[j,i])+"\n")  

    file.close()
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
