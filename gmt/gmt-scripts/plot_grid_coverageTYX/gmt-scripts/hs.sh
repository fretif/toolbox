#!/bin/bash

if [[ ! -f $infile ]]
then	
	echo "The file $infile doesn't exist"	
else	

	#outfile
	outfile="${outDir}/$currentTime-$var"

	echo "-> Significant wave height..."
	
	# We apply mask if we need	
	if [[ -n "$maskFile" ]] 
	then	
	  grdmath  ${infile}?hs[$tIndex] $maskFile OR = ${workingDir}/plot.grd
	  grdmath  ${infile}?waves_dir[$tIndex] $maskFile OR = ${workingDir}/dir.grd
	else
	  grdsample ${infile}?hs[$tIndex] -G${workingDir}/plot.grd
	  grdsample ${infile}?waves_dir[$tIndex] -G${workingDir}/dir.grd
	fi
	
	# Color palette configuration
	if [[ ! -n "$hsPalFile" ]] 
	then		
		grd2cpt -C${colorPalPath}pasadena.cpt ${workingDir}/plot.grd -Z > ${workingDir}/colorPal.cpt
		hsPalFile="${workingDir}/colorPal.cpt"	
		#cp ${workingDir}/colorPal.cpt hs.cpt		
	fi	  
	
	# Special processing on the direction. We remove somes points.
	grdsample ${workingDir}/dir.grd -G${workingDir}/dir_light.grd -I$[$Xsize*$vectorRatio/100]+/$[$Ysize*$vectorRatio/100]+
	grd2xyz ${workingDir}/dir_light.grd > ${workingDir}/dir

	# Plotting
	grdimage ${workingDir}/plot.grd $envelope $projection -C$hsPalFile -P -K > ${outfile}.ps
	awk '{print $1, $2, $3,'${vectorLength}i'}' ${workingDir}/dir  | psxy $envelope $projection -Sv0.08i+e -Gblack -O -K -P >> ${outfile}.ps

	if [[ -n "$instrumentFile" ]] 
	then
		source $basedir/gmt-scripts/instrument.sh
	fi

	if [[ -n "$typhonFile" ]] 
	then
		source $basedir/gmt-scripts/typhon_track.sh
	fi	
	
	
	psbasemap $envelope $projection $mapAnnotation -P -O -K >> ${outfile}.ps
	
	# Plotting colorbar
 	gmtset MAP_TICK_PEN_PRIMARY thinner,white,solid
 	gmtset MAP_GRID_PEN_PRIMARY thinner,black,solid
 	gmtset MAP_FRAME_PEN thinner,black,solid 	
 	
 	psscale -Dx14c/12.25c+w12c/0.5c+jTC+e -C$hsPalFile -Bx1+g1 -By+lm -S -O -K >> ${outfile}.ps 	
	echo "5 9 20 0 5 BC Significant wave height (m)" > ${workingDir}/legend
	echo "5 8.2 12 0 5 BC ${currentTime:0:`expr index "$currentTime" "_"`-1} ${currentTime: -8:2} h ${currentTime: -5:2}" >> ${workingDir}/legend
 	cat ${workingDir}/legend | pstext -R0/10/0/10 -JX10c -X0 -Y4.5 -O >> ${outfile}.ps
 	
	#psscale -D`echo "($Xmax - $Xmin)*$mapRatioSize + 1" | bc -l`/`echo "(($Ymax - $Ymin)*$mapRatioSize)/2" | bc -l`/`echo "($Ymax - $Ymin)*$mapRatioSize" | bc -l`/`echo "(($Ymax - $Ymin)*$mapRatioSize)/40" | bc -l` -C$hsPalFile -B0.1:"":/:"": -E -O -K >> ${outfile}.ps	
	#echo "5 9 12 0 5 BC Significant wave height (m)" > ${workingDir}/legend
	#echo "5 8.5 8 0 5 BC ${currentTime:0:`expr index "$currentTime" "_"`-1} ${currentTime: -8:2} h ${currentTime: -5:2}" >> ${workingDir}/legend
 	#cat ${workingDir}/legend | pstext -R0/10/0/10 -J -Y`echo "(($Ymax - $Ymin)*$mapRatioSize)/4" | bc -l` -O >> ${outfile}.ps
	
	ps2raster -E$png_resolution -A -Tg -P ${outfile}.ps

	rm -f ${workingDir}/pal.cpt 
	rm -f ${outfile}.ps 
fi
