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
#Old way to use
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
for infile in ${path}/*.dat; do 

	file=$(basename "$infile")
	filename="${file%.*}"	
	
	# Decode time
	currentTime="${filename:4:4}-${filename:8:2}-${filename:10:2} ${filename:13:2}:${filename:15:2}:${filename:17:2}"	
	currentSecondTime=`date -u --date="$currentTime" "+%s"`	
	
	if [[ $currentSecondTime < $startSecondTime || $currentSecondTime > $endSecondTime ]]
	then
		# we skip this date 		   
		continue
	fi  
	
	#
	# Compute envelope 1/2
	#
	gmtinfo -C $infile > ${workingDir}/minmax 

	if [[ ! -n "$Xmin" && ! -n "$Xmax" && ! -n "$Ymin" && ! -n "$Ymax" ]]
	then		
		Xmin=`cat ${workingDir}/minmax | cut -f "1"`
		Xmax=`cat ${workingDir}/minmax | cut -f "2"`
		Ymin=`cat ${workingDir}/minmax | cut -f "3"`
		Ymax=`cat ${workingDir}/minmax | cut -f "4"`
	fi

	envelope="-R$Xmin/$Xmax/$Ymin/$Ymax"	
	projection=-JX`echo "($Xmax - $Xmin)*$mapRatioSize" | bc -l`d/`echo "($Ymax - $Ymin)*$mapRatioSize" | bc -l`d
	
	#
	# Interpolation
	#
	echo "Interpolation in progress..."
	nearneighbor $infile -i0,1,2 $envelope -I${Xincr}/${Yincr} -S${searchRadius} -N${sector} -G${workingDir}/u.grd
	nearneighbor $infile -i0,1,3 $envelope -I${Xincr}/${Yincr} -S${searchRadius} -N${sector} -G${workingDir}/v.grd
	echo "Interpolation done."

	#
	# Compute envelope 2/2
	#
	grdinfo -C ${workingDir}/u.grd > ${workingDir}/minmax 

	Xincr=`cat ${workingDir}/minmax | cut -f "8"`		
	Yincr=`cat ${workingDir}/minmax | cut -f "9"`	
	Xsize=`cat ${workingDir}/minmax | cut -f "10"`		
	Ysize=`cat ${workingDir}/minmax | cut -f "11"`	

	echo "Current file : $filename - $currentTime"	

	var="wnd"
	if test $wnd -eq 1 && [[ "$filename" == *"$var"* ]];
	then				
		source $basedir/gmt-scripts/wnd.sh
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
done

# Plot 2D
if test $bathy -eq 1
then
	source $basedir/gmt-scripts/bathy.sh
fi

#Export to MOV
if test $wnd -eq 1
then
	var="wnd"		

	if test $exportToMov -eq 1
	then
		source $basedir/exportToMov.sh
	fi
fi

if test $taw -eq 1
then
	var="taw"		

	if test $exportToMov -eq 1
	then
		source $basedir/exportToMov.sh
	fi
fi	

if test $two -eq 1
then
	var="two"		

	if test $exportToMov -eq 1
	then
		source $basedir/exportToMov.sh
	fi
fi

rm *.eps
rm -rf ${workingDir}