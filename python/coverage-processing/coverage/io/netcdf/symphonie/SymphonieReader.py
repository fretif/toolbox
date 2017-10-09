#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# CoverageProcessing is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# CoverageProcessing is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

from coverage.io.File import File
from netCDF4 import Dataset, num2date
import numpy as np

class SymphonieReader(File):
    """
La classe SymphonieReader permet de lire les données du format Symphonie

@param  myGrid : lien vers le fichier de grille (que l'on trouve dans le RDIR/tmp/grid.nc)
@param myFile : lien vers le fichier de données (que l'on trouve dans GRAPHIQUES)
"""
    def __init__(self,myGrid, myFile):   
        File.__init__(self,myFile); 
        self.ncfile = Dataset(self.filename, 'r')
        self.grid = Dataset(myGrid, 'r')
        
    # Axis
    def read_axis_t(self,timestamp=0):
        data = self.ncfile.variables['time'][:]         
        result = num2date(data, units = self.ncfile.variables['time'].units.replace('from','since').replace('mar','03').replace('feb','02').replace('jun','06'), calendar = self.ncfile.variables['time'].calendar)
        
        if timestamp ==1:           
            return [ (t - TimeCoverage.TIME_DATUM).total_seconds() \
                for t in result];
        else:            
            return result
    
    def read_axis_x(self):       
        return self.grid.variables['longitude_t'][:]
    
    def read_axis_y(self):      
        return self.grid.variables['latitude_t'][:]
    
    def read_axis_z(self):
        lev = self.grid.variables['depth_t'][::]
        lev[::] *= -1.0 # inverse la profondeur
        return lev
        
    # Data    
    def read_variable_2D_mask(self):
        return self.grid.variables["mask_t"][0][:]

    def read_variable_3D_mask(self):
        return self.grid.variables["mask_t"][::]
    
    def read_variable_mesh_size(self): 
        data= self.grid.variables["sqrt_dxdy"][:]
        data[data < 0] = np.nan
        return data
    
    def read_variable_bathymetry(self): 
        return self.grid.variables["hm_w"][:]

    def read_variable_Ha(self):
        return self.ncfile.variables["Ha"][:]
    
    def read_variable_ssh_at_time(self,t):
        return self.ncfile.variables["ssh_w"][t][:]

    def read_variable_bathy_ssh_at_time(self,t):
        return self.ncfile.variables["hssh"][t][:]

    def read_variable_hs_at_time(self,t):
        return self.ncfile.variables["hs_wave_t"][t][:]

    def read_variable_waves_mean_period_at_time(self,t):
        return self.ncfile.variables["t_wave_t"][t][:]

    def read_variable_waves_dir_at_time(self, t):
        return self.ncfile.variables["dir_wave_t"][t][:]

    def read_variable_wetmask_at_time(self,t):
        return self.ncfile.variables["wetmask_t"][t][:]

    def read_variable_salinity_at_time_and_depth(self,index_t,index_z,depth,method="nearest"):
        mask_t = self.read_variable_3D_mask();
        lon_t = self.read_axis_x();
        lat_t = self.read_axis_y();
        xmax=np.shape(lon_t)[1]
        ymax=np.shape(lon_t)[0]
        data = self.ncfile.variables["sal"][index_t][:]
        sal = np.zeros([ymax,xmax])
        sal[:] = np.NAN

        for y in range(1,ymax-1):
            for x in range(1,xmax-1):

               if index_z[y,x] != -999 : # Le point (x,y) a une couche de profondeur depth

                    if mask_t[index_z[y,x],y,x] == 1.:
                        sal[y,x] = data[index_z[y,x],y,x]

        return sal

    def read_variable_current_at_time_and_depth(self,index_t,index_z,depth,method="nearest"):
        mask_t = self.read_variable_3D_mask();
        mask_u = self.grid.variables["mask_u"][:];
        mask_v = self.grid.variables["mask_v"][:];
        lon_t = self.read_axis_x();
        lat_t = self.read_axis_y();
        depth_t = self.read_axis_z()
        size_depth_t = np.shape(depth_t)[0];
        depth_u = self.grid.variables['depth_u'][::]
        depth_u[::] *= -1.0 # inverse la profondeur
        depth_v = self.grid.variables['depth_v'][::]
        depth_v[::] *= -1.0 # inverse la profondeur

        data_u = self.ncfile.variables["vel_u"][index_t][::]
        data_v = self.ncfile.variables["vel_v"][index_t][::]

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

        # 1. On calcule les points à l'intérieur du domaine en excluant les bords
        for y in range(1,ymax-1):
            for x in range(1,xmax-1):

                # 1.1 On calcule la matrice de rotation
                x1=(lon_t[y,x+1]-lon_t[y,x-1])*np.pi/180.
                if(x1<-np.pi): x1=x1+2.*np.pi
                if(x1> np.pi): x1=x1-2.*np.pi
                x0=-np.arctan2((lat_t[y,x+1]-lat_t[y,x-1])*np.pi/180.,x1*np.cos(lat_t[y,x]*np.pi/180.))
                gridrotcos_t[y,x]=np.cos(x0)
                gridrotsin_t[y,x]=np.sin(x0)

                if index_z[y,x] != -999 : # Le point (x,y) a une couche de profondeur depth

                    if mask_t[index_z[y,x],y,x] == 1.:

                        # 1.2 On interpole sur la verticale si possible et on récupère les valeurs aux points encadrant X.
                        ##############################
                        #           v_up
                        #
                        #   u_left   X     u_right
                        #
                        #         v_bottom
                        #############################

                        vert_inc=1
                        if method == "linear" and index_z[y,x]+1 >= size_depth_t:
                            vert_inc=-1

                        # u_left
                        u_left = 0
                        if (method == "linear" and mask_u[index_z[y,x],y,x-1] == 1. and mask_u[index_z[y,x]+vert_inc,y,x-1] == 1.):
                        # ATTENTION, par commodité, on utilise l'indice index_[y,x] qui est sur la grille C comme indice z des variables u et v qui sont sur une grille différente.
                        # Il peut donc exister un léger décalage.

                            # On fait une interpolation linéaire sur la verticale
                            r = (depth_u[index_z[y,x],y,x-1] - depth) / (depth_u[index_z[y,x]+vert_inc,y,x-1] - depth_u[index_z[y,x],y,x-1])
                            u_left_z1 = data_u[index_z[y,x],y,x-1];
                            u_left_z2 = data_u[index_z[y,x]+vert_inc,y,x-1];
                            u_left = u_left_z2*r + (1-r)*u_left_z1

                        elif method == "nearest" and mask_u[index_z[y,x],y,x-1] == 1.:
                            # Pas d'interpolation, on prend le plus proche inférieur
                            u_left = data_u[index_z[y,x],y,x-1];

                        # u_right
                        u_right = 0
                        if (method == "linear" and mask_u[index_z[y,x],y,x] == 1. and mask_u[index_z[y,x]+vert_inc,y,x] == 1.):

                            # On fait une interpolation linéaire sur la verticale
                            r = (depth - depth_u[index_z[y,x],y,x]) / (depth_u[index_z[y,x]+vert_inc,y,x] - depth_u[index_z[y,x],y,x])
                            u_right_z1 = data_u[index_z[y,x],y,x];
                            u_right_z2 = data_u[index_z[y,x]+vert_inc,y,x];
                            u_right = u_right_z2*r + (1-r)*u_right_z1

                        elif method == "nearest" and mask_u[index_z[y,x],y,x] == 1.:
                            # Pas d'interpolation, on prend le plus proche inférieur
                            u_right = data_u[index_z[y,x],y,x];

                        # v_down
                        v_down = 0
                        if (method == "linear" and mask_v[index_z[y,x],y-1,x] == 1. and mask_v[index_z[y,x]+vert_inc,y-1,x] == 1.):

                            # On fait une interpolation linéaire sur la verticale
                            r = (depth - depth_v[index_z[y,x],y,x]) / (depth_v[index_z[y,x]+vert_inc,y-1,x] - depth_v[index_z[y,x],y-1,x])
                            v_down_z1 = data_v[index_z[y,x],y-1,x];
                            v_down_z2 = data_v[index_z[y,x]+vert_inc,y-1,x];
                            v_down = v_down_z2*r + (1-r)*v_down_z1
                        elif method == "nearest" and mask_v[index_z[y,x],y-1,x] == 1.:
                            # Pas d'interpolation, on prend le plus proche inférieur
                            v_down = data_v[index_z[y,x],y-1,x];

                        # v_up
                        v_up = 0
                        if (method == "linear" and mask_v[index_z[y,x],y,x] == 1. and mask_v[index_z[y,x]+vert_inc,y,x] == 1.):
                            r = (depth - depth_v[index_z[y,x],y,x]) / (depth_v[index_z[y,x]+vert_inc,y,x] - depth_v[index_z[y,x],y,x])
                            v_up_z1 = data_v[index_z[y,x],y,x];
                            v_up_z2 = data_v[index_z[y,x]+vert_inc,y,x];
                            v_up = v_up_z2*r + (1-r)*v_up_z1

                        elif method == "nearest" and mask_v[index_z[y,x],y,x] == 1.:
                            # Pas d'interpolation, on prend le plus proche inférieur
                            v_up = data_v[index_z[y,x],y,x];

                        # 1.3 On calcule la demi-somme
                        u[y,x]=0.5*(u_left+u_right)
                        v[y,x]=0.5*(v_down+v_up)

                        # 1.4 On applique la rotation
                        u_rot[y,x]=u[y,x]*gridrotcos_t[y,x]+v[y,x]*gridrotsin_t[y,x]
                        v_rot[y,x]=-u[y,x]*gridrotsin_t[y,x]+v[y,x]*gridrotcos_t[y,x]

        # 2. On duplique les points sur les bords.
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

    def read_variable_current_at_time(self,index_t):
        mask_t = self.read_variable_2D_mask();
        mask_u = self.grid.variables["mask_u"][:];
        mask_v = self.grid.variables["mask_v"][:];
        lon_t = self.read_axis_x();
        lat_t = self.read_axis_y();
        depth_t = self.read_axis_z()
        size_depth_t = np.shape(depth_t)[0];
        depth_u = self.grid.variables['depth_u'][::]
        depth_u[::] *= -1.0 # inverse la profondeur
        depth_v = self.grid.variables['depth_v'][::]
        depth_v[::] *= -1.0 # inverse la profondeur

        data_u = self.ncfile.variables["velbar_u"][index_t][::]
        data_v = self.ncfile.variables["velbar_v"][index_t][::]

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

        # 1. On calcule les points à l'intérieur du domaine en excluant les bords
        for y in range(1,ymax-1):
            for x in range(1,xmax-1):

                # 1.1 On calcule la matrice de rotation
                x1=(lon_t[y,x+1]-lon_t[y,x-1])*np.pi/180.
                if(x1<-np.pi): x1=x1+2.*np.pi
                if(x1> np.pi): x1=x1-2.*np.pi
                x0=-np.arctan2((lat_t[y,x+1]-lat_t[y,x-1])*np.pi/180.,x1*np.cos(lat_t[y,x]*np.pi/180.))
                gridrotcos_t[y,x]=np.cos(x0)
                gridrotsin_t[y,x]=np.sin(x0)

                if mask_t[y,x] == 1.:

                    # 1.2 On interpole sur la verticale si possible et on récupère les valeurs aux points encadrant X.
                    ##############################
                    #           v_up
                    #
                    #   u_left   X     u_right
                    #
                    #         v_bottom
                    #############################

                    # u_left
                    u_left = 0
                    if mask_u[size_depth_t-1,y,x-1] == 1.:
                        # Pas d'interpolation, on prend le plus proche inférieur
                        u_left = data_u[y,x-1];

                    # u_right
                    u_right = 0
                    if mask_u[size_depth_t-1,y,x] == 1.:
                        # Pas d'interpolation, on prend le plus proche inférieur
                        u_right = data_u[y,x];

                    # v_down
                    v_down = 0
                    if mask_v[size_depth_t-1,y-1,x] == 1.:
                        # Pas d'interpolation, on prend le plus proche inférieur
                        v_down = data_v[y-1,x];

                    # v_up
                    v_up = 0
                    if mask_v[size_depth_t-1,y,x] == 1.:
                        # Pas d'interpolation, on prend le plus proche inférieur
                        v_up = data_v[y,x];

                    # 1.3 On calcule la demi-somme
                    u[y,x]=0.5*(u_left+u_right)
                    v[y,x]=0.5*(v_down+v_up)

                    # 1.4 On applique la rotation
                    u_rot[y,x]=u[y,x]*gridrotcos_t[y,x]+v[y,x]*gridrotsin_t[y,x]
                    v_rot[y,x]=-u[y,x]*gridrotsin_t[y,x]+v[y,x]*gridrotcos_t[y,x]

        # 2. On duplique les points sur les bords.
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

    def read_variable_wind_at_time(self,index_t):
        mask_t = self.read_variable_2D_mask();
        lon_t = self.read_axis_x();
        lat_t = self.read_axis_y();
        data_u = self.ncfile.variables["uwind_t"][index_t][::]
        data_v = self.ncfile.variables["vwind_t"][index_t][::]

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

        # 1. On calcule les points à l'intérieur du domaine en excluant les bords
        for y in range(1,ymax-1):
            for x in range(1,xmax-1):

                # 1.1 On calcule la matrice de rotation
                x1=(lon_t[y,x+1]-lon_t[y,x-1])*np.pi/180.
                if(x1<-np.pi): x1=x1+2.*np.pi
                if(x1> np.pi): x1=x1-2.*np.pi
                x0=-np.arctan2((lat_t[y,x+1]-lat_t[y,x-1])*np.pi/180.,x1*np.cos(lat_t[y,x]*np.pi/180.))
                gridrotcos_t[y,x]=np.cos(x0)
                gridrotsin_t[y,x]=np.sin(x0)

                if mask_t[y,x] == 1.:

                    # 1.4 On applique la rotation
                    u_rot[y,x]=u[y,x]*gridrotcos_t[y,x]+v[y,x]*gridrotsin_t[y,x]
                    v_rot[y,x]=-u[y,x]*gridrotsin_t[y,x]+v[y,x]*gridrotcos_t[y,x]

        # 2. On duplique les points sur les bords.
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

    def read_variable_taw_at_time(self,index_t):
        mask_t = self.read_variable_2D_mask();
        mask_u = self.grid.variables["mask_u"][:];
        mask_v = self.grid.variables["mask_v"][:];
        lon_t = self.read_axis_x();
        lat_t = self.read_axis_y();
        depth_t = self.read_axis_z()
        size_depth_t = np.shape(depth_t)[0];
        depth_u = self.grid.variables['depth_u'][::]
        depth_u[::] *= -1.0 # inverse la profondeur
        depth_v = self.grid.variables['depth_v'][::]
        depth_v[::] *= -1.0 # inverse la profondeur

        #data_u = self.ncfile.variables["wstress_u"][index_t][::]
        #data_v = self.ncfile.variables["wstress_v"][index_t][::]
        data_u = self.ncfile.variables["tawx"][index_t][::]
        data_v = self.ncfile.variables["tawy"][index_t][::]


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

        # 1. On calcule les points à l'intérieur du domaine en excluant les bords
        for y in range(1,ymax-1):
            for x in range(1,xmax-1):

                # 1.1 On calcule la matrice de rotation
                x1=(lon_t[y,x+1]-lon_t[y,x-1])*np.pi/180.
                if(x1<-np.pi): x1=x1+2.*np.pi
                if(x1> np.pi): x1=x1-2.*np.pi
                x0=-np.arctan2((lat_t[y,x+1]-lat_t[y,x-1])*np.pi/180.,x1*np.cos(lat_t[y,x]*np.pi/180.))
                gridrotcos_t[y,x]=np.cos(x0)
                gridrotsin_t[y,x]=np.sin(x0)

                if mask_t[y,x] == 1.:

                    # 1.2 On interpole sur la verticale si possible et on récupère les valeurs aux points encadrant X.
                    ##############################
                    #           v_up
                    #
                    #   u_left   X     u_right
                    #
                    #         v_bottom
                    #############################

                    # u_left
                    u_left = 0
                    if mask_u[size_depth_t-1,y,x-1] == 1.:
                        # Pas d'interpolation, on prend le plus proche inférieur
                        u_left = data_u[y,x-1];

                    # u_right
                    u_right = 0
                    if mask_u[size_depth_t-1,y,x] == 1.:
                        # Pas d'interpolation, on prend le plus proche inférieur
                        u_right = data_u[y,x];

                    # v_down
                    v_down = 0
                    if mask_v[size_depth_t-1,y-1,x] == 1.:
                        # Pas d'interpolation, on prend le plus proche inférieur
                        v_down = data_v[y-1,x];

                    # v_up
                    v_up = 0
                    if mask_v[size_depth_t-1,y,x] == 1.:
                        # Pas d'interpolation, on prend le plus proche inférieur
                        v_up = data_v[y,x];

                    # 1.3 On calcule la demi-somme
                    u[y,x]=0.5*(u_left+u_right)
                    v[y,x]=0.5*(v_down+v_up)

                    # 1.4 On applique la rotation
                    u_rot[y,x]=u[y,x]*gridrotcos_t[y,x]+v[y,x]*gridrotsin_t[y,x]
                    v_rot[y,x]=-u[y,x]*gridrotsin_t[y,x]+v[y,x]*gridrotcos_t[y,x]

        # 2. On duplique les points sur les bords.
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

    def read_variable_two_at_time(self,index_t):
        mask_t = self.read_variable_2D_mask();
        mask_u = self.grid.variables["mask_u"][:];
        mask_v = self.grid.variables["mask_v"][:];
        lon_t = self.read_axis_x();
        lat_t = self.read_axis_y();
        depth_t = self.read_axis_z()
        size_depth_t = np.shape(depth_t)[0];
        depth_u = self.grid.variables['depth_u'][::]
        depth_u[::] *= -1.0 # inverse la profondeur
        depth_v = self.grid.variables['depth_v'][::]
        depth_v[::] *= -1.0 # inverse la profondeur

        data_u = self.ncfile.variables["twox"][index_t][::]
        data_v = self.ncfile.variables["twoy"][index_t][::]

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

        # 1. On calcule les points à l'intérieur du domaine en excluant les bords
        for y in range(1,ymax-1):
            for x in range(1,xmax-1):

                # 1.1 On calcule la matrice de rotation
                x1=(lon_t[y,x+1]-lon_t[y,x-1])*np.pi/180.
                if(x1<-np.pi): x1=x1+2.*np.pi
                if(x1> np.pi): x1=x1-2.*np.pi
                x0=-np.arctan2((lat_t[y,x+1]-lat_t[y,x-1])*np.pi/180.,x1*np.cos(lat_t[y,x]*np.pi/180.))
                gridrotcos_t[y,x]=np.cos(x0)
                gridrotsin_t[y,x]=np.sin(x0)

                if mask_t[y,x] == 1.:

                    # 1.2 On interpole sur la verticale si possible et on récupère les valeurs aux points encadrant X.
                    ##############################
                    #           v_up
                    #
                    #   u_left   X     u_right
                    #
                    #         v_bottom
                    #############################

                    # u_left
                    u_left = 0
                    if mask_u[size_depth_t-1,y,x-1] == 1.:
                        # Pas d'interpolation, on prend le plus proche inférieur
                        u_left = data_u[y,x-1];

                    # u_right
                    u_right = 0
                    if mask_u[size_depth_t-1,y,x] == 1.:
                        # Pas d'interpolation, on prend le plus proche inférieur
                        u_right = data_u[y,x];

                    # v_down
                    v_down = 0
                    if mask_v[size_depth_t-1,y-1,x] == 1.:
                        # Pas d'interpolation, on prend le plus proche inférieur
                        v_down = data_v[y-1,x];

                    # v_up
                    v_up = 0
                    if mask_v[size_depth_t-1,y,x] == 1.:
                        # Pas d'interpolation, on prend le plus proche inférieur
                        v_up = data_v[y,x];

                    # 1.3 On calcule la demi-somme
                    u[y,x]=0.5*(u_left+u_right)
                    v[y,x]=0.5*(v_down+v_up)

                    # 1.4 On applique la rotation
                    u_rot[y,x]=u[y,x]*gridrotcos_t[y,x]+v[y,x]*gridrotsin_t[y,x]
                    v_rot[y,x]=-u[y,x]*gridrotsin_t[y,x]+v[y,x]*gridrotcos_t[y,x]

        # 2. On duplique les points sur les bords.
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

    def read_variable_surface_stokes_drift_at_time(self,index_t):
        mask_t = self.read_variable_2D_mask();
        mask_u = self.grid.variables["mask_u"][:];
        mask_v = self.grid.variables["mask_v"][:];
        lon_t = self.read_axis_x();
        lat_t = self.read_axis_y();
        depth_t = self.read_axis_z()
        size_depth_t = np.shape(depth_t)[0];
        depth_u = self.grid.variables['depth_u'][::]
        depth_u[::] *= -1.0 # inverse la profondeur
        depth_v = self.grid.variables['depth_v'][::]
        depth_v[::] *= -1.0 # inverse la profondeur

        data_u = self.ncfile.variables["velbarstokes_u"][index_t][::]
        data_v = self.ncfile.variables["velbarstokes_v"][index_t][::]

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

        # 1. On calcule les points à l'intérieur du domaine en excluant les bords
        for y in range(1,ymax-1):
            for x in range(1,xmax-1):

                # 1.1 On calcule la matrice de rotation
                x1=(lon_t[y,x+1]-lon_t[y,x-1])*np.pi/180.
                if(x1<-np.pi): x1=x1+2.*np.pi
                if(x1> np.pi): x1=x1-2.*np.pi
                x0=-np.arctan2((lat_t[y,x+1]-lat_t[y,x-1])*np.pi/180.,x1*np.cos(lat_t[y,x]*np.pi/180.))
                gridrotcos_t[y,x]=np.cos(x0)
                gridrotsin_t[y,x]=np.sin(x0)

                if mask_t[y,x] == 1.:

                    # 1.2 On interpole sur la verticale si possible et on récupère les valeurs aux points encadrant X.
                    ##############################
                    #           v_up
                    #
                    #   u_left   X     u_right
                    #
                    #         v_bottom
                    #############################

                    # u_left
                    u_left = 0
                    if mask_u[size_depth_t-1,y,x-1] == 1.:
                        # Pas d'interpolation, on prend le plus proche inférieur
                        u_left = data_u[y,x-1];

                    # u_right
                    u_right = 0
                    if mask_u[size_depth_t-1,y,x] == 1.:
                        # Pas d'interpolation, on prend le plus proche inférieur
                        u_right = data_u[y,x];

                    # v_down
                    v_down = 0
                    if mask_v[size_depth_t-1,y-1,x] == 1.:
                        # Pas d'interpolation, on prend le plus proche inférieur
                        v_down = data_v[y-1,x];

                    # v_up
                    v_up = 0
                    if mask_v[size_depth_t-1,y,x] == 1.:
                        # Pas d'interpolation, on prend le plus proche inférieur
                        v_up = data_v[y,x];

                    # 1.3 On calcule la demi-somme
                    u[y,x]=0.5*(u_left+u_right)
                    v[y,x]=0.5*(v_down+v_up)

                    # 1.4 On applique la rotation
                    u_rot[y,x]=u[y,x]*gridrotcos_t[y,x]+v[y,x]*gridrotsin_t[y,x]
                    v_rot[y,x]=-u[y,x]*gridrotsin_t[y,x]+v[y,x]*gridrotcos_t[y,x]

        # 2. On duplique les points sur les bords.
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
