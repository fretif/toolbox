#!/bin/bash

#infile=med-cruesim/grid.nc
#infile=/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/bathy_maker/GDL-WEST-MED/grid.nc
#infile="/home/retf/work/fieldsites/med-cruesim/modelling/waves/la-tet/outputs/test-one/grid-sympho.nc"
#infile=/home/retf/work/fieldsites/med-cruesim/modelling/hydro/la-tet/grid/grid_no_wetmask.nc
#infile=/home/retf/work/fieldsites/med-cruesim/modelling/hydro/la-tet/grid/grid-smooth.nc
#infile=/home/retf/work/fieldsites/med-cruesim/modelling/hydro/la-tet/grid/grid.nc
infile=/home/retf/test/grid.nc

#1 for classic grid
#2 for circular grid
grid_type=1

grd2xyz $infile?longitude_t > longitude_t
grd2xyz $infile?latitude_t > latitude_t
grd2xyz $infile?h_w > data
grd2xyz $infile?mask_t -Z > mask

join longitude_t latitude_t > grid_t.xy
join grid_t.xy data > temp
paste temp mask > joined.xyz

# grid with index
awk '{ print  $1" "$2" "$3" "$5" "$7" "$8}' joined.xyz > s-grid.xyz
# grid without index
awk '{ print  $3" "$5" "$7" "$8}' joined.xyz > s-lonlat.xyz

if [[ $grid_type == 1 ]] 
then
  # we get the long, lat, and bathy
  head s-grid.xyz
  awk '{ print  $3}' s-grid.xyz > longitude.dat
  awk '{ print  $4}' s-grid.xyz > latitude.dat
  #awk '{  if ($1 == 125 && $2 == 110) { printf("%s\n",0.77) } else print  $5}' s-grid.xyz > bathy.dat
  awk '{ print  $5}' s-grid.xyz > bathy.dat
  
  #awk '{ if($1 < 7) { printf("%s\n",-50)} 
  #else if($2 < 4 || $2 > 208) { printf("%s\n",-50)}  
  #else print $5}' s-grid.xyz > bathy.dat
  
  #TODO improve way to do input boundaries  
  #awk '{ if ($1 == 263 && $6 == 1) { printf("%s\n",2) } 
  #else if($1 < 7) { printf("%s\n",0)} 
  #else if($1 >= 7 && $1 <= 222 && $2 < 4 || $2 > 208) { printf("%s\n",0)} 
  #else if($1 >= 7 && $1 <= 222 && $2 >= 4 && $2 <= 208 && $6 == 0) { printf("%s\n",15)}
  #else print $6}' s-grid.xyz > mask.dat
  
  awk '{ if ($1 == 671 && $6 == 1) { printf("%s\n",2) } else print $6}' s-grid.xyz > mask.dat
  #awk '{ print $6}' s-grid.xyz > mask.dat

  
elif [[ $grid_type == 2 ]] 
then
  # we remove duplicate points
  awk '!a[$0]++' s-lonlat.xyz > s-grid-without-duplicate.xyz

  # we store the duplicate points removed in the previous line
  awk 'a[$0]++' s-lonlat.xyz > duplicate-points-lonlat.xyz

  # we find the index location of the duplicate points
  cat s-grid.xyz | grep -f duplicate-points-lonlat.xyz > duplicate-points-index.xyz
  # we keep only the i=0,1,iglb+1,iglb (the removed point)
  awk '{ if ($1 == 0 || $1 == 1 || $1 == 823 || $1 == 822) { print $0 }}' duplicate-points-index.xyz > duplicate-points.xyz

  cat s-grid.xyz | grep -v -x -f duplicate-points.xyz > s-grid-without-duplicate.xyz  

  # we get the long, lat, and bathy
  awk '{ print  $3}' s-grid-without-duplicate.xyz > longitude.dat
  awk '{ print  $4}' s-grid-without-duplicate.xyz > latitude.dat
  awk '{ print  $5}' s-grid-without-duplicate.xyz > bathy.dat
  
  #TODO improve way to do input boundaries  
  awk '{ if ($2 == 1 && $6 == 1) { printf("%s\n",2) } else print  $6}' s-grid-without-duplicate.xyz > mask.dat
  #awk '{ print  $6}' s-grid-without-duplicate.xyz > mask.dat
fi

rm temp longitude_t latitude_t data joined.xyz s-lonlat.xyz duplicate-points-lonlat.xyz duplicate-points-index.xyz s-grid.xyz


