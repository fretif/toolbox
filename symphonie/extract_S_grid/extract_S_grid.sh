#!/bin/bash

if [[ ! -n "${scanDir}" ]] 
then
	echo "You need to define scanDir var. Maybe you try to execute this script outside the master script. Abort"
	exit
fi
	

if [[ ! -n "${workingDir}" ]] 
then
	echo "You need to define workingDir var. Maybe you try to execute this script outside the master script. Abort"
	exit
fi

if [ ! -f ${scanDir}/grille.nc ]
then
	echo "The file grille.nc doesn't exist"
    exit 1
fi

if [ ! -f ${scanDir}/grid.nc ]
then
	echo "The file grid.nc doesn't exist so some operations could not be supported"
fi

echo "Extraction of grid meta data"

# 3. Extract the grid : long/lat/lsm

grd2xyz ${scanDir}/grille.nc?longitude_t > ${workingDir}/longitude_t
grd2xyz ${scanDir}/grille.nc?latitude_t > ${workingDir}/latitude_t
grd2xyz ${scanDir}/grille.nc?longitude_u > ${workingDir}/longitude_u
grd2xyz ${scanDir}/grille.nc?latitude_u > ${workingDir}/latitude_u
grd2xyz ${scanDir}/grille.nc?longitude_v > ${workingDir}/longitude_v
grd2xyz ${scanDir}/grille.nc?latitude_v > ${workingDir}/latitude_v
grd2xyz ${scanDir}/grille.nc?longitude_f > ${workingDir}/longitude_f
grd2xyz ${scanDir}/grille.nc?latitude_f > ${workingDir}/latitude_f
grd2xyz ${scanDir}/grille.nc?dy_u > ${workingDir}/dy_u
grd2xyz ${scanDir}/grille.nc?dx_v > ${workingDir}/dy_v
grd2xyz ${scanDir}/grille.nc?dx_v > ${workingDir}/dz_t
grd2xyz ${scanDir}/grille.nc?dx_v > ${workingDir}/dxdy_t
grd2xyz ${scanDir}/grille.nc?mask_t > ${workingDir}/mask_t

join ${workingDir}/longitude_t ${workingDir}/latitude_t > ${workingDir}/grid_t.xy
join ${workingDir}/longitude_u ${workingDir}/latitude_u > ${workingDir}/grid_u.xy
join ${workingDir}/longitude_v ${workingDir}/latitude_v > ${workingDir}/grid_v.xy
join ${workingDir}/longitude_f ${workingDir}/latitude_f > ${workingDir}/grid_f.xy

# Weight for nearneighbor
join ${workingDir}/grid_t.xy ${workingDir}/dxdy_t > ${workingDir}/dxdy_t.xyz

# grid_t : Compute envelope
gmtinfo -C ${workingDir}/grid_t.xy > ${workingDir}/minmax 

Xsize_grid_t=`cat ${workingDir}/minmax | cut -f "2"`	
Xsize_grid_t=$[$Xsize_grid_t+1]
Ysize_grid_t=`cat ${workingDir}/minmax | cut -f "4"`	
Ysize_grid_t=$[$Ysize_grid_t+1]

if [[ ! -n "$Xmin" && ! -n "$Xmax" && ! -n "$Ymin" && ! -n "$Ymax" ]]
then		
	Xmin_grid_t=`cat ${workingDir}/minmax | cut -f "5"`
	Xmax_grid_t=`cat ${workingDir}/minmax | cut -f "6"`
	Ymin_grid_t=`cat ${workingDir}/minmax | cut -f "9"`
	Ymax_grid_t=`cat ${workingDir}/minmax | cut -f "10"`
else	
	Xmin_grid_t=$Xmin
	Xmax_grid_t=$Xmax
	Ymin_grid_t=$Ymin
	Ymax_grid_t=$Ymax
fi

if [[ ! -n "$Xincr" && ! -n "$Yincr" ]]
then	
	Xincr_grid_t=`echo "(($Xmax_grid_t)-($Xmin_grid_t))/$Xsize_grid_t" | bc -l`	
	Yincr_grid_t=`echo "(($Ymax_grid_t)-($Ymin_grid_t))/$Ysize_grid_t" | bc -l`
else
	Xincr_grid_t=$Xincr
	Yincr_grid_t=$Yincr
