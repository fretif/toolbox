#!/bin/bash

outfile="${path}/bottom-current_${filename}"

echo "-> Bottom current..."

tickmarks1="-Ba1f0.5/a1f0.5" ;

minVector=0
scalestep=0.05
scalemin=0.
scalemax=1.5

scaleZColor=10
scaleZAnnotation=30+gwhite

scale1posX=5;
scale1posY=-2;
Ireso=7;

#
# make cpt
#
makecpt -Csealand -T$minVector/2/0.25 -Z > ${workingDir}/colorPal.cpt

#grd2xyz ${infile}?vel_u[0,$1] > ${workingDir}/vel_u
#grd2xyz ${infile}?vel_v[0,$1] > ${workingDir}/vel_v

grd2xyz ${infile}?velbar_u-velbarobc_u > ${workingDir}/vel_u
grd2xyz ${infile}?velbar_v_velbarobc_v > ${workingDir}/vel_v

join ${workingDir}/grid_u.xy ${workingDir}/vel_u > ${workingDir}/joined.xyz
awk '{ print  $3" "$5" "$7}' ${workingDir}/joined.xyz > ${workingDir}/vel_u.xyz

join ${workingDir}/grid_v.xy ${workingDir}/vel_v > ${workingDir}/joined.xyz
awk '{ print  $3" "$5" "$7}' ${workingDir}/joined.xyz > ${workingDir}/vel_v.xyz

#xyz2grd vel_u.xyz $envelope -I${Xsize}+/${Ysize}+ -Gvel_u.grd
#xyz2grd vel_v.xyz $envelope -I${Xsize}+/${Ysize}+ -Gvel_v.grd
nearneighbor ${workingDir}/vel_u.xyz $envelope -I${Xsize}+/${Ysize}+ -S6k -N4/3 -G${workingDir}/vel_u.grd
nearneighbor ${workingDir}/vel_v.xyz $envelope -I${Xsize}+/${Ysize}+ -S6k -N4/3 -G${workingDir}/vel_v.grd
#greenspline ${workingDir}/vel_u.xyz $envelope -I${Xsize}+/${Ysize}+ -G${workingDir}/vel_u_unmasked.grd
#greenspline ${workingDir}/vel_v.xyz $envelope -I${Xsize}+/${Ysize}+ -G${workingDir}/vel_v_unmasked.grd

grdmath ${workingDir}/vel_u.grd SQR ${workingDir}/vel_v.grd SQR ADD SQRT = ${workingDir}/L2.grd
grdmath ${workingDir}/L2.grd $minVector GT = ${workingDir}/mask.grd
grdmath ${workingDir}/L2.grd ${workingDir}/mask.grd MUL = ${workingDir}/plot.grd
grdmath ${workingDir}/vel_u.grd ${workingDir}/mask.grd MUL = ${workingDir}/current_u.grd
grdmath ${workingDir}/vel_v.grd ${workingDir}/mask.grd MUL = ${workingDir}/current_v.grd

MRmax=`grdinfo -C ${workingDir}/plot.grd | awk '{print $10}'`
NRmax=`grdinfo -C ${workingDir}/plot.grd | awk '{print $11}'`
  
grdimage ${workingDir}/plot.grd $projection $envelope $tagPPPraster -C${workingDir}/colorPal.cpt -X2 -Y10 -K > ${outfile}.ps
#grdcontour bathycote_in.nc -J -C$scaleZColor -A$scaleZAnnotation -L1/100 -Wa0.5p,gray32,solid -Wcfaint,gray32,solid -O -K >> ${outfile}.ps
grdsample ${workingDir}/current_u.grd -G${workingDir}/current_u_light.grd -I$[$MRmax*$Ireso/100]+/$[$NRmax*$Ireso/100]+
grdsample ${workingDir}/current_v.grd -G${workingDir}/current_v_light.grd -I$[$MRmax*$Ireso/100]+/$[$NRmax*$Ireso/100]+
#grdvector ${workingDir}/current_u.grd ${workingDir}/current_v.grd  $projection $envelope -I$[$MRmax/$Ireso]+/$[$MRmax/$Ireso]+ -Sl0.2c -W2/0/0/0 -Q0p/0.1c/0.05c -O -K >> ${outfile}.ps
grdvector ${workingDir}/current_u_light.grd ${workingDir}/current_v_light.grd  $projection $envelope -Sl0.2c -W2/0/0/0 -Q0p/0.1c/0.05c -O -K >> ${outfile}.ps
psbasemap  $projection $envelope -B1g6:"longitude":/1g6:"latitude"::."":WSne -P -O -K >> ${outfile}.ps
psscale -D14.5/6.3/11/0.5 -C${workingDir}/colorPal.cpt -B0.1:"":/:"": -E -O -K >> ${outfile}.ps
echo "121 29 12 0 5 BC $currentTime" | pstext -R -J -Y1 -O -K >> ${outfile}.ps
echo "121 28 18 0 5 BC Bottom current (m/s)" | pstext -R -J -Y1.5 -O >> ${outfile}.ps
ps2raster -E$png_resolution -A -Tg -P ${outfile}.ps

rm -f ${workingDir}/colorPal.cpt
rm -f ${workingDir}/data
rm -f ${workingDir}/joined.xyz
rm -f ${workingDir}/vel_u.xyz 
rm -f ${workingDir}/vel_v.xyz 
rm -f ${workingDir}/*.grd 
rm -f ${outfile}.ps 
