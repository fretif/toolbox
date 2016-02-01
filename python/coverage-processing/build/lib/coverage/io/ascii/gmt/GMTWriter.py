# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import math as math

class GMTWriter:

    def __init__(self, myFilename, myCoverage):
        self.filename = myFilename; 
        self.coverage = myCoverage;
        
    def write_vector_at_time(self,uvar,vvar,selectedTime): 
        
        lon = self.coverage.read_axis_x()
        lat = self.coverage.read_axis_y()
        u =  self.coverage.read_data_at_time(uvar,selectedTime)
        v =  self.coverage.read_data_at_time(vvar,selectedTime)       
        
        file = open(self.filename, "w")       
        for i in range(0, len(lon[1])):
            for j in range(0, len(lon)):    
                #print i,j
                
                #file.write(str(lon[j,i])+"\t"+str(lat[j,i])+"\t"+str(math.degrees(math.atan2(v[j,i],u[j,i]))+180)+"\t"+str(math.sqrt(u[j,i]**2 + v[j,i]**2))+"\t"+str(math.sqrt(u[j,i]**2 + v[j,i]**2))+"\n")          
                file.write(str(lon[j,i])+"\t"+str(lat[j,i])+"\t"+str(u[j,i])+"\t"+str(v[j,i])+"\n")          
           
            
        file.close()

