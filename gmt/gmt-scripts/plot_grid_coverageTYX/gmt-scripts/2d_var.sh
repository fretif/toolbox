#!/bin/bash

if [[ ! -f $infile ]]
then	
	echo "The file $infile doesn't exist"	
else	

	#outfile
	outfile="${outDir}/$currentTimeFilename-${STANDARD_NAME["$var"]}"

	echo "-> ${LONG_NAME["$var"]}..."

	grdsample $envelope ${infile}?${VARIABLE_NAME["$var"]}[$tIndex] -G${workingDir}/data.grd
	
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
	fi

	#
	# Color palette configuration
	#
	if [[ ! -n "${COLOR_PALETTES["$var"]}" ]] 
	then		
		grd2cpt -C${colorPalPath}/pasadena.cpt ${workingDir}/data.grd -Z > ${workingDir}/colorPal.cpt
		COLOR_PALETTES["$var"]="${workingDir}/colorPal.cpt"	

        if [[ "${saveColorPal}" == "1" ]]; then
		    cp ${workingDir}/colorPal.cpt $var.cpt		
        fi
	fi
	  
	#
	# Plotting
	#	
	grdimage ${workingDir}/data.grd $envelope $projection -C${COLOR_PALETTES["$var"]} -P -K > ${outfile}.ps
	#grdcontour ${workingDir}/ssh.grd ${envelope} -J -C5 -Wcthin,black,solid -P -O -K >> ${outfile}.ps

	if [[ -n "$instrumentFile" ]] 
	then
		source ./gmt-scripts/instrument.sh
	fi

	psbasemap $envelope $projection $mapAnnotation -P -O -K >> ${outfile}.ps

	gmtset MAP_TICK_PEN_PRIMARY thinner,white,solid
 	gmtset MAP_GRID_PEN_PRIMARY thinner,black,solid
 	gmtset MAP_FRAME_PEN thinner,black,solid 	

	psscale $colorBarPosition -C${COLOR_PALETTES["$var"]} -Bx${SCALE_TICK["$var"]} -By+l"${CANONICAL_UNITS["$var"]}" -S -O -K >> ${outfile}.ps	
	echo "5 9 20 0 5 BC ${LONG_NAME["$var"]}" > ${workingDir}/legend
	echo "5 8.5 8 0 5 BC ${currentTimeSubTitle}" >> ${workingDir}/legend
 	cat ${workingDir}/legend | pstext -R0/10/0/10 -JX10c $titlePosition -O >> ${outfile}.ps
	
	ps2raster -E$png_resolution -A -Tg -P ${outfile}.ps

	rm -f ${workingDir}/pal.cpt 
	rm -f ${outfile}.ps 
fi
