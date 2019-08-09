#!/bin/bash

#infile
current_u=$path"${filename%-*}-bottomCurrent_u.nc"	
current_v=$path"${filename%-*}-bottomCurrent_v.nc"

if [[ ! -f $current_u  || ! -f $current_v ]]
then	
	echo "The file *bottomCurrent_u.nc or *bottomCurrent_v.nc doesn't exist"	
else	

	#outfile
	outfile="${outDir}/${filename%-*}-bottom-current"
	#outfile="${outDir}/${filename:11:2}_${filename:13:2}-bottom-current"

	echo "-> Bottom current..."

	#
	# Processing
	#
	# Apply the mask on the input file
	# !!!!!!!!!!!! Bug dans le masque !
	#grdinfo -C ${current_u} > ${workingDir}/minmax
	#Xsize_lsm=`cat ${workingDir}/minmax | cut -f "10"`
	#Ysize_lsm=`cat ${workingDir}/minmax | cut -f "11"`
	#Xmin_lsm=`cat ${workingDir}/minmax | cut -f "2"`
	#Xmax_lsm=`cat ${workingDir}/minmax | cut -f "3"`
	#Ymin_lsm=`cat ${workingDir}/minmax | cut -f "4"`
	#Ymax_lsm=`cat ${workingDir}/minmax | cut -f "5"`
	#grdlandmask -R$Xmin_lsm/$Xmax_lsm/$Ymin_lsm/$Ymax_lsm -Df -I${Xsize_lsm}+/${Ysize_lsm}+ -N1/NaN -G${workingDir}/land_mask.nc
	#grdmath ${current_u} ${workingDir}/land_mask.nc OR = ${workingDir}/current_u.grd
	#grdmath ${current_v} ${workingDir}/land_mask.nc OR = ${workingDir}/current_v.grd
	#!!!!!!!!!!!!

	grdmath ${current_u} SQR ${current_v} SQR ADD SQRT = ${workingDir}/L2.grd
	grdmath ${workingDir}/L2.grd $minVector GT = ${workingDir}/mask.grd
	grdmath ${workingDir}/L2.grd ${workingDir}/mask.grd MUL = ${workingDir}/plot.grd
	grdmath ${current_u} ${workingDir}/mask.grd MUL = ${workingDir}/current_u.grd
	grdmath ${current_v} ${workingDir}/mask.grd MUL = ${workingDir}/current_v.grd

	#
	# Color palette configuration
	#
	if [[ ! -n "$currentPalFile" ]] 
	then		
		grd2cpt ${workingDir}/plot.grd -Z > ${workingDir}/colorPal.cpt
		currentPalFile="${workingDir}/colorPal.cpt"
	fi
	  
	#
	# Plotting
	#
	grdimage ${workingDir}/plot.grd $projection $envelope $tagPPPraster -C$currentPalFile -X2 -Y10 -K > ${outfile}.ps
	grdsample ${workingDir}/current_u.grd -G${workingDir}/current_u_light.grd -I$[$Xsize*$vectorRatio/100]+/$[$Ysize*$vectorRatio/100]+
	grdsample ${workingDir}/current_v.grd -G${workingDir}/current_v_light.grd -I$[$Xsize*$vectorRatio/100]+/$[$Ysize*$vectorRatio/100]+

	grdvector ${workingDir}/current_u_light.grd ${workingDir}/current_v_light.grd  -J -R -Gblack -S$vectorLength -W1/0/0/0 -Q0p/0.2c/0.03c -O -K >> ${outfile}.ps

echo "121.649500 23.260189" | psxy ${envelope}  $projection -Sc0.1c -Gyellow -W1p,yellow,solid -O -K >> ${outfile}.ps
echo "121.649500 23.260189 12 0 4 LT KR03" | pstext -D0.5/0 -R -J -Gyellow -O -K >> ${outfile}.ps

	psbasemap  -J -R $mapAnnotation -P -O -K >> ${outfile}.ps
	psscale -D18/5/10/0.3 -C$currentPalFile -B0.25:"":/:"": -E -O -K >> ${outfile}.ps
	echo "5 9.5 12 0 5 BC $currentTime" | pstext -R0/10/0/10 -J -Y1.7 -O -K >> ${outfile}.ps
#	echo "5 9.5 12 0 5 BC 00:${filename:11:2}:${filename:13:2}" | pstext -R0/10/0/10 -J -Y1.2 -O -K >> ${outfile}.ps
	echo "5 9 12 0 5 BC Bottom current (m/s)" | pstext -R -J -Y1.2 -O >> ${outfile}.ps

	ps2raster -E$png_resolution -A -Tg -P ${outfile}.ps

	rm -f ${workingDir}/colorPal.cpt
	rm -f ${workingDir}/data
	rm -f ${workingDir}/joined.xyz
	rm -f ${workingDir}/vel_u.xyz 
	rm -f ${workingDir}/vel_v.xyz 
	rm -f ${workingDir}/*.grd 
	rm -f ${outfile}.ps 
fi
