# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from coverage.TimeCoverage import TimeCoverage
from netCDF4 import Dataset, num2date
import numpy as np

class MercatorReader: 
    
    def __init__(self,m,d,t,u,v): 
        self.mask = Dataset(m, 'r')
        self.grid2D = Dataset(d, 'r')
        self.gridT = Dataset(t, 'r') 
        self.gridU = Dataset(u, 'r')  
        self.gridV = Dataset(v, 'r') 
     
    # Axis
    def read_axis_t(self,timestamp):
        """Attention si gridT, U,V,2D ont un time_counter different"""
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
        return self.gridT.variables['deptht']
    
    # Data    
    def read_variable_mask(self): 
        return self.mask.variables["tmask"][:]
    
    def read_variable_ssh_at_time(self,t):
        return self.grid2D.variables["sossheig"][t][:]
     
    def read_variable_current_at_time_and_level(self,t,z):
        mask_t = self.read_variable_mask();
        mask_u = self.mask.variables["umask"][:];
        mask_v = self.mask.variables["vmask"][:];
        lon_t = self.read_axis_x();
        lat_t = self.read_axis_y();
        data_u = self.gridU.variables["vozocrtx"][t][::]
        data_v = self.gridV.variables["vomecrty"][t][::]
        
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

        # We process points inside the domain
        for y in range(1,ymax-1):
            for x in range(1,xmax-1):
                
                x1=(lon_t[y,x+1]-lon_t[y,x-1])*np.pi/180.
                if(x1<-np.pi): x1=x1+2.*np.pi
                if(x1> np.pi): x1=x1-2.*np.pi
                x0=-np.arctan2((lat_t[y,x+1]-lat_t[y,x-1])*np.pi/180.,x1*np.cos(lat_t[y,x]*np.pi/180.))
                gridrotcos_t[y,x]=np.cos(x0)
                gridrotsin_t[y,x]=np.sin(x0)

                if (mask_t[0,z[y,x],y,x] == 1.):
                    
                    u_left = 0
                    u_right = 0
                    v_down = 0
                    v_up = 0
                   
                    if (mask_u[0,z[y,x-1],y,x-1] == 1.):
                        u_left = data_u[z[y,x-1],y,x-1];

                    if (mask_u[0,z[y,x],y,x] == 1.):
                        u_right = data_u[z[y,x],y,x];

                    if (mask_v[0,z[y-1,x],y-1,x] == 1.):
                        v_down = data_v[z[y-1,x],y-1,x];

                    if (mask_v[0,z[y,x],y,x] == 1.):
                        v_up = data_v[z[y,x],y,x];

                    # compute an half-value
                    u[y,x]=0.5*(u_left+u_right)
                    v[y,x]=0.5*(v_down+v_up)
                    
                    # apply rotation                
                    u_rot[y,x]=u[y,x]*gridrotcos_t[y,x]+v[y,x]*gridrotsin_t[y,x]
                    v_rot[y,x]=-u[y,x]*gridrotsin_t[y,x]+v[y,x]*gridrotcos_t[y,x]   
          
        # We process boundaries points     
        # bottom        
        u_rot[0,0:xmax]=u_rot[1,0:xmax]   
        v_rot[0,0:xmax]=v_rot[1,0:xmax] 
        # up
        u_rot[ymax-1,0:xmax]=u_rot[ymax-2,0:xmax] 
        v_rot[ymax-1,0:xmax]=v_rot[ymax-2,0:xmax] 
        
        # left
        u_rot[0:ymax,0]=u_rot[0:ymax,1]   
        v_rot[0:ymax,0]=v_rot[0:ymax,1]   
        # right
        u_rot[0:ymax,xmax-1]=u_rot[0:ymax,xmax-2]  
        v_rot[0:ymax,xmax-1]=v_rot[0:ymax,xmax-2]  

        return [u_rot,v_rot]

