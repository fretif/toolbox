#!/bin/bash

#################
#	CONFIG File	#
#################

basedir="${0%/*}"
source $basedir/$1

#################################
#	Variable to extract 		#
#################################

#variables=(SP SSHF SLHF T2M D2M SSRD STRD SSR STR TP);
variables=();
times=(03 06 09 12 15 18 21);

#################
#	BEGIN		#
#################

# 1. Set environement

if [[ ! -n "$scanDir" ]] 
then
	path=`pwd`
else
	path=$scanDir
fi

workingDir=`mktemp -d`

# Calculate start time in seconds
parsedStartTime="${startTime:0:4}-${startTime:5:2}-${startTime:8:2} ${startTime:11:2}:${startTime:14:2}:${startTime:17:2}"
startSecondTime=`date --date="$parsedStartTime" "+%s"`

parsedEndTime="${endTime:0:4}-${endTime:5:2}-${endTime:8:2} ${endTime:11:2}:${endTime:14:2}:${endTime:17:2}"
endSecondTime=`date --date="$parsedEndTime" "+%s"`

oldTime=""

# 3. for each file
for infile in ${path}/*.nc; do 

	file=$(basename "$infile")
	filename="${file%.*}"
	
	parsedTime="${filename:18:4}-${filename:22:2}-${filename:24:2}"

	#if [[ $parsedTime != $oldTime ]]
	#then
		currentSecondTime=`date --date="$parsedTime" "+%s"`	
	
		if [[ $currentSecondTime < $startSecondTime || $currentSecondTime > $endSecondTime ]]	
		then		
			# we skip this date
			continue
		fi 

		echo "Current file : $filename"	
	
		if [[ $infile == *gridT* ]]
		then

			if [[ ! -n "$envelope" ]] 
			then
				grdinfo -C $infile > ${workingDir}/minmax		
				Xmin=`cat ${workingDir}/minmax | cut -f "2"`
				Xmax=`cat ${workingDir}/minmax | cut -f "3"`
				Ymin=`cat ${workingDir}/minmax | cut -f "4"`
				Ymax=`cat ${workingDir}/minmax | cut -f "5"`
				Xsize=`cat ${workingDir}/minmax | cut -f "10"`
				Ysize=`cat ${workingDir}/minmax | cut -f "11"`

				envelope="-R$Xmin/$Xmax/$Ymin/$Ymax"				
			fi
	
			#sea surface height
			var="ssh"
			outfile="${parsedTime}_${var}"
			#
			# Color palette configuration
			#
	
				grd2cpt -Csealand ${infile}?sossheig -Z > ${workingDir}/colorPal.cpt
				palFile="${workingDir}/colorPal.cpt"
			
			#
			# Plotting
			#
			grdimage ${infile}?sossheig $envelope -JX10c -C$palFile -P -K > ${outfile}.ps
	
			psbasemap -R -J $mapAnnotation -P -O -K >> ${outfile}.ps
			psscale -D11/5/10/0.3 -C$palFile -B0.2:"":/:"": -E -O -K >> ${outfile}.ps
			echo "5 9.5 12 0 5 BC $parsedTime" | pstext -R0/10/0/10 -J -Y0.8 -O -K >> ${outfile}.ps
			echo "5 9 12 0 5 BC ${var}" | pstext -R -J -Y1.1 -O >> ${outfile}.ps

			ps2raster -E300 -A -Tg -P ${outfile}.ps	

			#surface temperature
			var="surface_temp"
			outfile="${parsedTime}_${var}"
			#
			# Color palette configuration
			#
	
				grd2cpt -Csealand ${infile}?votemper[0] -Z > ${workingDir}/colorPal.cpt
				palFile="${workingDir}/colorPal.cpt"
			
			#
			# Plotting
			#
			grdimage ${infile}?votemper[0] $envelope -JX10c -C$palFile -P -K > ${outfile}.ps
	
			psbasemap -R -J $mapAnnotation -P -O -K >> ${outfile}.ps
			psscale -D11/5/10/0.3 -C$palFile -B5:"":/:"": -E -O -K >> ${outfile}.ps
			echo "5 9.5 12 0 5 BC $parsedTime" | pstext -R0/10/0/10 -J -Y0.8 -O -K >> ${outfile}.ps
			echo "5 9 12 0 5 BC ${var}" | pstext -R -J -Y1.1 -O >> ${outfile}.ps

			ps2raster -E300 -A -Tg -P ${outfile}.ps	

			# surface current velocity = 0.5m
			var="surface_current_velocity"
			outfile="${parsedTime}_${var}"

			#
			# Procceding
			#

			grdmath ${infile/gridT/gridU}?vozocrtx[0,0] SQR ${infile/gridT/gridV}?vomecrty[0,0] SQR ADD SQRT = ${workingDir}/L2.grd
			grdmath ${workingDir}/L2.grd $minVector GT = ${workingDir}/mask.grd
			grdmath ${workingDir}/L2.grd ${workingDir}/mask.grd MUL = ${workingDir}/wind_speed.grd			
			
			#
			# Color palette configuration
			#
	
				grd2cpt -Csealand ${workingDir}/wind_speed.grd -Z > wind_speedPal.cpt
				#makecpt -Csealand -T0/2/0.1 -Z > wind_speedPal.cpt
				palFile="wind_speedPal.cpt"	
				#palFile="/work/thesis/gmt-color-palettes/current.cpt"		
			
			#
			# Plotting
			#
			grdimage ${workingDir}/wind_speed.grd $envelope -JX10c -C$palFile -P -K > ${outfile}.ps

			grdsample ${infile/gridT/gridU}?vozocrtx[0,0] -G${workingDir}/wind_u_light.grd -I$[$Xsize*$vectorRatio/100]+/$[$Ysize*$vectorRatio/100]+
			grdsample ${infile/gridT/gridV}?vomecrty[0,0] -G${workingDir}/wind_v_light.grd -I$[$Xsize*$vectorRatio/100]+/$[$Ysize*$vectorRatio/100]+

			grdvector ${workingDir}/wind_u_light.grd ${workingDir}/wind_v_light.grd -J $envelope -Gblack -W0.5/0/0 -Q0.05i+e+jc -S$vectorLength -O -K >> ${outfile}.ps
			#grdvector  ${infile/gridT/gridU}?vozocrtx[0,0] ${infile/gridT/gridV}?vomecrty[0,0] -J -R -I10 -Gblack -W1/0/0/0 -Q0p/0.1c/0.05c -S20 -O -K >> ${outfile}.ps

	
			psbasemap -R -J $mapAnnotation -P -O -K >> ${outfile}.ps
			psscale -D11/5/10/0.3 -C$palFile -B0.25:"":/:"": -E -O -K >> ${outfile}.ps
			echo "5 9.5 12 0 5 BC $parsedTime" | pstext -R0/10/0/10 -J -Y0.8 -O -K >> ${outfile}.ps
			echo "5 9 12 0 5 BC Surface current" | pstext -R -J -Y1.1 -O -K >> ${outfile}.ps
			echo "5 9 12 0 5 BC m/s" | pstext -R -J -X6.1 -Y-0.6 -O >> ${outfile}.ps

			ps2raster -E300 -A -Tg -P ${outfile}.ps
			

		fi

		oldTime=$parsedTime;

	#fi	

done

rm -f *.bb *.eps *.ps
rm -rf ${workingDir}
