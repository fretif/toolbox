#!/bin/bash

#########################
#	Better looklike		#
#########################
#gmtset COLOR_BACKGROUND  220/220/220
#gmtset COLOR_FOREGROUND 50/50/20
#gmtset COLOR_NAN 255/255/255
gmtset MAP_FRAME_TYPE fancy
gmtset MAP_FRAME_WIDTH 0.1c
gmtset MAP_FRAME_PEN 0.05c
gmtset MAP_TICK_PEN_PRIMARY 0.01c
gmtset MAP_ANNOT_OFFSET_PRIMARY 0.05c
gmtset MAP_LABEL_OFFSET 0.25c
gmtset MAP_ANNOT_OBLIQUE 32
gmtset MAP_ANNOT_MIN_SPACING 1c
gmtset MAP_GRID_CROSS_SIZE_PRIMARY 0
gmtset MAP_GRID_PEN_PRIMARY 0.015c,0/0/0,.
gmtset MAP_GRID_PEN_SECONDARY 0.015c,0/0/0
gmtset PS_LINE_JOIN miter
gmtset PS_LINE_CAP butt
gmtset PS_MITER_LIMIT 180
LANG=en_us_8859_1

# 1. Import config file

basedir="${0%/*}"
# Old way to use
#source $basedir/$1
source $1

# 2. Set environement

if [[ ! -n "$scanDir" ]] 
then
	path=`pwd`
else
	path=$scanDir
fi

#outDir
if [[ ! -n "$outDir" ]] 
then
	echo "Please define 'outDir' variable. Abort"
	exit
else
	mkdir -p $outDir
fi

workingDir=`mktemp -d`

# Calculate start time in seconds
parsedStartTime="${startTime:0:4}-${startTime:5:2}-${startTime:8:2} ${startTime:11:2}:${startTime:14:2}:${startTime:17:2}"
startSecondTime=`date -u --date="$parsedStartTime" "+%s"`

# Calculate end time in seconds
parsedEndTime="${endTime:0:4}-${endTime:5:2}-${endTime:8:2} ${endTime:11:2}:${endTime:14:2}:${endTime:17:2}"
endSecondTime=`date -u --date="$parsedEndTime" "+%s"`

