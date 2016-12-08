#!/bin/bash

if [[ ! -n "${workingDir}" ]] 
then
	echo "You execute this script outside the master script. We use the configuration below."
	workingDir="/tmp"
	outDir="/home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/processing/mars-2013/map/png/"
	var="surface-salinity"
	echo "Output dir = $outDir"
	echo "Variable = $var"
fi

x=1
for i in ${outDir}*${var}.png; 
do 
	counter=$(printf %04d $x); 
	convert "$i" -resize 1920x1080! ${workingDir}/img"$counter".png
	x=$(($x+1));
done

ffmpeg -f image2 -r 10 -i "${workingDir}/img%04d.png" -y ${outDir}/${var}.mp4

rm -f ${workingDir}/img*




