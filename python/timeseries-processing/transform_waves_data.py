# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from timeserie.TimeSerie import TimeSerie
from timeserie.io.ascii.candhis.CandhisReader import CandhisReader
from timeserie.io.ascii.bessete.BesseteReader import BesseteReader
from timeserie.io.ascii.hymex.HymexReader import HymexReader
from timeserie.io.ascii.sirocco.SiroccoWriter import SiroccoWriter
import logging
import numpy as np

if __name__ == "__main__":
    print("Transform waves data to SIROCCO format")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    outDir="/home/retf/work/fieldsites/med-cruesim/raw-data/waves/"
    
    #
    # Data from HyMex
    #
    sourceDirHymex="/home/retf/work/fieldsites/med-cruesim/observations/waves/HyMex/"
    
    ## LION
    reader = HymexReader(sourceDirHymex+'Lion_HS.dat',sourceDirHymex+'Lion_TS.dat')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "LION"
    serie.data_source = "HyMex / METEO FRANCE"
    serie.x_coord="4.640000"
    serie.y_coord="42.060000"
    logging.info(str(serie.name_station)) 
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_wave_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_waves(serie)
    
    ## AZUR
    reader = HymexReader(sourceDirHymex+'Azur_HS.dat',sourceDirHymex+'Azur_TS.dat')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "AZUR"
    serie.data_source = "HyMex / METEO FRANCE"
    serie.x_coord="7.830000"
    serie.y_coord="43.38000"
    logging.info(str(serie.name_station)) 
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_wave_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_waves(serie)  
    
    #
    # Data from Candhis
    #    
    sourceDirCandhis = "/home/retf/work/fieldsites/med-cruesim/observations/waves/CANDHIS/"
    
    ## NICE
    reader = CandhisReader(sourceDirCandhis+'CANDHIS_export_pem_00601_Base.csv')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "NICE"
    serie.data_source = "CEREMA / DDTM 06"
    serie.x_coord="7.229083"
    serie.y_coord="43.634917"
    logging.info(str(serie.name_station))  
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_wave_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_waves(serie)
    
    ## BANYULS 
    reader = CandhisReader(sourceDirCandhis+'CANDHIS_export_pem_06601_Base.csv')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "BANYULS"
    serie.data_source = "CEREMA / DREAL Languedoc Roussillon / Observatoire Oceanologique de Banyuls"
    serie.x_coord="3.167667"
    serie.y_coord="42.489500"
    logging.info(str(serie.name_station)) 
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_wave_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_waves(serie)
    
    ## CAP_CORSE
    reader = CandhisReader(sourceDirCandhis+'CANDHIS_export_pem_02B02_Base.csv')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "CAP_CORSE"
    serie.data_source = "CEREMA"
    serie.x_coord="9.275167"
    serie.y_coord="43.061000"
    logging.info(str(serie.name_station)) 
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_wave_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_waves(serie)
    
    ## ESPIGUETTE
    reader = CandhisReader(sourceDirCandhis+'CANDHIS_export_pem_03001_Base.csv')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "ESPIGUETTE"
    serie.data_source = "CEREMA / DREAL Languedoc Roussillon"
    serie.x_coord="4.162500"
    serie.y_coord="43.411000"
    logging.info(str(serie.name_station)) 
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_wave_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_waves(serie)
    
    ## LE_PLANIER
    reader = CandhisReader(sourceDirCandhis+'CANDHIS_export_pem_01305_Base.csv')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "LE_PLANIER"
    serie.data_source = "CEREMA / Grand Port Maritime de Marseille"
    serie.x_coord="5.230000"
    serie.y_coord="43.208333"
    logging.info(str(serie.name_station)) 
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_wave_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_waves(serie)
    
    ## LEUCATE
    reader = CandhisReader(sourceDirCandhis+'CANDHIS_export_pem_01101_Base.csv')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "LEUCATE"
    serie.data_source = "CEREMA / DREAL Languedoc Roussillon"
    serie.x_coord="3.125000"
    serie.y_coord="42.916667"
    logging.info(str(serie.name_station)) 
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_wave_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_waves(serie)
    
    ## PORQUEROLLES
    reader = CandhisReader(sourceDirCandhis+'CANDHIS_export_pem_08301_Base.csv')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "PORQUEROLLES"
    serie.data_source = "CEREMA"
    serie.x_coord="6.204833"
    serie.y_coord="42.966667"
    logging.info(str(serie.name_station)) 
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_wave_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_waves(serie)
    
    ## SETE
    reader = CandhisReader(sourceDirCandhis+'CANDHIS_export_pem_03404_Base.csv')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "SETE"
    serie.data_source = "CEREMA / DREAL Languedoc Roussillon"
    serie.x_coord="3.779617"
    serie.y_coord="43.371017"
    logging.info(str(serie.name_station)) 
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_wave_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_waves(serie)
        
    #
    # Data from BESSETE
    #    
    ## SETE-ADCP
    reader = BesseteReader('/home/retf/work/fieldsites/med-cruesim/observations/waves/BESSETE/WAVES_000_000_LogData.TXT')         
    serie = TimeSerie(reader,'2013-02-01','2013-05-01','3H');
    serie.name_station = "SETE-ADCP"
    serie.data_source = "GeoSciences Montpellier / Yann LEREDDE"
    serie.x_coord="3.639617"
    serie.y_coord="43.333917"
    logging.info(str(serie.name_station)) 
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_wave_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_waves(serie) 
      
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
