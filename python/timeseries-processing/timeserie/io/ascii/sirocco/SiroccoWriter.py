# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

class SiroccoWriter:
    
    UNITS = {};
    UNITS['sea_surface_wave_significant_height'] = "(m)"
    UNITS['sea_surface_wave_mean_period'] = "(s)"
    UNITS['sea_surface_wave_peak_period'] = "(s)"
    UNITS['sea_surface_wave_from_direction'] = "(deg)"
    UNITS['sea_surface_wave_peak_from_direction'] = "(deg)"
    UNITS['sea_surface_wave_to_direction'] = "(deg)"
    UNITS['sea_surface_wave_peak_to_direction'] = "(deg)"
    UNITS['sea_surface_elevation'] = "(m)"
    UNITS['sea_surface_height'] = "(m)"

    def __init__(self, myFilename):
        self.filename = myFilename   
        
    def write_waves(self,serie):
        
        data = serie.read_data();
        var = []
        
        if not 'sea_surface_wave_significant_height' in data:            
            raise ValueError("None sea_surface_significant_height variable")  
        else:
            var.append('sea_surface_wave_significant_height')            
        
        if 'sea_surface_wave_mean_period' in data:            
            var.append('sea_surface_wave_mean_period')
            
        if 'sea_surface_wave_peak_period' in data:            
            var.append('sea_surface_wave_peak_period')
            
        if 'sea_surface_wave_from_direction' in data:            
            var.append('sea_surface_wave_from_direction')       
            
        if 'sea_surface_wave_to_direction' in data:            
            var.append('sea_surface_wave_to_direction') 
            
        if 'sea_surface_wave_peak_from_direction' in data:            
            var.append('sea_surface_wave_peak_from_direction')
            
        if 'sea_surface_wave_peak_to_direction' in data:            
            var.append('sea_surface_wave_peak_to_direction') 
            
        data.to_csv(self.filename, sep='\t',columns=var,header=False, encoding='utf-8',na_rep="NaN")
          
        file = open(self.filename, "r+")        
        old = file.read() # read everything in the file
        file.seek(0) # rewind
        
        file.write("############################################################ \n\
# Station : "+str(serie.name_station)+" \n\
# Coordinate Reference System : WGS84 \n\
# Longitude : "+str(serie.x_coord)+" \n\
# Latitude : "+str(serie.y_coord)+" \n\
# Data source : "+str(serie.data_source)+" \n\
# Time zone : UTC \n\
# Separator: Tabulation \\t \n\
# Column 1: year-month-day hour:minute:second UTC \n")

        column = 2
        for key in var:
            file.write("# Column "+str(column)+": "+str(key)+" "+str(SiroccoWriter.UNITS[key])+" FillValue: NaN \n")
            column = column + 1
            
        file.write("############################################################\n")        
        
        file.write(old) # write the new line before
        file.close()
        
    def write_tide(self,serie):
        
        data = serie.read_data();
        var = []
        
        if 'sea_surface_elevation' in data: 
            var.append('sea_surface_elevation')            
        
        if 'sea_surface_height' in data:            
            var.append('sea_surface_height')
            
        if len(var) == 0:
             raise ValueError("None sea_surface_elevation variable")  
            
        data.to_csv(self.filename, sep='\t',columns=var,header=False, encoding='utf-8',na_rep="NaN")
          
        file = open(self.filename, "r+")        
        old = file.read() # read everything in the file
        file.seek(0) # rewind
        
        file.write("############################################################ \n\
# Station : "+str(serie.name_station)+" \n\
# Coordinate Reference System : WGS84 \n\
# Longitude : "+str(serie.x_coord)+" \n\
# Latitude : "+str(serie.y_coord)+" \n\
# Data source : "+str(serie.data_source)+" \n\
# Time zone : UTC \n\
# Vertical datum : "+str(serie.vertical_datum)+" \n\
# Separator: Tabulation \\t \n\
# Column 1: year-month-day hour:minute:second UTC \n")

        column = 2
        for key in var:
            file.write("# Column "+str(column)+": "+str(key)+" "+str(SiroccoWriter.UNITS[key])+" FillValue: NaN \n")
            column = column + 1
            
        file.write("############################################################\n")        
        
        file.write(old) # write the new line before
        file.close()

            