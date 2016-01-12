#!/bin/bash

if [[ ! -f $infile ]]
then	
	echo "The file $infile doesn't exist"	
else	

	#outfile
	outfile="${outDir}/$currentTime-$var"

	echo "-> Significant wave height..."

	#
	# Color palette configuration
	#
	if [[ ! -n "$hsPalFile" ]] 
	then		
		grd2cpt -C${colorPalPath}pasadena.cpt ${infile}?z[$tIndex] -Z > ${workingDir}/colorPal.cpt
		hsPalFile="${workingDir}/colorPal.cpt"	
		#cp ${workingDir}/colorPal.cpt ./regional/meteo-ib.cpt		
	fi	  
	
	#
	# Plotting
	#	
	grdimage ${infile}?z[$tIndex] $envelope $projection -C$hsPalFile -P -K > ${outfile}.ps

	if [[ -n "$instrumentFile" ]] 
	then
		source ./gmt-scripts/instrument.sh
	fi

	if [[ -n "$typhonFile" ]] 
	then
		source ./gmt-scripts/typhon_track.sh
	fi

	#grdcontour ${workingDir}/ssh.grd ${envelope} -J -C5 -Wcthin,black,solid -P -O -K >> ${outfile}.ps
	psbasemap $envelope $projection $mapAnnotation -P -O -K >> ${outfile}.ps
	psscale -D`echo "($Xmax - $Xmin)*$mapRatioSize + 1" | bc -l`/`echo "(($Ymax - $Ymin)*$mapRatioSize)/2" | bc -l`/`echo "($Ymax - $Ymin)*$mapRatioSize" | bc -l`/`echo "(($Ymax - $Ymin)*$mapRatioSize)/40" | bc -l` -C$hsPalFile -B1:"":/:"": -E -O >> ${outfile}.ps	
	#echo "5 9 12 0 5 BC Significant wave height (m)" > ${workingDir}/legend
	#echo "5 8.5 8 0 5 BC ${currentTime:0:`expr index "$currentTime" "_"`-1} ${currentTime: -8:2} h ${currentTime: -5:2}" >> ${workingDir}/legend
 	#cat ${workingDir}/legend | pstext -R0/10/0/10 -J -Y`echo "(($Ymax - $Ymin)*$mapRatioSize)/4" | bc -l` -O >> ${outfile}.ps
	
	ps2raster -E$png_resolution -A -Tg -P ${outfile}.ps

	rm -f ${workingDir}/pal.cpt 
	rm -f ${outfile}.ps 
fi
