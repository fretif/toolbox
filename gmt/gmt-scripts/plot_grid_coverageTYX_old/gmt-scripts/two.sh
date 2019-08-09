#!/bin/bash	

if [[ ! -f $infile ]]
then	
	echo "The file $infile doesn't exist"	
else	

	#outfile
	outfile="${outDir}/$currentTime-$var"	
	echo "-> TWO..."
	
	# We apply mask if we need	
	if [[ -n "$maskFile" ]] 
	then	
	  grdmath  ${infile}?utwo[$tIndex] $maskFile OR = ${workingDir}/u.grd
	  grdmath  ${infile}?vtwo[$tIndex] $maskFile OR = ${workingDir}/v.grd
	else
	  grdsample ${infile}?utwo[$tIndex] -G${workingDir}/u.grd
	  grdsample ${infile}?vtwo[$tIndex] -G${workingDir}/v.grd
	fi
	
	# Processing
	grdmath ${workingDir}/u.grd SQR ${workingDir}/v.grd SQR ADD SQRT = ${workingDir}/plot.grd	
	grdsample ${workingDir}/u.grd -G${workingDir}/current_u_light.grd -I$[$Xsize*$vectorRatio/100]+/$[$Ysize*$vectorRatio/100]+
	grdsample ${workingDir}/v.grd -G${workingDir}/current_v_light.grd -I$[$Xsize*$vectorRatio/100]+/$[$Ysize*$vectorRatio/100]+
	#
	# Color palette configuration
	#
	if [[ ! -n "$twoPalFile" ]] 
	then		
		grd2cpt -C${colorPalPath}pasadena.cpt ${workingDir}/plot.grd -Z > ${workingDir}/colorPal.cpt
		twoPalFile="${workingDir}/colorPal.cpt"
		#cp ${workingDir}/colorPal.cpt ./two.cpt		
	fi
	  
	# Plotting
	grdimage ${workingDir}/plot.grd $projection $envelope $tagPPPraster -C$twoPalFile -K > ${outfile}.ps
	grdvector ${workingDir}/current_u_light.grd ${workingDir}/current_v_light.grd  -J -R -Gblack -S${vectorLength}i -Q0.08i+e -O -K >> ${outfile}.ps

	if [[ -n "$typhonFile" ]] 
	then
		source ./gmt-scripts/typhon_track.sh
	fi

	if [[ -n "$instrumentFile" ]] 
	then
		source ./gmt-scripts/instrument.sh
	fi
	
	psbasemap $envelope $projection $mapAnnotation -P -O -K >> ${outfile}.ps
	
	# Plotting colorbar	
	gmtset MAP_TICK_PEN_PRIMARY thinner,white,solid
 	gmtset MAP_GRID_PEN_PRIMARY thinner,black,solid
 	gmtset MAP_FRAME_PEN thinner,black,solid 	
 	
 	#psscale -Dx14c/12.25c+w12c/0.5c+jTC+e -C$twoPalFile -Bx0.002+g0.002 -By+lN/m2 -S -O -K >> ${outfile}.ps	
 	psscale -Dx19.5c/7.25c+w6c/0.5c+jTC+e -C$twoPalFile -Bx0.002+g0.002 -By+lN/m2 -S -O -K >> ${outfile}.ps
 	#psscale -Dx19.5c/7.25c+w6c/0.5c+jTC+e -C$twoPalFile -Bx0.0002+g0.0002 -By+lN/m2 -S -O -K >> ${outfile}.ps
	echo "5 9 20 0 5 BC TWO (N/m2)" > ${workingDir}/legend
	echo "5 8.2 12 0 5 BC ${currentTime:0:`expr index "$currentTime" "_"`-1} ${currentTime: -8:2} h ${currentTime: -5:2}" >> ${workingDir}/legend
 	#cat ${workingDir}/legend | pstext -R0/10/0/10 -JX10c -X0 -Y4.5 -O >> ${outfile}.ps
 	cat ${workingDir}/legend | pstext -R0/10/0/10 -JX10c -X4 -Y1 -O >> ${outfile}.ps
 	
	#psscale -D`echo "($Xmax - $Xmin)*$mapRatioSize + 1" | bc -l`/`echo "(($Ymax - $Ymin)*$mapRatioSize)/2" | bc -l`/`echo "($Ymax - $Ymin)*$mapRatioSize" | bc -l`/`echo "(($Ymax - $Ymin)*$mapRatioSize)/40" | bc -l` -C$tawPalFile -B0.0002:"":/:"": -E -O -K >> ${outfile}.ps	
	#echo "5 9 12 0 5 BC TAW (N/m2)" > ${workingDir}/legend	
	#echo "5 8.5 8 0 5 BC ${currentTime:0:`expr index "$currentTime" "_"`-1} ${currentTime: -8:2} h ${currentTime: -5:2}" >> ${workingDir}/legend
 	#cat ${workingDir}/legend | pstext -R0/10/0/10 -J -Y`echo "(($Ymax - $Ymin)*$mapRatioSize)/4" | bc -l` -O >> ${outfile}.ps

	ps2raster -E$png_resolution -A -Tg -P ${outfile}.ps

	rm -f ${workingDir}/pal.cpt 
	rm -f ${workingDir}/*.grd 
	rm -f ${outfile}.ps 
fi

