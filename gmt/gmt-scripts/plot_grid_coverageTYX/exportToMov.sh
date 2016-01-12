#!/bin/bash

if [[ ! -n "${workingDir}" ]] 
then
	echo "You execute this script outside the master script. We use the configuration below."
	workingDir="/tmp"
	outDir="/NAS/data/fieldsites/taiwan/modelling/hydro/simulations/regional/KRC-WIND-001/basic-processing/png/saola/total/"
	var="wind-stress"
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




