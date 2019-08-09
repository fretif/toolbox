#!/bin/bash	

if [[ ! -f $infile ]]
then	
	echo "The file $infile doesn't exist"	
else	

	#outfile
	outfile="${outDir}/$currentTime-$var"

	echo "-> Wind stress..."

	grdmath ${infile}?u[$tIndex] SQR ${infile}?v[$tIndex] SQR ADD SQRT = ${workingDir}/L2.grd
	grdmath ${workingDir}/L2.grd $minVector GT = ${workingDir}/mask.grd
	grdmath ${workingDir}/L2.grd ${workingDir}/mask.grd MUL = ${workingDir}/plot.grd
	grdmath ${infile}?u[$tIndex] ${workingDir}/mask.grd MUL = ${workingDir}/current_u.grd
	grdmath ${infile}?v[$tIndex] ${workingDir}/mask.grd MUL = ${workingDir}/current_v.grd

	#
	# Color palette configuration
	#
	if [[ ! -n "$windStressPalFile" ]] 
	then		
		grd2cpt -C${colorPalPath}pasadena.cpt ${workingDir}/plot.grd -Z > ${workingDir}/colorPal.cpt
		windStressPalFile="${workingDir}/colorPal.cpt"
		#cp ${workingDir}/colorPal.cpt /home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/outputs/GDL-HYDRO-02/png/wind-stress.cpt		
	fi
	  
	#
	# Plotting
	#
	grdimage ${workingDir}/plot.grd $projection $envelope $tagPPPraster -C$windStressPalFile -K > ${outfile}.ps
	grdsample ${workingDir}/current_u.grd -G${workingDir}/current_u_light.grd -I$[$Xsize*$vectorRatio/100]+/$[$Ysize*$vectorRatio/100]+
	grdsample ${workingDir}/current_v.grd -G${workingDir}/current_v_light.grd -I$[$Xsize*$vectorRatio/100]+/$[$Ysize*$vectorRatio/100]+

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
	#psscale -D`echo "($Xmax - $Xmin)*$mapRatioSize + 1" | bc -l`/`echo "(($Ymax - $Ymin)*$mapRatioSize)/2" | bc -l`/`echo "($Ymax - $Ymin)*$mapRatioSize" | bc -l`/`echo "(($Ymax - $Ymin)*$mapRatioSize)/40" | bc -l` -C$windStressPalFile -B0.2:"":/:"": -E -O -K >> ${outfile}.ps	
	#echo "5 9 12 0 5 BC Wind stress (N/m2)" > ${workingDir}/legend	
	#echo "5 8.5 8 0 5 BC ${currentTime:0:`expr index "$currentTime" "_"`-1} ${currentTime: -8:2} h ${currentTime: -5:2}" >> ${workingDir}/legend
 	#cat ${workingDir}/legend | pstext -R0/10/0/10 -J -Y`echo "(($Ymax - $Ymin)*$mapRatioSize)/4" | bc -l` -O >> ${outfile}.ps
 	
 	psscale -D0/0/20/0.5 -C$windStressPalFile -B0.2:"":/:"": -E -O -K -X23.5 -Y10 >> ${outfile}.ps	
	echo "5 9 28 0 5 BC Wind stress (N/m2)" > ${workingDir}/legend
	echo "5 8.5 16 0 5 BC ${currentTime:0:`expr index "$currentTime" "_"`-1} ${currentTime: -8:2} h ${currentTime: -5:2}" >> ${workingDir}/legend
 	cat ${workingDir}/legend | pstext -R0/10/0/10 -J -X-26 -Y-11 -O >> ${outfile}.ps

	ps2raster -E$png_resolution -A -Tg -P ${outfile}.ps

	rm -f ${workingDir}/pal.cpt 
	rm -f ${workingDir}/*.grd 
	rm -f ${outfile}.ps 
fi

