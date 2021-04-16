#!/bin/bash

#########################
#	Better looklike		#
#########################
function set_default_style {
  gmtset COLOR_BACKGROUND  255/255/255
  gmtset COLOR_FOREGROUND 255/255/255
  gmtset COLOR_NAN 255/255/255
  gmtset MAP_FRAME_TYPE fancy
  gmtset MAP_FRAME_WIDTH 0.1c
  gmtset MAP_FRAME_PEN 0.05c
  gmtset MAP_TICK_PEN_PRIMARY 0.01c
  gmtset MAP_ANNOT_OFFSET_PRIMARY 0.05c
  gmtset FONT_ANNOT_PRIMARY 8p,Helvetica,black
  gmtset FONT_LABEL 8p,Helvetica,black
  gmtset FONT_TITLE 13p,Helvetica,black
  gmtset MAP_LABEL_OFFSET 0.25c
  gmtset MAP_ANNOT_OBLIQUE 32
  gmtset MAP_ANNOT_MIN_SPACING 2c
  gmtset MAP_GRID_PEN_PRIMARY 0.015c,black,. # dotted-line
  gmtset PS_LINE_JOIN miter
  gmtset PS_LINE_CAP butt
  gmtset PS_MITER_LIMIT 180
}

LANG=en_us_8859_1
set_default_style

# 1. Import config file

basedir="${0%/*}"
source $basedir/gmt-scripts/variablesDefinition.sh
source $1

# 2. Set environement

if [[ ! -n "$infile" ]] 
then
	echo "Please define 'infile' variable. Abort"
	exit
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

file=$(basename "$infile")
filename="${file%.*}"

#Check variables
for var in "${variables[@]}"; do
	
	if [[ -n "${VARIABLE_NAME["$var"]}" ]]
	then 
		ncdump -h $infile > ${workingDir}/check_variable	        
		if [[ `cat ${workingDir}/check_variable | grep " ${VARIABLE_NAME["$var"]}(" -c` -eq 0 ]]
		then 			
  			echo "[ERROR] Variable '${VARIABLE_NAME["$var"]}' not found."
  			exit 1
		else
			testVar=${VARIABLE_NAME["$var"]}
		fi
	elif [[ -n "${VARIABLE_NAME["eastward_$var"]}" ]]
	then

        ncdump -h $infile > ${workingDir}/check_variable
		if [[ `cat ${workingDir}/check_variable | grep " ${VARIABLE_NAME["eastward_$var"]}(" -c` -eq 0 ]]
		then 
			echo "[ERROR] Variable '${VARIABLE_NAME["eastward_$var"]}' not found."
  			exit 1
		else
			testVar=${VARIABLE_NAME["eastward_$var"]}
		fi
	else
		echo "[ERROR] Variable '$var' not found in the default variables."
  		exit 1
	fi
done

#Compute envelope
grdinfo -C $infile?$testVar > ${workingDir}/minmax 

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

if [[ -n "$mapRatioSize" ]]
then 
  projection=-JX`echo "($Xmax - $Xmin)*$mapRatioSize" | bc -l`d/`echo "($Ymax - $Ymin)*$mapRatioSize" | bc -l`d
elif [[ -n "$mapWidth" ]]
then
  projection=-Jm$mapWidth
fi

#For each time
tIndex=0
gmtconvert $infile?time | while read currentSecondTime
do
  currentTimeFilename=`date -u --date="@$currentSecondTime" "$dateFormatFilename"`
  currentTimeSubTitle=`date -u --date="@$currentSecondTime" "$dateFormatSubTitle"`

  if (( $(echo "$currentSecondTime >= $startSecondTime" |bc -l) && $(echo "$currentSecondTime <= $endSecondTime" |bc -l) ))
  then

	echo "Current file : $filename - $currentTimeSubTitle"	

	for var in "${variables[@]}"; do

		set_default_style #reset style
		source $basedir/gmt-scripts/${GMT_SCRIPT["$var"]}.sh
	done
  fi
  
  ((tIndex ++))

done	

#Export to MOV
if test $exportToMov -eq 1
then
	for var in "${variables[@]}"; do

		source $basedir/gmt-scripts/exportToMov.sh	
	done

fi

rm *.eps
rm -rf ${workingDir}
