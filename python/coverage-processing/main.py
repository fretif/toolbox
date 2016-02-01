# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.io.netcdf.ww3.WW3Reader import WW3Reader
from coverage.io.ascii.gmt.GMTWriter import GMTWriter
from coverage.TYXCoverage import TYXCoverage
from datetime import datetime
import os


def extract_timeseries():
    # create list of month available to process
    f = open('/home/retf/work/fieldsites/taiwan/modelling/hydro/regional/KRC-WAVES-001/simulation/KRC-WAVES-001/LIST/list_taw')
    #f = open('/home/retf/work/fieldsites/taiwan/modelling/waves/KR-WAVES-001/simulation-v5.07-1/graphiques/list_taw')
    
    for nc in f:
        #Read file
        reader = WW3Reader(nc.strip())     
        coverage = TYXCoverage(reader);
        
        for time in coverage.get_times():
            
            print time
            
            writer = GMTWriter('/home/retf/work/fieldsites/taiwan/modelling/waves/KR-WAVES-001/simulation-v5.07-1/graphiques/ascii/ww3.'+str(time).replace(' ','_')+'_two.dat',coverage)     
            writer.write_vector_at_time("utwo","vtwo",time)

            writer = GMTWriter('/home/retf/work/fieldsites/taiwan/modelling/waves/KR-WAVES-001/simulation-v5.07-1/graphiques/ascii/ww3.'+str(time).replace(' ','_')+'_wnd.dat',coverage)     
            writer.write_vector_at_time("uwnd","vwnd",time)

            writer = GMTWriter('/home/retf/work/fieldsites/taiwan/modelling/waves/KR-WAVES-001/simulation-v5.07-1/graphiques/ascii/ww3.'+str(time).replace(' ','_')+'_taw.dat',coverage)     
            writer.write_vector_at_time("utaw","vtaw",time)
            
            writer = GMTWriter('/home/retf/work/fieldsites/taiwan/modelling/waves/KR-WAVES-001/simulation-v5.07-1/graphiques/ascii/ww3.'+str(time).replace(' ','_')+'_hs.dat',coverage)     
            writer.write_vector_at_time("hs","dir",time) 
            
    f.close()
    

def extract_single_data():
     #Read file
    reader = WW3Reader('/home/retf/work/fieldsites/taiwan/modelling/waves/KR-WAVES-001/simulation-v5.07-3/graphiques/ww3.20120619.nc')     
    coverage = TYXCoverage(reader);

    #At the given time
    time=datetime(2012,06,19,12,00)  
    #coverage.read_data_at_time("hs",selectedTime)

    writer = GMTWriter('/home/retf/work/fieldsites/taiwan/modelling/waves/KR-WAVES-001/simulation-v5.07-3/graphiques/ascii/ww3.'+str(time).replace(' ','_')+'_two.dat',coverage)     
    writer.write_vector_at_time("utwo","vtwo",time)

    writer = GMTWriter('/home/retf/work/fieldsites/taiwan/modelling/waves/KR-WAVES-001/simulation-v5.07-3/graphiques/ascii/ww3.'+str(time).replace(' ','_')+'_wnd.dat',coverage)     
    writer.write_vector_at_time("uwnd","vwnd",time)

    writer = GMTWriter('/home/retf/work/fieldsites/taiwan/modelling/waves/KR-WAVES-001/simulation-v5.07-3/graphiques/ascii/ww3.'+str(time).replace(' ','_')+'_taw.dat',coverage)     
    writer.write_vector_at_time("utaw","vtaw",time)
    
    writer = GMTWriter('/home/retf/work/fieldsites/taiwan/modelling/waves/KR-WAVES-001/simulation-v5.07-3/graphiques/ascii/ww3.'+str(time).replace(' ','_')+'_hs.dat',coverage)     
    writer.write_vector_at_time("hs","dir",time) 
    
def compare_mask():
     #Read file
    reader = WW3Reader('/home/retf/work/fieldsites/med-cruesim/modelling/waves/gulf-of-lion/graphiques/ww3.20120701.nc')     
    coverage = TYXCoverage(reader);

    writer = GMTWriter('/home/retf/work/fieldsites/med-cruesim/modelling/waves/gulf-of-lion/ww3-bathy.dat',coverage)  
    #At the given time
    time=datetime(2012,07,01,00,00) 
    writer.write_var_at_time("dpt",time)  
    writer = GMTWriter('/home/retf/work/fieldsites/med-cruesim/modelling/waves/gulf-of-lion/ww3-mask.dat',coverage) 
    writer.write_var("MAPSTA")

if __name__ == "__main__":
    print("Hello World !")
    
    #extract_timeseries();
    #extract_single_data();
    compare_mask();
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
