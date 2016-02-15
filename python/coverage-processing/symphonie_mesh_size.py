# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.Coverage import Coverage
from coverage.io.netcdf.symphonie.SymphonieReader import SymphonieReader
from coverage.operator.interpolator.models.Symphonie import resample_type_2
import logging

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s] %(message)s',level=logging.INFO)
    
    # Read file    
    symphonieReader = SymphonieReader('/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/graphiques/grid.nc','/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/simulation/grid.nc')     
    coverage = Coverage(symphonieReader);
    
    #resample_type_2(coverage,0.01,0.01,'/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/graphiques/regular/grid.nc') 
    
    lon = coverage.read_axis_x()
    lat = coverage.read_axis_y()
    mesh_size = coverage.reader.read_variable_mesh_size();
    mask = coverage.reader.read_variable_mask();
    bathy = coverage.reader.read_variable_bathymetry();
   
    file = open('/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/graphiques/mesh_size_50m.xyz', "w")  
    file.write("#Longitude \t Latitude \t mesh size(m)\n")  
    for i in range(0, coverage.get_x_size(),3):
        for j in range(0, coverage.get_y_size(),3):
            
            if(mask[j,i]==1 and bathy[j,i]<50):
                file.write(str(lon[j,i])+"\t"+str(lat[j,i])+"\t"+str(mesh_size[j,i])+"\n")  

    file.close()
    
    file = open('/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/graphiques/mesh_size_500m.xyz', "w")  
    file.write("#Longitude \t Latitude \t mesh size(m)\n")  
    for i in range(0, coverage.get_x_size(),6):
        for j in range(0, coverage.get_y_size(),6):
            
            if(mask[j,i]==1 and bathy[j,i]>50 and bathy[j,i]<500):
                file.write(str(lon[j,i])+"\t"+str(lat[j,i])+"\t"+str(mesh_size[j,i])+"\n")  

    file.close()
    
    file = open('/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/graphiques/mesh_size_1000m.xyz', "w")  
    file.write("#Longitude \t Latitude \t mesh size(m)\n")  
    for i in range(0, coverage.get_x_size(),10):
        for j in range(0, coverage.get_y_size(),10):
            
            if(mask[j,i]==1):
                file.write(str(lon[j,i])+"\t"+str(lat[j,i])+"\t"+str(mesh_size[j,i])+"\n")  

    file.close()
    
    print 'End of programm'
     
    
    
    
       
        
    
    
    
    
    
