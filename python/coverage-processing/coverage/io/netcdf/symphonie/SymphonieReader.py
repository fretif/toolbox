# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.io.File import File
from netCDF4 import Dataset
from numpy import ndarray
import datetime as datetime

class SymphonieReader(File):    


    def __init__(self,myGrid, myFile):   
        File.__init__(self,myFile); 
        self.grid = Dataset(myGrid, 'r')
        
    # Axis
    def read_axis_t(self,timestamp):
        myFile = Dataset(self.filename, 'r')
        data = myFile.variables['time'][:]        
        result = num2date(data, units = myFile.variables['time'].units, calendar = myFile.variables['time'].calendar)
        
        if timestamp ==1:           
            return [ (t - TimeCoverage.TIME_DATUM).total_seconds() \
                for t in result];
        else:            
            return result
    
    def read_axis_x(self):
        myFile = Dataset(self.filename, 'r')
        return myFile.variables['longitude_t'][:]
    
    def read_axis_y(self):
        myFile = Dataset(self.filename, 'r')
        return myFile.variables['latitude_t'][:]
    
    def read_axis_z(self):
        myFile = Dataset(self.filename, 'r')
        return myFile.variables['depth_t'][::]
        
    # Data    
    def read_variable_mask(self): 
        return self.grid.variables["mask_t"][:]
    
    def read_variable_wlv_at_time(self,t): 
        myFile = Dataset(self.filename, 'r')
        return myFile.variables["ssh_w"][t][:]
     
    def read_variable_u_current_at_time_and_level(self,t,z):
        myFile = Dataset(self.filename, 'r')
        mask_t = self.read_variable_mask();
        mask_u = self.grid.variables["mask_u"][:];
        mask_v = self.grid.variables["mask_v"][:];
        lon_t = self.read_axis_x();
        lat_t = self.read_axis_y();
        data_u = myFile.variables["vel_u"][t][z][:]  
        data_v = myFile.variables["vel_v"][t][z][:]  
        
        # compute and apply rotation matrix
        imax=np.shape(lon_t)[0]
        jmax=np.shape(lon_t)[1]
        gridrotcos_t = np.zeros([imax,jmax])
        gridrotsin_t = np.zeros([imax,jmax])
        
        u = np.zeros([imax,jmax])
        u[:] = np.NAN
        v = np.zeros([imax,jmax])
        v[:] = np.NAN
        u_rot = np.zeros([imax,jmax])
        u_rot[:] = np.NAN
        v_rot = np.zeros([imax,jmax])
        v_rot[:] = np.NAN
        
        for j in range(0,jmax-1):
            for i in range(0,imax-1):
                
                # compute rotation matrix
                x1=(lon_t[i+1,j]-lon_t[i-1,j])*np.pi/180.
                if(x1<-np.pi): x1=x1+2.*np.pi
                if(x1> np.pi): x1=x1-2.*np.pi
                x0=-np.arctan2((lat_t[i+1,j]-lat_t[i-1,j])*np.pi/180.,x1*np.cos(lat_t[i,j]*np.pi/180.))
                gridrotcos_t[i,j]=np.cos(x0)
                gridrotsin_t[i,j]=np.sin(x0)
                
                if (mask_t[0,0,i,j]==1.):
                    
                    # center on _t grid
                    if (mask_u[0,0,i,j]==1. and mask_u[0,0,i+1,j]==1. and mask_v[0,0,i,j]==1. and mask_v[0,0,i,j+1]==1.):
                              u[i,j]=0.5*(data_u[i,j]+data_u[i+1,j])
                              v[i,j]=0.5*(data_v[i,j]+data_v[i,j+1])
                            
                    # copy boundaries points
                                
                    # apply rotation
                    u_rot[i,j]=u[i,j]*gridrotcos_t[i,j]+v[i,j]*gridrotsin_t[i,j]
                    v_rot[i,j]=-u[i,j]*gridrotsin_t[i,j]+v[i,j]*gridrotcos_t[i,j]
                    
        return u_rot               
	
        
    def read_variable_v_current_at_time_and_level(self,t,z):
        myFile = Dataset(self.filename, 'r')
        mask_t = self.read_variable_mask();
        mask_u = self.grid.variables["mask_u"][:];
        mask_v = self.grid.variables["mask_v"][:];
        lon_t = self.read_axis_x();
        lat_t = self.read_axis_y();
        data_u = myFile.variables["vel_u"][t][z][:]  
        data_v = myFile.variables["vel_v"][t][z][:]  
        
        # compute and apply rotation matrix
        imax=np.shape(lon_t)[0]
        jmax=np.shape(lon_t)[1]
        gridrotcos_t = np.zeros([imax,jmax])
        gridrotsin_t = np.zeros([imax,jmax])
        
        u = np.zeros([imax,jmax])
        u[:] = np.NAN
        v = np.zeros([imax,jmax])
        v[:] = np.NAN
        u_rot = np.zeros([imax,jmax])
        u_rot[:] = np.NAN
        v_rot = np.zeros([imax,jmax])
        v_rot[:] = np.NAN
        
        for j in range(0,jmax-1):
            for i in range(0,imax-1):
                
                # compute rotation matrix
                x1=(lon_t[i+1,j]-lon_t[i-1,j])*np.pi/180.
                if(x1<-np.pi): x1=x1+2.*np.pi
                if(x1> np.pi): x1=x1-2.*np.pi
                x0=-np.arctan2((lat_t[i+1,j]-lat_t[i-1,j])*np.pi/180.,x1*np.cos(lat_t[i,j]*np.pi/180.))
                gridrotcos_t[i,j]=np.cos(x0)
                gridrotsin_t[i,j]=np.sin(x0)
                
                if (mask_t[0,0,i,j]==1.):
                    
                    # center on _t grid
                    if (mask_u[0,0,i,j]==1. and mask_u[0,0,i+1,j]==1. and mask_v[0,0,i,j]==1. and mask_v[0,0,i,j+1]==1.):
                              u[i,j]=0.5*(data_u[i,j]+data_u[i+1,j])
                              v[i,j]=0.5*(data_v[i,j]+data_v[i,j+1])
                            
                    # copy boundaries points
                                
                    # apply rotation
                    u_rot[i,j]=u[i,j]*gridrotcos_t[i,j]+v[i,j]*gridrotsin_t[i,j]
                    v_rot[i,j]=-u[i,j]*gridrotsin_t[i,j]+v[i,j]*gridrotcos_t[i,j]
                    
        return v_rot           
    