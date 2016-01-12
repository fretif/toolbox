# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.io.netcdf.ww3.WW3Reader import WW3Reader
from coverage.io.ascii.gmt.GMTWriter import GMTWriter
from coverage.TYXCoverage import TYXCoverage
from datetime import datetime


if __name__ == "__main__":
    print("Hello World")
    
    #Read file
    reader = WW3Reader('/home/retf/work/fieldsites/taiwan/modelling/waves/KR-WAVES-001/graphiques/ww3.20120619.nc')     
    coverage = TYXCoverage(reader);
    
    #At the given time
    selectedTime=datetime(2012,06,19,11,31)  
    #coverage.read_data_at_time("hs",selectedTime)
    
    #writer = GMTWriter('/home/retf/work/fieldsites/taiwan/modelling/waves/KR-WAVES-001/graphiques/ww3.20120619_113100_two.dat',coverage)     
    #writer.write_vector_at_time("utwo","vtwo",selectedTime)
    
    #writer = GMTWriter('/home/retf/work/fieldsites/taiwan/modelling/waves/KR-WAVES-001/graphiques/ww3.20120619_113100_wnd.dat',coverage)     
    #writer.write_vector_at_time("uwnd","vwnd",selectedTime)
    
    writer = GMTWriter('/home/retf/work/fieldsites/taiwan/modelling/waves/KR-WAVES-001/graphiques/ww3.20120619_113100_taw.dat',coverage)     
    writer.write_vector_at_time("utaw","vtaw",selectedTime)
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
