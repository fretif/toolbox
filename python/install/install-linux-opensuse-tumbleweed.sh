#!/bin/bash

# 1. Installation des entêtes Python & librairies essentielles
sudo zypper install python-devel lapack freetype-devel libpng-devel libX11-devel libXaw-devel m4 patch make libexpat-devel

# 2. Installation de gfortran & g++ & git
sudo zypper install gcc gcc-c++ gcc-fortran

source ./install-linux-common.sh

