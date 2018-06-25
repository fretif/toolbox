#!/bin/bash

if [[ ! -f $infile ]]
then	
	echo "The file $infile doesn't exist"	
else	

	#outfile
	outfile="${outDir}/bathy"

	echo "-> Bathymetry..."
	
	# We apply mask if we need	
	if [[ -n "$maskFile" ]] 
	then	
	  grdmath ${infile}?bathy $maskFile OR = ${workingDir}/plot.grd	 
	else
	  grdsample ${infile}?bathy -G${workingDir}/plot.grd	 
	fi

	#
	# Color palette configuration
	#
	if [[ ! -n "$bathyPalFile" ]] 
	then		
		grd2cpt -C${colorPalPath}pasadena.cpt ${workingDir}/plot.grd -L-8/10 -Z > ${workingDir}/colorPal.cpt
		bathyPalFile="${workingDir}/colorPal.cpt"
		#cp ${workingDir}/colorPal.cpt ./bathy.cpt
	fi

  
	#
	# Plotting
	#	
	grdgradient ${workingDir}/plot.grd -R$Xmin/3.046/$Ymin/$Ymax -G${workingDir}/gradient.grd -A0/270 -Ne0.2  
	grdimage ${workingDir}/plot.grd $envelope $projection -C$bathyPalFile -Q -P -K > ${outfile}.ps
	grdimage ${workingDir}/plot.grd $projection ${envelope} -C$bathyPalFile -I${workingDir}/gradient.grd -P -O -K >> ${outfile}.ps
	#grdcontour ${workingDir}/plot.grd ${envelope} -J -C50 -A500+gwhite+f4 -Wcthinnest,black,solid -Wathinner,black,solid -P -O -K >> ${outfile}.ps
	psbasemap ${envelope} $projection $mapAnnotation -P -O -K >> ${outfile}.ps
	
	# Old
	#psscale -D18/5/10/0.3 -C$bathyPalFile -B500:"":/:"": -E -O -K >> ${outfile}.ps
	#echo "5 9.5 12 0 5 BC " | pstext -R0/10/0/10 -J -Y0.8 -O -K >> ${outfile}.ps
	#echo "5 9 12 0 5 BC Bathymetry (m)" | pstext -R -J -Y1.1 -O >> ${outfile}.ps
	
	gmtset MAP_TICK_PEN_PRIMARY thinner,white,solid
 	gmtset MAP_GRID_PEN_PRIMARY thinner,black,solid
 	gmtset MAP_FRAME_PEN thinner,black,solid 	
 	
 	psscale -Dx10c/12.25c+w12c/0.5c+jTC+e -C$bathyPalFile -Bx2+g5 -By+lm -S -O -K >> ${outfile}.ps	
	echo "5 9 20 0 5 BC Bathymetry (m)" > ${workingDir}/legend
	echo "5 8 12 0 5 BC ${currentTime:0:`expr index "$currentTime" "_"`-1} ${currentTime: -8:2} h ${currentTime: -5:2}" >> ${workingDir}/legend
 	cat ${workingDir}/legend | pstext -R0/10/0/10 -JX10c -X0 -Y6 -O >> ${outfile}.ps

	ps2raster -E300 -A -Tg -P ${outfile}.ps
	
	#export to SIG
	#makecpt -C${colorPalPath}pasadena.cpt -T-5/15/0.0001 -Z > ${workingDir}/colorPal.cpt
	#grdmath  ${infile}?ssh[$tIndex] /home/retf/work/fieldsites/med-cruesim/modelling/hydro/la-tet/outputs/TET-FULL-1cm/river_mask.nc OR = ${workingDir}/plot.grd
	grdimage ${workingDir}/plot.grd $envelope $projection -C$bathyPalFile -Q -P -K > ${outfile}_sig.ps
	grdimage ${workingDir}/plot.grd $envelope $projection -C$bathyPalFile -I${workingDir}/gradient.grd -Q -P -O -K >> ${outfile}_sig.ps
	#grdcontour ${workingDir}/plot.grd ${envelope} -J -C50 -A500+gwhite+f4 -Wcthinnest,black,solid -Wathinner,black,solid -P -O -K >> ${outfile}_sig.ps
	#echo "3.041623 42.714123" | psxy -J -R -Sc0.15c -Gblack -O -K  >> ${outfile}_sig.ps	
	#echo "3.03505174811 42.7120035783" | psxy -J -R -Sc0.15c -Gblack -O -K  >> ${outfile}_sig.ps	
	psscale -Dx10c/6c+w4c/0.3c+jTC+e -C$bathyPalFile -Bx2+g5 -By+lm -S -O >> ${outfile}_sig.ps
	ps2raster -E600 -Tt -W+g -V ${outfile}_sig.ps

	rm -f ${workingDir}/pal.cpt 
	rm -f ${outfile}.ps 
fi
