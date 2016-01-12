#!/bin/bash

#infile
infile=$path"sqrt_dxdy.grd"

if [[ ! -f $infile ]]
then	
	echo "The file $infile doesn't exist"	
else	

	#outfile
	outfile="${outDir}/meshSize"

	echo "-> Mesh size..."

	#
	# Color palette configuration
	#			
	grd2cpt -Csealand ${infile} > ${workingDir}/colorPal.cpt
	palFile="${workingDir}/colorPal.cpt"
	

	#
	# Processing
	#
	# Apply the mask on the input file
	#grdinfo -C ${infile} > ${workingDir}/minmax
	#Xsize_lsm=`cat ${workingDir}/minmax | cut -f "10"`
	#Ysize_lsm=`cat ${workingDir}/minmax | cut -f "11"`
	#Xmin_lsm=`cat ${workingDir}/minmax | cut -f "2"`
	#Xmax_lsm=`cat ${workingDir}/minmax | cut -f "3"`
	#Ymin_lsm=`cat ${workingDir}/minmax | cut -f "4"`
	#Ymax_lsm=`cat ${workingDir}/minmax | cut -f "5"`
	#grdlandmask -R$Xmin_lsm/$Xmax_lsm/$Ymin_lsm/$Ymax_lsm -Df -I${Xsize_lsm}+/${Ysize_lsm}+ -N1/NaN -G${workingDir}/land_mask.nc
	#grdmath ${infile} ${workingDir}/land_mask.nc OR = ${workingDir}/bathy.grd
	  
	#
	# Plotting
	#

	#grdgradient ${infile} -G${workingDir}/gradient.grd -A45 -Nt0.7 
	grdimage ${infile} $projection ${envelope} -C$palFile -P -K > ${outfile}.ps
	#grdcontour ${infile} ${envelope} -J -C50 -A500+gwhite+f4 -Wcthinnest,black,solid -Wathinner,black,solid -P -O -K >> ${outfile}.ps
	psbasemap ${envelope} $projection $mapAnnotation -P -O -K >> ${outfile}.ps
	psscale -D18/5/10/0.3 -C$palFile -B100:"":/:"": -E -O -K >> ${outfile}.ps
	echo "5 9.5 12 0 5 BC " | pstext -R0/10/0/10 -J -Y0.8 -O -K >> ${outfile}.ps
	echo "5 9 12 0 5 BC Mesh size (m)" | pstext -R -J -Y1.1 -O >> ${outfile}.ps

	ps2raster -E$png_resolution -A -Tg -P ${outfile}.ps

	rm -f ${workingDir}/pal.cpt 
	rm -f ${outfile}.ps 
fi
