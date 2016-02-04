# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.TimeCoverage import TimeCoverage
from netCDF4 import Dataset, num2date
import numpy as np

class MercatorReader: 
    
    def __init__(self,m,t,u,v): 
        self.mask = Dataset(m, 'r')
        self.gridT = Dataset(t, 'r') 
        self.gridU = Dataset(u, 'r')  
        self.gridV = Dataset(v, 'r') 
     
    # Axis
    def read_axis_t(self,timestamp):
        data = self.gridT.variables['time_counter'][:]        
        result = num2date(data, units = self.gridT.variables['time_counter'].units, calendar = self.gridT.variables['time_counter'].calendar)
        
        if timestamp ==1:           
            return [ (t - TimeCoverage.TIME_DATUM).total_seconds() \
                for t in result];
        else:            
            return result
    
    def read_axis_x(self):        
        return self.gridT.variables['nav_lon'][:]
    
    def read_axis_y(self):        
        return self.gridT.variables['nav_lat'][:]
    
    def read_axis_z(self):       
        return self.gridT.variables['deptht'][::] 
    
    # Data    
    def read_variable_mask(self): 
        return self.mask.variables["tmask"][:]
    
    def read_variable_wlv_at_time(self,t):    
        return self.gridT.variables["sossheig"][t][:]
     
    def read_variable_u_current_at_time_and_level(self,t,z):
        mask_t = self.read_variable_mask();
        mask_u = self.mask.variables["umask"][:];
        mask_v = self.mask.variables["vmask"][:];
        lon_t = self.read_axis_x();
        lat_t = self.read_axis_y();
        data_u = self.gridU.variables["vozocrtx"][t][z][:]  
        data_v = self.gridV.variables["vomecrty"][t][z][:]  
        
        # compute and apply rotation matrix
        xmax=np.shape(lon_t)[1]
        ymax=np.shape(lon_t)[0]
        gridrotcos_t = np.zeros([ymax,xmax])
        gridrotsin_t = np.zeros([ymax,xmax])       
        
        u = np.zeros([ymax,xmax])
        u[:] = np.NAN
        v = np.zeros([ymax,xmax])
        v[:] = np.NAN
        u_rot = np.zeros([ymax,xmax])
        u_rot[:] = np.NAN
        v_rot = np.zeros([ymax,xmax])
        v_rot[:] = np.NAN
        
        for y in range(0,ymax-1):
            for x in range(0,xmax-1):
                
                # compute rotation matrix
                x1=(lon_t[y,x+1]-lon_t[y,x-1])*np.pi/180.
                if(x1<-np.pi): x1=x1+2.*np.pi
                if(x1> np.pi): x1=x1-2.*np.pi
                x0=-np.arctan2((lat_t[y,x+1]-lat_t[y,x-1])*np.pi/180.,x1*np.cos(lat_t[y,x]*np.pi/180.))
                gridrotcos_t[y,x]=np.cos(x0)
                gridrotsin_t[y,x]=np.sin(x0)
                
                if (mask_t[0,0,y,x]==1.):
                    
                    # center on _t grid
                    if (mask_u[0,0,y,x]==1. and mask_u[0,0,y,x+1]==1. and mask_v[0,0,y,x]==1. and mask_v[0,0,y+1,x]==1.):
                              u[y,x]=0.5*(data_u[y,x]+data_u[y,x+1])
                              v[y,x]=0.5*(data_v[y,x]+data_v[y+1,x])
                    else:
                        # copy boundaries points 
                        #print y,x
                        u[y,x] = data_u[y,x]
                        v[y,x] = data_v[y,x]
                
                # apply rotation                
                u_rot[y,x]=u[y,x]*gridrotcos_t[y,x]+v[y,x]*gridrotsin_t[y,x]
                v_rot[y,x]=-u[y,x]*gridrotsin_t[y,x]+v[y,x]*gridrotcos_t[y,x]
      
        
        return u_rot               
	
        
    def read_variable_v_current_at_time_and_level(self,t,z): 
        mask_t = self.read_variable_mask();
        mask_u = self.mask.variables["umask"][:];
        mask_v = self.mask.variables["vmask"][:];
        lon_t = self.read_axis_x();
        lat_t = self.read_axis_y();
        data_u = self.gridU.variables["vozocrtx"][t][z][:]  
        data_v = self.gridV.variables["vomecrty"][t][z][:]  
        
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
  

    