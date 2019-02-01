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
# Author : Fabien Rétif - fabien.retif@zoho.com
#
from __future__ import division, print_function, absolute_import
from coverage.io.File import File
import re
import array
from scipy.io import loadmat
import numpy as np
from datetime import datetime
from time import strftime
import logging


class MatReader(File):
    def __init__(self,xsize, ysize, myFile):
        File.__init__(self, myFile);
        self.mat = loadmat(self.filename)
        self.x_size = xsize
        self.y_size = ysize

    # Axis
    def read_axis_x(self):
        x = np.reshape(self.mat['x'], (self.y_size, self.x_size))
        axis_x = np.zeros([self.x_size])

        for i in range(0,self.x_size):
            for j in range(0,self.y_size):
                axis_x[i] = x[j,i]

        return axis_x

    def read_axis_y(self):
        y = np.reshape(self.mat['y'], (self.y_size, self.x_size))

        axis_y = np.zeros([self.y_size])

        for i in range(0, self.x_size):
            for j in range(0, self.y_size):
                axis_y[j] = y[j, i]

        return axis_y


        # Scalar
    def read_variable_bathymetry(self):
        return np.reshape(self.mat['z'], (self.y_size, self.x_size))


