# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from timeserie.TimeSerie import TimeSerie
from timeserie.io.ascii.refmar.RefmarReader import RefmarReader
from timeserie.io.ascii.bessete.BesseteReader import BesseteReader
from timeserie.io.ascii.sirocco.SiroccoWriter import SiroccoWriter
import logging
import numpy as np

if __name__ == "__main__":
    print("Transform tide data to SIROCCO format")
    
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    outDir="/home/retf/work/fieldsites/med-cruesim/raw-data/tide/"
    
    #
    # Data from BESSETE
    #    
    ## SETE-ADCP
    reader = BesseteReader('/home/retf/work/fieldsites/med-cruesim/observations/seal-level/BESSETE/WAVES_000_000_LogData.TXT')         
    serie = TimeSerie(reader,'2013-02-01','2013-05-01','3H');
    serie.name_station = "SETE-ADCP"
    serie.data_source = "GeoSciences Montpellier / Yann LEREDDE"
    serie.vertical_datum = "MSL - be careful, the instrument has probably moved during storms"
    serie.x_coord="3.639617"
    serie.y_coord="43.333917"
    logging.info(str(serie.name_station)) 
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_tide_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_tide(serie) 
    
    #
    # Data from Refmar
    #    
    sourceDirRefmar = "/home/retf/work/fieldsites/med-cruesim/observations/seal-level/REFMAR/"
    
    ## AJACCIO_ASPRETTO
    reader = RefmarReader(sourceDirRefmar+'Ajaccio_aspretto.txt')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "AJACCIO_ASPRETTO"
    serie.data_source = "SHOM / OCA / Marine nationale"
    serie.vertical_datum = "zero_hydrographique"
    serie.x_coord="8.76284981"
    serie.y_coord="41.92279816"
    logging.info(str(serie.name_station))  
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_tide_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_tide(serie)
    
    ## CENTURI
    reader = RefmarReader(sourceDirRefmar+'Centuri.txt')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "CENTURI"
    serie.data_source = "SHOM / Mairie de Centuri"
    serie.vertical_datum = "zero_hydrographique"
    serie.x_coord="9.349833"
    serie.y_coord="42.965775"
    logging.info(str(serie.name_station))  
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_tide_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_tide(serie)
    
    ## FOS-SUR-MER
    reader = RefmarReader(sourceDirRefmar+'Fos-sur-mer.txt')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "FOS-SUR-MER"
    serie.data_source = "SHOM / GPM de Marseille"
    serie.vertical_datum = "zero_hydrographique"
    serie.x_coord="4.892935"
    serie.y_coord="43.404935"
    logging.info(str(serie.name_station))  
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_tide_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_tide(serie)
    
    ## MARSEILLE
    reader = RefmarReader(sourceDirRefmar+'Marseille.txt')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "MARSEILLE"
    serie.data_source = "SHOM / IGN"
    serie.vertical_datum = "zero_hydrographique"
    serie.x_coord="5.353758"
    serie.y_coord="43.278814"
    logging.info(str(serie.name_station))  
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_tide_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_tide(serie)
    
    ## PORT-VENDRES
    reader = RefmarReader(sourceDirRefmar+'Port-vendres.txt')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "PORT-VENDRES"
    serie.data_source = "SHOM / Region Languedoc-Roussillon / CG Pyrenees Orientales"
    serie.vertical_datum = "zero_hydrographique"
    serie.x_coord="3.10745"
    serie.y_coord="42.519922"
    logging.info(str(serie.name_station))  
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_tide_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_tide(serie)
    
    ## SETE
    reader = RefmarReader(sourceDirRefmar+'Sete.txt')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "SETE"
    serie.data_source = "SHOM / Region Languedoc-Roussillon"
    serie.vertical_datum = "zero_hydrographique"
    serie.x_coord="3.699105"
    serie.y_coord="43.397633"
    logging.info(str(serie.name_station))  
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_tide_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_tide(serie)
    
    ## SOLENZARA
    reader = RefmarReader(sourceDirRefmar+'Sete.txt')      
    serie = TimeSerie(reader,'2010-01-01','2016-01-01','H');
    serie.name_station = "SOLENZARA"
    serie.data_source = "SHOM / Mairie de Sari-Solenzara"
    serie.vertical_datum = "zero_hydrographique"
    serie.x_coord="9.40383"
    serie.y_coord="41.856856"
    logging.info(str(serie.name_station))  
    writer = SiroccoWriter(outDir+str(serie.name_station)+'_tide_'+str(serie.time_range[0].strftime("%Y"))+'_to_'+str(serie.time_range[serie.time_range.size-1].strftime("%Y"))+'.dat');
    writer.write_tide(serie)
      
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
