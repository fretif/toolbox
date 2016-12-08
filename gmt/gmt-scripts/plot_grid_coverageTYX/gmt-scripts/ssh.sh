#!/bin/bash

if [[ ! -f $infile ]]
then	
	echo "The file $infile doesn't exist"	
else	

	#outfile
	outfile="${outDir}/$currentTime-$var"

	echo "-> Sea surface height..."
	
	# We apply mask if we need	
	if [[ -n "$maskFile" ]] 
	then	
	  grdmath  ${infile}?ssh[$tIndex] $maskFile OR = ${workingDir}/plot.grd	 
	else
	  grdsample ${infile}?ssh[$tIndex] -G${workingDir}/plot.grd	 
	fi

	#
	# Color palette configuration
	#
	if [[ ! -n "$sshPalFile" ]] 
	then		
		grd2cpt -C${colorPalPath}pasadena.cpt ${workingDir}/plot.grd -Z > ${workingDir}/colorPal.cpt
		sshPalFile="${workingDir}/colorPal.cpt"	
		#cp ${workingDir}/colorPal.cpt /home/retf/work/fieldsites/med-cruesim/modelling/hydro/gulf-of-lion/outputs/GDL-HYDRO-02/png/ssh.cpt		
	fi
	  
	#
	# Plotting
	#	
	grdimage ${workingDir}/plot.grd	$envelope $projection -C$sshPalFile -P -K > ${outfile}.ps
	
	psxy -i1,0 $envelope $projection /home/retf/work/fieldsites/med-cruesim/observations/bathy/trait_cote_tot.txt -W0.7p -O -K >> ${outfile}.ps

	if [[ -n "$instrumentFile" ]] 
	then
		source ./gmt-scripts/instrument.sh
	fi
	
	psbasemap $envelope $projection $mapAnnotation -P -O -K >> ${outfile}.ps

	#grdcontour ${workingDir}/ssh.grd ${envelope} -J -C5 -Wcthin,black,solid -P -O -K >> ${outfile}.ps
	
	#psscale -D`echo "($Xmax - $Xmin)*$mapRatioSize + 1" | bc -l`/`echo "(($Ymax - $Ymin)*$mapRatioSize)/2" | bc -l`/`echo "($Ymax - $Ymin)*$mapRatioSize" | bc -l`/`echo "(($Ymax - $Ymin)*$mapRatioSize)/40" | bc -l` -C$sshPalFile -B0.1:"":/:"": -E -O -K >> ${outfile}.ps	
	#echo "5 9 12 0 5 BC Sea surface height (m)" > ${workingDir}/legend
	#echo "5 8.5 8 0 5 BC ${currentTime:0:`expr index "$currentTime" "_"`-1} ${currentTime: -8:2} h ${currentTime: -5:2}" >> ${workingDir}/legend
 	#cat ${workingDir}/legend | pstext -R0/10/0/10 -J -Y`echo "(($Ymax - $Ymin)*$mapRatioSize)/4" | bc -l` -O >> ${outfile}.ps
 	
 	#psscale -D0/0/20/0.5 -C$sshPalFile -B0.1:"":/:"": -E -O -K -X23.5 -Y10 >> ${outfile}.ps	
	#echo "5 9 28 0 5 BC Sea surface height (m)" > ${workingDir}/legend
	#echo "5 8.5 16 0 5 BC ${currentTime:0:`expr index "$currentTime" "_"`-1} ${currentTime: -8:2} h ${currentTime: -5:2}" >> ${workingDir}/legend
 	#cat ${workingDir}/legend | pstext -R0/10/0/10 -J -X-26 -Y-11 -O >> ${outfile}.ps
 	 	
 	
 	gmtset MAP_TICK_PEN_PRIMARY thinner,white,solid
 	gmtset MAP_GRID_PEN_PRIMARY thinner,black,solid
 	gmtset MAP_FRAME_PEN thinner,black,solid 	
 	
 	psscale -Dx10c/12.25c+w12c/0.5c+jTC+e -C$sshPalFile -Bx0.1+g0.1 -By+lpsu -S -O -K >> ${outfile}.ps	
	echo "5 9 20 0 5 BC Sea surface height (m)" > ${workingDir}/legend
	echo "5 8 12 0 5 BC ${currentTime:0:`expr index "$currentTime" "_"`-1} ${currentTime: -8:2} h ${currentTime: -5:2}" >> ${workingDir}/legend
 	cat ${workingDir}/legend | pstext -R0/10/0/10 -JX10c -X0 -Y6 -O >> ${outfile}.ps
	
	ps2raster -E$png_resolution -A -Tg -P ${outfile}.ps
	
	#export to SIG
	#makecpt -C${colorPalPath}pasadena.cpt -T0.145/0.20/0.001 -M -Z > ${workingDir}/colorPal.cpt
	#grdmath  ${infile}?ssh[$tIndex] /home/retf/work/fieldsites/med-cruesim/modelling/hydro/la-tet/outputs/TET-FULL-1cm/river_mask.nc OR = ${workingDir}/plot.grd
	#grdimage ${workingDir}/plot.grd $envelope $projection -C$sshPalFile -Q -P -K > ${outfile}_sig.ps
	#echo "3.041623 42.714123" | psxy -J -R -Sc0.15c -Gblack -O -K  >> ${outfile}_sig.ps	
	#echo "3.03505174811 42.7120035783" | psxy -J -R -Sc0.15c -Gblack -O -K  >> ${outfile}_sig.ps	
	#psscale -D12/3/5/0.2 -C$sshPalFile -B0.02:"":/:"m": -E -O >> ${outfile}_sig.ps	
	#ps2raster -Tt -W+g -V ${outfile}_sig.ps

	rm -f ${workingDir}/pal.cpt 
	rm -f ${outfile}.ps ${outfile}_sig.ps temp.grd
fi
