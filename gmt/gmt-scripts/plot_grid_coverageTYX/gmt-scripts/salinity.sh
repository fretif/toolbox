#!/bin/bash

if [[ ! -f $infile ]]
then	
	echo "The file $infile doesn't exist"	
else	

	#outfile
	outfile="${outDir}/$currentTime-$var"

	echo "-> Salinity..."

	#
	# Color palette configuration
	#
	if [[ ! -n "$salPalFile" ]] 
	then		
		grd2cpt -C${colorPalPath}pasadena.cpt ${infile}?salinity[$tIndex] -Z > ${workingDir}/colorPal.cpt
		salPalFile="${workingDir}/colorPal.cpt"	
		#cp ${workingDir}/colorPal.cpt /home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/processing/mars-2013/map/sal.cpt		
	fi
	  
	#
	# Plotting
	#	
	grdimage ${infile}?salinity[$tIndex] $envelope $projection -C$salPalFile -P -K > ${outfile}.ps

	if [[ -n "$instrumentFile" ]] 
	then
		source ./gmt-scripts/instrument.sh
	fi

	#grdcontour ${workingDir}/ssh.grd ${envelope} -J -C5 -Wcthin,black,solid -P -O -K >> ${outfile}.ps
	psbasemap $envelope $projection $mapAnnotation -P -O -K >> ${outfile}.ps
	
	#psscale -D`echo "($Xmax - $Xmin)*$mapRatioSize + 1" | bc -l`/`echo "(($Ymax - $Ymin)*$mapRatioSize)/2" | bc -l`/`echo "($Ymax - $Ymin)*$mapRatioSize" | bc -l`/`echo "(($Ymax - $Ymin)*$mapRatioSize)/40" | bc -l` -C$salPalFile -B0.5:"":/:"": -E -O -K >> ${outfile}.ps	
	#echo "5 9 12 0 5 BC Salinity (psu)" > ${workingDir}/legend
	#echo "5 8.5 8 0 5 BC ${currentTime:0:`expr index "$currentTime" "_"`-1} ${currentTime: -8:2} h ${currentTime: -5:2}" >> ${workingDir}/legend
 	#cat ${workingDir}/legend | pstext -R0/10/0/10 -J -Y`echo "(($Ymax - $Ymin)*$mapRatioSize)/4" | bc -l` -O >> ${outfile}.ps
 	
 	psxy -i1,0 $envelope $projection /home/retf/work/fieldsites/med-cruesim/observations/bathy/trait_cote_tot.txt -W0.7p -O -K >> ${outfile}.ps 
 	
 	gmtset MAP_TICK_PEN_PRIMARY thinner,white,solid
 	gmtset MAP_GRID_PEN_PRIMARY thinner,black,solid
 	gmtset MAP_FRAME_PEN thinner,black,solid 	
 	
 	psscale -Dx10c/12.25c+w12c/0.5c+jTC+e -C$salPalFile -Bx5+g5 -By+lpsu -S -O -K >> ${outfile}.ps	
	echo "5 9 20 0 5 BC Sea surface salinity (psu)" > ${workingDir}/legend
	echo "5 8 12 0 5 BC ${currentTime:0:`expr index "$currentTime" "_"`-1} ${currentTime: -8:2} h ${currentTime: -5:2}" >> ${workingDir}/legend
 	cat ${workingDir}/legend | pstext -R0/10/0/10 -JX10c -X0 -Y6 -O >> ${outfile}.ps
	
	ps2raster -E$png_resolution -A -Tg -P ${outfile}.ps

	rm -f ${workingDir}/pal.cpt 
	rm -f ${outfile}.ps 
fi

