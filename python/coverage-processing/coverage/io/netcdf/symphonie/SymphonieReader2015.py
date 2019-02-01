#! #! /usr/bin/env python2.7
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
# Author : Fabien Rétif - fabien.retif@zoho.com
#
from __future__ import division, print_function, absolute_import
from coverage.io.File import File
from netCDF4 import Dataset, num2date
import numpy as np
from coverage.io.netcdf.symphonie.SymphonieReader import SymphonieReader

class SymphonieReader2015(File,SymphonieReader):
    """
La classe SymphonieReader permet de lire les données du format Symphonie

@param  myGrid : lien vers le fichier de grille (que l'on trouve dans le RDIR/tmp/grid.nc)
@param myFile : lien vers le fichier de données (que l'on trouve dans GRAPHIQUES)
"""
    def __init__(self,myGrid, myFile):   
        File.__init__(self,myFile);
        SymphonieReader.__init__(self,myGrid,myFile);
        
    def read_variable_ssh_at_time(self,index_t):
        return self.ncfile.variables["ssh"][index_t][:]

    def read_variable_current_at_time_and_depth_and_location(self,index_t,index_z,index_x,index_y):
        mask_t = self.read_variable_3D_mask();
        mask_u = self.grid.variables["mask_u"][index_y,index_x];
        mask_v = self.grid.variables["mask_v"][index_y,index_x];
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

        if index_z != -999 : # Le point (x,y) a une couche de profondeur depth

            if mask_t[index_z,index_y,index_x] == 1.:

                ##############################
                #           v_up
                #
                #   u_left   X     u_right
                #
                #         v_bottom
                #############################

                # u_left
                u_left = 0
                if mask_u[index_z,index_y,index_x-1] == 1.:
                    # Pas d'interpolation, on prend le plus proche inférieur
                    u_left = data_u[index_z,index_y,index_x-1];

                # u_right
                u_right = 0
                if mask_u[index_z[y,x],y,x] == 1.:
                    # Pas d'interpolation, on prend le plus proche inférieur
                    u_right = data_u[index_z[y,x],y,x];

                # v_down
                v_down = 0
                if mask_v[index_z[y,x],y-1,x] == 1.:
                    # Pas d'interpolation, on prend le plus proche inférieur
                    v_down = data_v[index_z[y,x],y-1,x];

                # v_up
                v_up = 0
                if mask_v[index_z[y,x],y,x] == 1.:
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