fi
envelope_grid_t="-R$Xmin_grid_t/$Xmax_grid_t/$Ymin_grid_t/$Ymax_grid_t"
projection_grid_t=-JX`echo $Xmax_grid_t- $Xmin_grid_t | bc -l`d/`echo $Ymax_grid_t- $Ymin_grid_t | bc -l`d
#projection=-JX`echo "($Xmax-$Xmin)*$mapRatioSize)" | bc -l`d/`echo "($Ymax-$Ymin)*$mapRatioSize" | bc -l`d

# grid_u : Compute envelope

if [[ ! -n "$Xsize" && ! -n "$Ysize" && ! -n "$Xmin" && ! -n "$Xmax" && ! -n "$Ymin" && ! -n "$Ymax" ]]
then
	minmax -C ${workingDir}/grid_u.xy > ${workingDir}/minmax
	Xsize_grid_u=`cat ${workingDir}/minmax | cut -f "2"`
	Ysize_grid_u=`cat ${workingDir}/minmax | cut -f "4"`
	Xmin_grid_u=`cat ${workingDir}/minmax | cut -f "5"`
	Xmax_grid_u=`cat ${workingDir}/minmax | cut -f "6"`
	Ymin_grid_u=`cat ${workingDir}/minmax | cut -f "9"`
	Ymax_grid_u=`cat ${workingDir}/minmax | cut -f "10"`
else
	Xsize_grid_u=$Xsize
	Ysize_grid_u=$Ysize
	Xmin_grid_u=$Xmin
	Xmax_grid_u=$Xmax
	Ymin_grid_u=$Ymin
	Ymax_grid_u=$Ymax
fi
envelope_grid_u="-R$Xmin_grid_u/$Xmax_grid_u/$Ymin_grid_u/$Ymax_grid_u"
projection_grid_u=-JX`echo $Xmax_grid_u-$Xmin_grid_u | bc`d/`echo $Ymax_grid_u-$Ymin_grid_u | bc`d

if [[ ! -n "$Xsize" && ! -n "$Ysize" && ! -n "$Xmin" && ! -n "$Xmax" && ! -n "$Ymin" && ! -n "$Ymax" ]]
then
	minmax -C ${workingDir}/grid_v.xy > ${workingDir}/minmax
	Xsize_grid_v=`cat ${workingDir}/minmax | cut -f "2"`
	Ysize_grid_v=`cat ${workingDir}/minmax | cut -f "4"`
	Xmin_grid_v=`cat ${workingDir}/minmax | cut -f "5"`
	Xmax_grid_v=`cat ${workingDir}/minmax | cut -f "6"`
	Ymin_grid_v=`cat ${workingDir}/minmax | cut -f "9"`
	Ymax_grid_v=`cat ${workingDir}/minmax | cut -f "10"`
else
	Xsize_grid_v=$Xsize
	Ysize_grid_v=$Ysize
	Xmin_grid_v=$Xmin
	Xmax_grid_v=$Xmax
	Ymin_grid_v=$Ymin
	Ymax_grid_v=$Ymax
fi
envelope_grid_v="-R$Xmin_grid_v/$Xmax_grid_v/$Ymin_grid_v/$Ymax_grid_v"
projection_grid_v=-JX`echo $Xmax_grid_v-$Xmin_grid_v | bc`d/`echo $Ymax_grid_v-$Ymin_grid_v | bc`d

if [[ ! -n "$Xsize" && ! -n "$Ysize" && ! -n "$Xmin" && ! -n "$Xmax" && ! -n "$Ymin" && ! -n "$Ymax" ]]
then
	minmax -C ${workingDir}/grid_f.xy > ${workingDir}/minmax
	Xsize_grid_f=`cat ${workingDir}/minmax | cut -f "2"`
	Ysize_grid_f=`cat ${workingDir}/minmax | cut -f "4"`
	Xmin_grid_f=`cat ${workingDir}/minmax | cut -f "5"`
	Xmax_grid_f=`cat ${workingDir}/minmax | cut -f "6"`
	Ymin_grid_f=`cat ${workingDir}/minmax | cut -f "9"`
	Ymax_grid_f=`cat ${workingDir}/minmax | cut -f "10"`
else
	Xsize_grid_f=$Xsize
	Ysize_grid_f=$Ysize
	Xmin_grid_f=$Xmin
	Xmax_grid_f=$Xmax
	Ymin_grid_f=$Ymin
	Ymax_grid_f=$Ymax
fi
envelope_grid_f="-R$Xmin_grid_f/$Xmax_grid_f/$Ymin_grid_f/$Ymax_grid_f"
projection_grid_f=-JX`echo $Xmax_grid_f-$Xmin_grid_f | bc`d/`echo $Ymax_grid_f-$Ymin_grid_f | bc`d

