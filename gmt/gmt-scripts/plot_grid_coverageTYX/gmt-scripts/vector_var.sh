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
		grdsample -I${Xsize}+/${Ysize}+ ${infile}?${VARIABLE_NAME["eastward_$var"]}[$tIndex] -G${workingDir}/u.grd
		grdsample -I${Xsize}+/${Ysize}+ ${infile}?${VARIABLE_NAME["northward_$var"]}[$tIndex] -G${workingDir}/v.grd		
	else
		grdsample $envelope ${infile}?${VARIABLE_NAME["eastward_$var"]}[$tIndex] -G${workingDir}/u.grd
		grdsample $envelope ${infile}?${VARIABLE_NAME["northward_$var"]}[$tIndex] -G${workingDir}/v.grd
	fi
	
	if [[ ! -n "${workingDir}/u.grd" ]] && [[ ! -n "${workingDir}/v.grd" ]]
	then
		echo "Error during cropping"
		exit 0
	fi		
	
	# We apply mask if we need	
	if [[ -n "$maskFile" ]] 
	then	
	  	#Compute new data envelope
		grdinfo -C ${workingDir}/u.grd > ${workingDir}/minmax 
		XminMask=`cat ${workingDir}/minmax | cut -f "2"`
		XmaxMask=`cat ${workingDir}/minmax | cut -f "3"`
		YminMask=`cat ${workingDir}/minmax | cut -f "4"`
		YmaxMask=`cat ${workingDir}/minmax | cut -f "5"`
		XincrMask=`cat ${workingDir}/minmax | cut -f "8"`		
		YincrMask=`cat ${workingDir}/minmax | cut -f "9"`	
		XsizeMask=`cat ${workingDir}/minmax | cut -f "10"`		
		YsizeMask=`cat ${workingDir}/minmax | cut -f "11"`	

		grdsample -R$XminMask/$XmaxMask/$YminMask/$YmaxMask -I${XsizeMask}+/${YsizeMask}+ $maskFile -G${workingDir}/mask.grd
	  	grdmath ${workingDir}/u.grd ${workingDir}/mask.grd OR = ${workingDir}/u.grd
	  	grdmath ${workingDir}/v.grd ${workingDir}/mask.grd OR = ${workingDir}/v.grd
	fi

	# Processing
	grdmath ${workingDir}/u.grd SQR ${workingDir}/v.grd SQR ADD SQRT = ${workingDir}/L2.grd	
	grdmath ${workingDir}/L2.grd $minVector GT = ${workingDir}/mask.grd
	
	grdmath ${workingDir}/L2.grd ${workingDir}/mask.grd MUL = ${workingDir}/plot.grd
	grdmath ${workingDir}/u.grd ${workingDir}/mask.grd MUL = ${workingDir}/current_u.grd
	grdmath ${workingDir}/v.grd ${workingDir}/mask.grd MUL = ${workingDir}/current_v.grd
	
	grdsample ${workingDir}/current_u.grd -G${workingDir}/current_u_light.grd -I$[$Xsize*$vectorRatio/100]+/$[$Ysize*$vectorRatio/100]+
	grdsample ${workingDir}/current_v.grd -G${workingDir}/current_v_light.grd -I$[$Xsize*$vectorRatio/100]+/$[$Ysize*$vectorRatio/100]+

	#
	# Color palette configuration
	#
	if [[ ! -n "${COLOR_PALETTES["$var"]}" ]] 
	then		
		grd2cpt -C${colorPalPath}/pasadena.cpt ${workingDir}/plot.grd -Z > ${workingDir}/colorPal.cpt
		COLOR_PALETTES["$var"]="${workingDir}/colorPal.cpt"	

		if [[ "${saveColorPal}" == "1" ]]; then
		    cp ${workingDir}/colorPal.cpt $var.cpt		
        fi
	fi
		  
	#
	# Plotting
	#
	grdimage ${workingDir}/plot.grd $projection $envelope $tagPPPraster -C${COLOR_PALETTES["$var"]} -K > ${outfile}.ps	
	grdvector ${workingDir}/current_u_light.grd ${workingDir}/current_v_light.grd  -J -R -Gblack -S${vectorLength}i -Q0.08i+e+jc -O -K >> ${outfile}.ps

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

	psscale $envelope $projection -DjBR+w${colorBarXsize}/${colorBarYsize}+o0.5/0.3c+j+e -C${COLOR_PALETTES["$var"]} -Bx${SCALE_TICK["$var"]} -By+l"${CANONICAL_UNITS["$var"]}" -S -O -K >> ${outfile}.ps	
	echo ${LONG_NAME["$var"]} | pstext $envelope $projection -F+f20p,Helvetica+cTC -Y2 -P -O -K >> ${outfile}.ps
	echo ${currentTimeSubTitle} | pstext $envelope $projection -F+f8p,Helvetica+cTC -Y-0.8 -P -O >> ${outfile}.ps
	
	ps2raster -E$png_resolution -A -Tg -P ${outfile}.ps

	rm -f ${workingDir}/pal.cpt 
	rm -f ${workingDir}/*.grd 
	rm -f ${outfile}.ps 
fi

