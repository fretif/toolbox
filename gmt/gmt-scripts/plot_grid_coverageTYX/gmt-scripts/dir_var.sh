#!/bin/bash

if [[ ! -f $infile ]]
then	
	echo "The file $infile doesn't exist"	
else	

	#outfile
	outfile="${outDir}/$currentTimeFilename-${STANDARD_NAME["$var"]}"

	echo "-> ${LONG_NAME["$var"]}..."
	
	# Cropping	
	if [[ "$crop" == "0" ]]
	then 
		grdsample -I${Xsize}+/${Ysize}+ ${infile}?${VARIABLE_NAME["$var"]}[$tIndex] -G${workingDir}/data.grd
		grdsample -I${Xsize}+/${Ysize}+ ${infile}?${VARIABLE_NAME["dir_$var"]}[$tIndex] -G${workingDir}/dir.grd
	else
		grdsample $envelope ${infile}?${VARIABLE_NAME["$var"]}[$tIndex] -G${workingDir}/data.grd
		grdsample $envelope ${infile}?${VARIABLE_NAME["dir_$var"]}[$tIndex] -G${workingDir}/dir.grd
	fi
	
	if [[ ! -n "${workingDir}/data.grd" ]] 
	then
		echo "Error during cropping"
		exit 0
	fi	
	
	# We apply mask if we need	
	if [[ -n "$maskFile" ]] 
	then		  
		#Compute new data envelope
		grdinfo -C ${workingDir}/data.grd > ${workingDir}/minmax 
		XminMask=`cat ${workingDir}/minmax | cut -f "2"`
		XmaxMask=`cat ${workingDir}/minmax | cut -f "3"`
		YminMask=`cat ${workingDir}/minmax | cut -f "4"`
		YmaxMask=`cat ${workingDir}/minmax | cut -f "5"`
		XincrMask=`cat ${workingDir}/minmax | cut -f "8"`		
		YincrMask=`cat ${workingDir}/minmax | cut -f "9"`	
		XsizeMask=`cat ${workingDir}/minmax | cut -f "10"`		
		YsizeMask=`cat ${workingDir}/minmax | cut -f "11"`	

		grdsample -R$XminMask/$XmaxMask/$YminMask/$YmaxMask -I${XsizeMask}+/${YsizeMask}+ $maskFile -G${workingDir}/mask.grd
	  	grdmath ${workingDir}/data.grd ${workingDir}/mask.grd OR = ${workingDir}/data.grd
	  	grdmath ${workingDir}/dir.grd ${workingDir}/mask.grd OR = ${workingDir}/dir.grd
	fi

	# Processing
	grdmath ${workingDir}/data.grd $minVector GT = ${workingDir}/mask.grd	
	grdmath ${workingDir}/data.grd ${workingDir}/mask.grd MUL = ${workingDir}/data.grd
	grdmath ${workingDir}/dir.grd ${workingDir}/mask.grd MUL = ${workingDir}/dir.grd
	
	grdsample ${workingDir}/dir.grd -G${workingDir}/dir_light.grd -I$[$Xsize*$vectorRatio/100]+/$[$Ysize*$vectorRatio/100]+

	#
	# Color palette configuration
	#
	if [[ ! -n "${COLOR_PALETTES["$var"]}" ]] 
	then		
		grd2cpt -C${colorPalPath}/pasadena.cpt ${workingDir}/data.grd -Z > ${workingDir}/colorPal.cpt
		COLOR_PALETTES["$var"]="${workingDir}/colorPal.cpt"	
		#cp ${workingDir}/colorPal.cpt ./regional/meteo-temp.cpt		
	fi
	  
	#
	# Plotting
	#	
	grdimage ${workingDir}/data.grd $envelope $projection -C${COLOR_PALETTES["$var"]} -P -K > ${outfile}.ps
	grd2xyz ${workingDir}/dir_light.grd | awk '{printf("%s %s\n",$0,'$(echo $vectorLength + 0.3 | bc -l)'i)}' | psxy $envelope $projection -Sv0.09i+e+jc -Gblack -P -O -K >> ${outfile}.ps
	#grdcontour ${workingDir}/ssh.grd ${envelope} -J -C5 -Wcthin,black,solid -P -O -K >> ${outfile}.ps

	if [[ -n "$instrumentFile" ]] 
	then
		source ./gmt-scripts/instrument.sh
	fi

	psbasemap $envelope $projection $mapAnnotation -P -O -K >> ${outfile}.ps

	gmtset MAP_TICK_PEN_PRIMARY thinner,white,solid
 	gmtset MAP_GRID_PEN_PRIMARY thinner,black,solid
 	gmtset MAP_FRAME_PEN thinner,black,solid 	

	psscale $envelope $projection -DjBR+w${colorBarXsize}/${colorBarYsize}+o0.5/0.3c+j+e -C${COLOR_PALETTES["$var"]} -Bx${SCALE_TICK["$var"]} -By+l"${CANONICAL_UNITS["$var"]}" -S -O -K >> ${outfile}.ps	
	echo ${LONG_NAME["$var"]} | pstext $envelope $projection -F+f20p,Helvetica+cTC -Y2 -P -O -K >> ${outfile}.ps
	echo ${currentTimeSubTitle} | pstext $envelope $projection -F+f8p,Helvetica+cTC -Y-0.8 -P -O >> ${outfile}.ps
	
	psconvert -A -Tg -P ${outfile}.ps

	rm -f ${workingDir}/pal.cpt 
	rm -f ${outfile}.ps 
fi
