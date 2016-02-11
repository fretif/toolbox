# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.io.File import File

class GMTWriter(File):

    def __init__(self, myFile):
        File.__init__(self,myFile);         
        
    def write_variable_bathymetry(self): 
        
        lon = self.coverage.read_axis_x()
        lat = self.coverage.read_axis_y()
        data =  self.coverage.read_variable_bathymetry() 
        
        file = open(self.filename, "w")  
        file.write("#Longitude \t Latitude \t h (m)\n")  
        for i in range(0, len(lon[1])):
            for j in range(0, len(lon)):    
                #print i,j
                
                file.write(str(lon[j,i])+"\t"+str(lat[j,i])+"\t"+str(data[j,i])+"\n")
            
        file.close()
        
    def write_variable_current_at_time_and_level(self,coverage,time,z):
        
        lon = coverage.read_axis_x()
        lat = coverage.read_axis_y()
        ucur = coverage.read_variable_u_current_at_time_and_level(time,z)
        vcur = coverage.read_variable_v_current_at_time_and_level(time,z)
        
        file = open(self.filename, "w")  
        file.write("#Longitude \t Latitude \t u comp (m/s) \t v comp (m/s)\n")
        for i in range(0, coverage.get_x_size()):
            for j in range(0, coverage.get_y_size()):               
                    file.write(str(lon[j,i])+"\t"+str(lat[j,i])+"\t"+str(ucur[j,i])+"\t"+str(vcur[j,i])+"\n")  
                
        file.close()
        
    def write_variable_current_at_time(self,coverage,time):
        
        lon = self.coverage.read_axis_x()
        lat = self.coverage.read_axis_y()
        ucur = coverage.read_variable_u_current_at_time(time)
        vcur = coverage.read_variable_v_current_at_time(time)
        
        file = open(self.filename, "w")  
        file.write("#Longitude \t Latitude \t u comp (m/s) \t v comp (m/s)\n")  
        for i in range(0, self.coverage.get_x_size()):
            for j in range(0, self.coverage.get_y_size()):
                
                file.write(str(lon[j,i])+"\t"+str(lat[j,i])+"\t"+str(ucur[j,i])+"\t"+str(vcur[j,i])+"\n")  
                
        file.close()

