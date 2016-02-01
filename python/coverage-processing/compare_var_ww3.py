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
    ww3Reader = WW3Reader('/home/retf/work/fieldsites/med-cruesim/modelling/waves/large-scale/outputs/netcdf/ww3.201207.nc')     
    ww3Coverage = TYXCoverage(ww3Reader);  
    
    j=161
    i=183 
    
    file = open('/home/retf/work/fieldsites/med-cruesim/modelling/waves/large-scale/basic-processing/compare_values/Lion-buoy-july-2012.xyz', "w")   
    file.write("#Time (UTC)\tHS (m)\tPeriod (s)\tU comp wind (m/s)\tV comp wind (m/s)\tZ0\tU comp TAW (m2 s-2)\tV comp TAW (m2 s-2)\tU comp TWO (m2 s-2)\tV comp TWO (m2 s-2)\n")  
    
    for time in ww3Coverage.get_times(): 
        hs = ww3Coverage.read_data_at_time("hs",time);  
        period = ww3Coverage.read_data_at_time("t01",time);  
        z0 = ww3Coverage.read_data_at_time("cha",time);  
        utwo = ww3Coverage.read_data_at_time("utwo",time);  
        vtwo = ww3Coverage.read_data_at_time("vtwo",time);  
        utaw = ww3Coverage.read_data_at_time("utaw",time); 
        vtaw = ww3Coverage.read_data_at_time("vtaw",time);  
        uwnd = ww3Coverage.read_data_at_time("uwnd",time);  
        vwnd = ww3Coverage.read_data_at_time("vwnd",time); 
        
        print time
    
        file.write(str(time)+" "+str(hs[j,i])+" "+str(period[j,i])+" "+str(uwnd[j,i])+" "+str(z0[j,i])+" "+str(vwnd[j,i])+" "+str(utaw[j,i])+" "+str(vtaw[j,i])+" "+str(utwo[j,i])+" "+str(vtwo[j,i])+"\n")      
    
    file.close()
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
