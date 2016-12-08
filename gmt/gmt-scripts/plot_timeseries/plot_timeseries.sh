#!/bin/bash

#########################
#	Better looklike		#
#########################
gmtset COLOR_BACKGROUND  220/220/220
gmtset COLOR_FOREGROUND 50/50/20
gmtset COLOR_NAN 255/255/255
gmtset MAP_FRAME_TYPE fancy
gmtset MAP_FRAME_WIDTH 0.1c
gmtset MAP_FRAME_PEN 0.05c
gmtset MAP_LABEL_OFFSET 0.25c
gmtset MAP_ANNOT_OBLIQUE 32
gmtset MAP_ANNOT_MIN_SPACING 1c
gmtset PS_MEDIA A3+   # A3+ was fine with -Jx1:2000

gmtset MAP_GRID_CROSS_SIZE_PRIMARY 0
gmtset MAP_GRID_PEN_PRIMARY 0.015c,0/0/0,.
gmtset MAP_TICK_PEN_PRIMARY 0.01c

gmtset MAP_GRID_PEN_SECONDARY 0.015c,0/0/0,solid
gmtset MAP_GRID_CROSS_SIZE_SECONDARY 0
gmtset MAP_TICK_PEN_SECONDARY 0.01c

gmtset FONT_ANNOT_PRIMARY 10p,Helvetica,black
gmtset FONT_ANNOT_SECONDARY black

gmtset MAP_TICK_LENGTH_SECONDARY 5p

gmtset PS_LINE_JOIN miter
gmtset PS_LINE_CAP butt
gmtset PS_MITER_LIMIT 180
LANG=en_us_8859_1

gmtset FORMAT_DATE_MAP=dd/mm
gmtset FORMAT_CLOCK_MAP=hh:mm

#################
#	CONFIG File	#
#################

basedir="${0%/*}"
source $1

#################
#	BEGIN	#
#################

workingDir=`mktemp -d`

if [[ ! -n "$Zmin" && ! -n "$Zmax" ]] 
then

	minmax $file1 $file2 $file3 $file4 -I1 > ${workingDir}/minmax
	Zmin=`cat ${workingDir}/minmax | awk -F"/" '{print $3}'`
	Zmax=`cat ${workingDir}/minmax | awk -F"/" '{print $4}'`
fi

if [[ ! -n "$outfile" ]] 
then

	outfile="track"
fi

paramR="-R$startTime/$endTime/$Zmin/$Zmax"

#paramJ="-JX25cT/10c"
#paramJText="-JX25c/10c"

paramJ="-JX10cT/5c"
paramJText="-JX10c/5c"

parsedTime="${startTime:0:4}-${startTime:5:2}-${startTime:8:2}"
startTimeTitle=`date --date="$parsedTime" "+%d %B %Y"`
parsedTime="${endTime:0:4}-${endTime:5:2}-${endTime:8:2}"
endTimeTitle=`date --date="$parsedTime" "+%d %B %Y"`

#psbasemap $paramR $paramJ -Bsx${secondAnnotX} -Bpx${annontX}+l"${titleX}" -Bpy${annontY}+l"${titleY}" -BWS  -K > ${outfile}.ps
psbasemap $paramR $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontY}+l"${titleY}" -BWS  -K > ${outfile}.ps

# Plot typhoons
#	nb=0
#	colors=("291.18-1-1" "273.53-1-1" "255.88-1-1" "238.24-1-1" "220.59-1-1" "202.94-1-1" "185.29-1-1" "167.65-1-1" "150-1-1" "132.35-1-1" "114.71-1-1" "97.059-1-1" "79.412-1-1" "61.765-1-1" "44.118-1-1" "26.471-1-1" "8.8235-1-1" "black");
#	for typhon in /data/fieldsites/taiwan/raw-data/tracks_typhoons/kunshen/*; do 
#
#		file=$(basename "$typhon")
#		filename="${file%.*}"
#
#		nb=$[$nb+1];
#
#		# Calculate start time in seconds
#		time=`head -n 1 $typhon | cut -f 1`
#		startTime="${time:0:4}-${time:4:2}-${time:6:2}T${time:8:2}:${time:10:2}:${time:12:2}"		       
#
#		# Calculate end time in seconds
#		time=`tail -n 1 $typhon | cut -f 1`
#		endTime="${time:0:4}-${time:4:2}-${time:6:2}T${time:8:2}:${time:10:2}:${time:12:2}"	
#
#	        echo "$startTime	1.6" >> ${workingDir}/typhon
#		echo "$endTime	1.6" >> ${workingDir}/typhon
#
#		psxy ${workingDir}/typhon $paramR $paramJ -Sb0.05c -G${colors[$nb]} -O -K >> ${outfile}.ps
#		#echo "$startTime 20 $filename" | pstext $paramR $paramJ -F+a90 -O -K >> ${outfile}.ps
#
#		rm ${workingDir}/typhon	
#
#	done