# 3. Scan file directory
for infile in ${path}/*.nc; do 

	file=$(basename "$infile")
	filename="${file%.*}"

	#Compute envelope

	#Select variable according to the name
	if [[ "$filename" == *"sea-surface-height"* ]] || [[ "$filename" == *"inverse-barometer"* ]] || [[ "$filename" == *"hs-wave"* ]];
	then		
		grdinfo -C $infile?z > ${workingDir}/minmax 
	else
		grdinfo -C $infile?u > ${workingDir}/minmax 
	fi

	if [[ ! -n "$Xmin" && ! -n "$Xmax" && ! -n "$Ymin" && ! -n "$Ymax" ]]
	then		
		Xmin=`cat ${workingDir}/minmax | cut -f "2"`
		Xmax=`cat ${workingDir}/minmax | cut -f "3"`
		Ymin=`cat ${workingDir}/minmax | cut -f "4"`
		Ymax=`cat ${workingDir}/minmax | cut -f "5"`
	fi		
		
	Xincr=`cat ${workingDir}/minmax | cut -f "8"`		
	Yincr=`cat ${workingDir}/minmax | cut -f "9"`	
	Xsize=`cat ${workingDir}/minmax | cut -f "10"`		
	Ysize=`cat ${workingDir}/minmax | cut -f "11"`	

	envelope="-R$Xmin/$Xmax/$Ymin/$Ymax"	
	projection=-JX`echo "($Xmax - $Xmin)*$mapRatioSize" | bc -l`d/`echo "($Ymax - $Ymin)*$mapRatioSize" | bc -l`d

	#For each time
	tIndex=0
	gmtconvert $infile?time | while read currentSecondTime
	do
		currentTime=`date -u --date="@$currentSecondTime" "+%d-%B-%Y_%H-%M-%S"`

		if test $currentSecondTime -ge $startSecondTime && test $currentSecondTime -le $endSecondTime
		then

			echo "Current file : $filename - $currentTime"	
	
			var="sea-surface-height"
			if test $ssh -eq 1 && [[ "$filename" == *"$var"* ]];
			then				
				source $basedir/gmt-scripts/ssh.sh
			fi
	
			var="barotropic-current"	
			if test $barotropicCurrent -eq 1 && [[ "$filename" == *"$var"* ]];
			then
						
				source $basedir/gmt-scripts/barotropicCurrent.sh
			fi
			
			var="surface-current"			
			if test $surfaceCurrent -eq 1 && [[ "$filename" == *"$var"* ]];
			then									
				source $basedir/gmt-scripts/surfaceCurrent.sh
			fi
	
			var="surface-temperature"	
			if test $surfaceTemperature -eq 1 && [[ "$filename" == *"$var"* ]];
			then	
				
				source $basedir/gmt-scripts/temperature.sh
			fi
	
			var="surface-salinity"	
			if test $surfaceSalinity -eq 1 && [[ "$filename" == *"$var"* ]];
			then					
				source $basedir/gmt-scripts/salinity.sh
			fi
	
			var="middle-current"	
			if test $middleCurrent -eq 1 && [[ "$filename" == *"$var"* ]];
			then				
				source $basedir/gmt-scripts/middleCurrent.sh
			fi

			var="bottom-current"	
			if test $bottomCurrent -eq 1 && [[ "$filename" == *"$var"* ]];
			then				
				source $basedir/gmt-scripts/bottomCurrent.sh
			fi

			var="wind-stress"	
			if test $windStress -eq 1 && [[ "$filename" == *"$var"* ]];
			then				
				source $basedir/gmt-scripts/windStress.sh
			fi

			var="inverse-barometer"	
			if test $ib -eq 1 && [[ "$filename" == *"$var"* ]];
			then				
				source $basedir/gmt-scripts/ib.sh
			fi

			var="hs-wave"	
			if test $hs -eq 1 && [[ "$filename" == *"$var"* ]];
			then					
				source $basedir/gmt-scripts/hs.sh
			fi
			
			var="two"	
			if test $two -eq 1 && [[ "$filename" == *"$var"* ]];
			then					
				source $basedir/gmt-scripts/two.sh
			fi
			
			var="taw"	
			if test $taw -eq 1 && [[ "$filename" == *"$var"* ]];
			then					
				source $basedir/gmt-scripts/taw.sh
			fi
			
			var="tsub"	
			if test $twoSubTaw -eq 1 && [[ "$filename" == *"$var"* ]];
			then					
				source $basedir/gmt-scripts/two-taw.sh
			fi
		fi

		((tIndex ++))

	done	

done

# Plot 2D
if test $bathy -eq 1
then
	source $basedir/gmt-scripts/bathy.sh
fi

if test $meshSize -eq 1
then
	source $basedir/gmt-scripts/meshSize.sh
fi

#Export to MOV
if test $ssh -eq 1
then
	var="sea-surface-height"		

	if test $exportToMov -eq 1
	then
		source $basedir/exportToMov.sh
	fi
fi

if test $barotropicCurrent -eq 1
then
	var="barotropic-current"		

	if test $exportToMov -eq 1
	then
		source $basedir/exportToMov.sh
	fi
fi	

if test $surfaceCurrent -eq 1
then
	var="surface-current"		

	if test $exportToMov -eq 1
	then
		source $basedir/exportToMov.sh
	fi
fi

if test $surfaceTemperature -eq 1
then
	var="surface-temperature"		

	if test $exportToMov -eq 1
	then
		source $basedir/exportToMov.sh
	fi
fi

if test $surfaceSalinity -eq 1
then
	var="surface-salinity"
	source $basedir/gmt-scripts/salinity.sh

	if test $exportToMov -eq 1
	then
		source $basedir/exportToMov.sh
	fi
fi

if test $middleCurrent -eq 1
then
	var="middle-current"		

	if test $exportToMov -eq 1
	then
		source $basedir/exportToMov.sh
	fi
fi

if test $bottomCurrent -eq 1
then
	var="bottom-current"		

	if test $exportToMov -eq 1
	then
		source $basedir/exportToMov.sh
	fi
fi

if test $windStress -eq 1
then
	var="wind-stress"		

	if test $exportToMov -eq 1
	then
		source $basedir/exportToMov.sh
	fi
fi

if test $ib -eq 1
then
	var="inverse-barometer"		

	if test $exportToMov -eq 1
	then
		source $basedir/exportToMov.sh
	fi
fi

rm *.eps
rm -rf ${workingDir}
