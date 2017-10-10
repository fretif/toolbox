# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.io.File import File

class GMTWriter(File):

    def __init__(self,cov,myFile):
        self.coverage = cov;
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
        
    def write_variable_current_at_time_and_depth(self,time,z):
        
        lon = self.coverage.read_axis_x()
        lat = self.coverage.read_axis_y()
        cur = self.coverage.read_variable_current_at_time_and_depth(time,z)
        mask = self.coverage.read_variable_2D_mask()
        
        file = open(self.filename, "w")  
        file.write("#Longitude \t Latitude \t u comp (m/s) \t v comp (m/s)\n")
        for i in range(0, self.coverage.get_x_size(),6):
            for j in range(0, self.coverage.get_y_size(),6):
                    if(mask[j,i]==1.):
                        file.write(str(lon[j,i])+"\t"+str(lat[j,i])+"\t"+str(cur[0][j,i])+"\t"+str(cur[1][j,i])+"\n")
                
        file.close()
        
    def write_variable_current_at_time(self,time):
        
        lon = self.coverage.read_axis_x()
        lat = self.coverage.read_axis_y()
        ucur = self.coverage.read_variable_u_current_at_time(time)
        vcur = self.coverage.read_variable_v_current_at_time(time)
        
        file = open(self.filename, "w")  
        file.write("#Longitude \t Latitude \t u comp (m/s) \t v comp (m/s)\n")  
        for i in range(0, self.coverage.get_x_size()):
            for j in range(0, self.coverage.get_y_size()):
                
                file.write(str(lon[j,i])+"\t"+str(lat[j,i])+"\t"+str(ucur[j,i])+"\t"+str(vcur[j,i])+"\n")  
                
        file.close()

    def write_variable_ssh_at_time(self, time):

        lon = self.coverage.read_axis_x()
        lat = self.coverage.read_axis_y()
        ssh = self.coverage.read_variable_ssh_at_time(time)

        file = open(self.filename, "w")
        file.write("#Longitude \t Latitude \t u comp (m/s) \t v comp (m/s)\n")
        for i in range(0, self.coverage.get_x_size()):
            for j in range(0, self.coverage.get_y_size()):
                file.write(
                    str(lon[j, i]) + "\t" + str(lat[j, i]) + "\t" + str(ssh[j, i]) + "\n")

        file.close()