countFiles=0

for index in "${!files[@]}"; do 

	if [[ -f "${files[$index]}" ]]
	then
 		file=${files[$index]}

		if [[ -n "${formats[$index]}" ]] 
		then
			format=${formats[$index]}

			if [[ -n "${titles[$index]}" ]] 
			then
				fileTitle=${titles[$index]}
			else
				fileTitle="undefined"
			fi

			if [[ -n "${colors[$index]}" ]] 
			then
				color=${colors[$index]}
			else
				color="black"
			fi

			if [[ -n "${styles[$index]}" ]] 
			then
				style=${styles[$index]}
			else
				style="solid"
			fi

			if [[ "${format}" == "gmt" ]] 
			then
				# GMT Format #
				if [[ ! -n "${columns[$index]}" ]] 
				then
					cp $file ${workingDir}/file.tmp	

				else					
					awk '$0~/#/ {next;}
				     { printf("%s %s\n",$1,$'${columns[$index]}'); 	  
				     }' $file > ${workingDir}/file.tmp					
				fi

			elif [[ "${format}" == "kunshen" ]] 
			then
				if [[ ! -n "${columns[$index]}" ]] 
				then
					echo "You need select a column for Kunshen."				
				fi

				# KUNSHEN Format #
				 
				awk '$0~/#/ {next;}
				     { year  = substr($2,1,4); 
				       month = substr($2,5,2);
				       day   = substr($2,7,2);
				       hour  = substr($2,9,2);
				       min   = substr($2,11,2);
				       sec   = substr($2,13,2);      
				       dateGMT = year"-"month"-"day"T"hour":"min":"sec;
				       printf("%s %s\n",dateGMT,$'${columns[$index]}'); 	  
				     }' $file > ${workingDir}/file.tmp

			elif [[ "${format}" == "sirocco" ]] 
			then
				if [[ ! -n "${columns[$index]}" ]] 
				then
					echo "You need select a column for Sirocco."				
				fi

				# SIROCCO Format #
				 
				awk -F'\t' '$0~/#/ {next;}
				     { year  = substr($1,1,4); 
				       month = substr($1,6,2);
				       day   = substr($1,9,2);
				       hour  = substr($1,12,2);
				       min   = substr($1,15,2);
				       sec   = substr($1,18,2);      
				       dateGMT = year"-"month"-"day"T"hour":"min":"sec;				       
				       printf("%s %s\n",dateGMT,$'${columns[$index]}'); 	  
				     }' $file > ${workingDir}/file.tmp					     

			elif [[ "${format}" == "ww3" ]] 
			then

				if [[ ! -n "${columns[$index]}" ]] 
				then
					echo "You need select a column for WW3."				
				fi

				# WW3 Format #   
				awk 'NR > 3 { 
				       year  = substr($1,1,4); 
				       month = substr($1,5,2);
				       day   = substr($1,7,2);
				       hour  = substr($2,1,2);
				       min   = substr($3,1,2);
				       sec   = substr($4,1,2);
				      dateGMT = year"-"month"-"day"T"hour":"min":"sec;
				       printf("%s %s\n",dateGMT,$'${columns[$index]}'); 	  
				     }' $file > ${workingDir}/file.tmp	
			else
				echo "Unknowed format for file $index."
			fi

			# TODO 
			#offsetsTime[1]="40 min"
			#offsetsZ[1]=0
			if [[ -n "${offsetTime[$index]}" ]] 
			then
				awk '$0~/#/ {next;}
				{
				       year  = substr($1,1,4); 
				       month = substr($1,6,2);
				       day   = substr($1,9,2);
				       hour  = substr($1,12,2); 
				       min   = substr($1,15,2); 
				       sec   = substr($1,18,2); 

				       utcTime= year"-"month"-"day" "hour":"min":"sec;	
				       
				       dateCmd = "date -u --date='\''"utcTime " '${offsetTime[$index]}' ""'\'' '"'+%Y%m%d%H%M%S'"'"	
				       dateCmd|getline utcTime;
				       close (dateCmd); 
				       
					year  = substr(utcTime,1,4); 
					month = substr(utcTime,5,2);
					day   = substr(utcTime,7,2);
					hour  = substr(utcTime,9,2); 
					min   = substr(utcTime,11,2); 
					sec   = substr(utcTime,13,2);	
					
				       dateGMT = year"-"month"-"day"T"hour":"min":"sec;
				       printf("%s %s\n",dateGMT,$2);
				  
			     }' ${workingDir}/file.tmp > ${workingDir}/file-time.tmp

			     mv ${workingDir}/file-time.tmp ${workingDir}/file.tmp				
			fi

			if [[ -n "${offsetValue[$index]}" ]] 
			then

				awk '$0~/#/ {next;}
				{
				       printf("%s %s\n",$1,$2'${offsetValue[$index]}');
				  
			     }' ${workingDir}/file.tmp > ${workingDir}/file-value.tmp

			     mv ${workingDir}/file-value.tmp ${workingDir}/file.tmp			    
			fi

			#if [[ "${index}" == "2" ]]
			#then
			#	cp ${workingDir}/file.tmp .
			#fi
			if [[ "${style}" == "circle" ]] 
			then			    
				  psxy ${workingDir}/file.tmp $paramR $paramJ -Sc0.1 -W0.3p,$color,solid -O -K >> ${outfile}.ps
			  
			elif [[ "${style}" == "circlef" ]] 
			then			    
				  psxy ${workingDir}/file.tmp $paramR $paramJ -Sc0.1 -G$color -W0.3p,$color,solid -O -K >> ${outfile}.ps
			elif [[ "${style}" == "direction" ]] 
			then
			      awk '$0~/#/ {next;}
				{				       
				       printf("%s %s %s 0.12i\n",$1,21,$2);
				  
			     }' ${workingDir}/file.tmp > ${workingDir}/file-time.tmp
			     
			     mv ${workingDir}/file-time.tmp ${workingDir}/file.tmp			     
			     psxy ${workingDir}/file.tmp $paramR $paramJ -SV0.09i+b -W0.8p -G$color -O -K >> ${outfile}.ps
			else
				  psxy ${workingDir}/file.tmp $paramR $paramJ -W1p,$color,$style -O -K >> ${outfile}.ps #-Y`echo "0.3 * $index" | bc -l`
				  #psxy ${workingDir}/file.tmp $paramR $paramJ -W1p,$color,$style -O -K -Y`echo "0.5 * $index" | bc -l` >> ${outfile}.ps
			fi				

			if [[ "${style}" == "circle" ]] || [[ "${style}" == "circlef" ]] 
			    then
			      echo "S 0.1i c 0.1i - thin,$color,solid 0.3i $fileTitle" >> ${workingDir}/legend
			elif [[ "${style}" == "direction" ]]  
			    then
			      echo "S 0.1i v0.1i+a40+e 0.15i $color thin 0.3i $fileTitle" >> ${workingDir}/legend
			      #S 0.1i v0.1i+a40+e 0.25i magenta 0.25p 0.3i This is a vector
			 else
			      echo "S 0.1i - 0.15i - thin,$color,$style 0.3i $fileTitle" >> ${workingDir}/legend
			 fi
			(( countFiles ++))

		else
			echo "Please set a format for file $index."
		fi		

	else
		echo "File $index doesn't exists."
	fi

done

#echo "5 9.5 $startTimeTitle - $endTimeTitle" | pstext -R0/10/0/10 $paramJText -Y1 -O -K >> ${outfile}.ps
#echo "5 9 $title" | pstext -R -J -Y1.2 -O -K >> ${outfile}.ps
   echo "5 9.5 ${title}" | pstext -R0/10/0/10 $paramJText -Gwhite -To -W0.5p,black,solid -O -K >> ${outfile}.ps	

#pslegend ${workingDir}/legend $paramR $paramJ -Dx-0.2i/`echo "0.2*$countFiles" | bc -l`i/5i/3.3i/BL -O >> ${outfile}.ps
pslegend ${workingDir}/legend $paramR $paramJ -Dx-0.2i/`echo "0.2" | bc -l`i/5i/3.3i/BL -X-0 -Y-2.3 -O >> ${outfile}.ps
#pslegend ${workingDir}/legend $paramR $paramJ -Dx0.1i/0i+w2.2i/0.6i+jBL+l1.2 -F+p0.3p+gwhite -Y8.5 -O >> ${outfile}.ps

ps2raster ${outfile}.ps -A -E300 -Tg -P

rm -f ${outfile}.ps
rm *.eps
rm -rf ${workingDir}
