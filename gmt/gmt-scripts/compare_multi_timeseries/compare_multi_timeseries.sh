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
gmtset FONT_ANNOT_SECONDARY white

gmtset MAP_TICK_LENGTH_SECONDARY 5p

gmtset PS_LINE_JOIN miter
gmtset PS_LINE_CAP butt
gmtset PS_MITER_LIMIT 180
LANG=en_us_8859_1

gmtset FORMAT_DATE_MAP=dd/mm

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

paramR="-R$startTime/$endTime"

if [[ $maxGroup == 1 ]]
then
  paramJ="-JX25cT/10c"
  paramJText="-JX25c/10c"
else
  paramJ="-JX10cT/4c"
  paramJsmall="-JX10cT/2c"
  paramJText="-JX10c/4c"
fi

parsedTime="${startTime:0:4}-${startTime:5:2}-${startTime:8:2}"
startTimeTitle=`date --date="$parsedTime" "+%d %B %Y"`
parsedTime="${endTime:0:4}-${endTime:5:2}-${endTime:8:2}"
endTimeTitle=`date --date="$parsedTime" "+%d %B %Y"`

#graphOffsetX=12
graphOffsetX=11.5
graphOffsetY=5

for ((group=1;group<=$maxGroup;group++)) do 

  if [[ $group == 1 ]]
  then       
    psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -K > ${outfile}.ps
  fi
  
  if [[ $group == 2 ]]
  then  
    if [[ $plotPerLine == 1 ]]
    then   
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -Y$graphOffsetY -O -K >> ${outfile}.ps
    else       
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -X$graphOffsetX -Y0 -O -K >> ${outfile}.ps
    fi     
  fi
  
  if [[ $group == 3 ]]
  then  
    if [[ $plotPerLine == 1 ]]
    then   
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -Y$graphOffsetY -O -K >> ${outfile}.ps    
    elif [[ $plotPerLine == 2 ]]
    then   
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -X-$graphOffsetX -Y$graphOffsetY -O -K >> ${outfile}.ps
    else
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]} -BWS -X$graphOffsetX -Y0 -O -K >> ${outfile}.ps
    fi   
  fi
  
  if [[ $group == 4 ]]
  then   
    if [[ $plotPerLine == 1 ]]
    then   
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -Y$graphOffsetY -O -K >> ${outfile}.ps    
    elif [[ $plotPerLine == 3 ]]
    then 
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -X-`echo "$graphOffsetX*($plotPerLine-1)" | bc -l` -Y$graphOffsetY -O -K >> ${outfile}.ps
    else        
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]} -BWS -X$graphOffsetX -Y0 -O -K >> ${outfile}.ps
    fi  
  fi
  
   if [[ $group == 5 ]]
  then   
    if [[ $plotPerLine == 1 ]]
    then   
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -Y$graphOffsetY -O -K >> ${outfile}.ps    
    elif [[ $plotPerLine == 2 ]]
    then   
        psbasemap$paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -X-`echo "$graphOffsetX*($plotPerLine-1)" | bc -l` -Y$graphOffsetY -O -K >> ${outfile}.ps
    else
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]} -BWS -X$graphOffsetX -Y0 -O -K >> ${outfile}.ps
    fi 
  fi
  
   if [[ $group == 6 ]]
  then   
    if [[ $plotPerLine == 1 ]]
    then   
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -Y$graphOffsetY -O -K >> ${outfile}.ps    
    else
	psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]} -BWS -X$graphOffsetX -Y0 -O -K >> ${outfile}.ps
    fi
  fi
  
   if [[ $group == 7 ]]
  then   
    if [[ $plotPerLine == 1 ]]
    then   
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -Y$graphOffsetY -O -K >> ${outfile}.ps    
    elif [[ $plotPerLine == 3 ]]
    then   
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -X-`echo "$graphOffsetX*($plotPerLine-1)" | bc -l` -Y$graphOffsetY -O -K >> ${outfile}.ps
    else
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]} -BWS -X$graphOffsetX -Y0 -O -K >> ${outfile}.ps
    fi  
  fi
  
   if [[ $group == 8 ]]
  then   
    if [[ $plotPerLine == 1 ]]
    then   
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -Y6 -O -K >> ${outfile}.ps    
    else
	psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]} -BWS -X$graphOffsetX -Y0 -O -K >> ${outfile}.ps
    fi
  fi
  
   if [[ $group == 9 ]]
  then   
    if [[ $plotPerLine == 1 ]]
    then   
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -Y$graphOffsetY -O -K >> ${outfile}.ps    
    else
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]} -BWS -X$graphOffsetX -Y0 -O -K >> ${outfile}.ps
    fi
  fi
  
   if [[ $group == 10 ]]
  then   
    if [[ $plotPerLine == 1 ]]
    then   
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -Y$graphOffsetY -O -K >> ${outfile}.ps    
    elif [[ $plotPerLine == 3 ]]
    then   
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -X-`echo "$graphOffsetX*($plotPerLine-1)" | bc -l` -Y$graphOffsetY -O -K >> ${outfile}.ps
    else
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]} -BWS -X$graphOffsetX -Y0 -O -K >> ${outfile}.ps
    fi  
  fi
  
   if [[ $group == 11 ]]
  then   
    if [[ $plotPerLine == 1 ]]
    then   
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -Y$graphOffsetY -O -K >> ${outfile}.ps    
    else
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]} -BWS -X$graphOffsetX -Y0 -O -K >> ${outfile}.ps
    fi
  fi
  
   if [[ $group == 12 ]]
  then   
    if [[ $plotPerLine == 1 ]]
    then   
        psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]}+l"${titleYGroup["$group"]}" -BWS -Y$graphOffsetY -O -K >> ${outfile}.ps    
    else
	psbasemap $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Bsx${secondAnnotX} -Bpx${annontX} -Bpy${annontYGroup["$group"]} -BWS -X$graphOffsetX -Y0 -O -K >> ${outfile}.ps
    fi
  fi

  countFiles=0

  for ((index=1;index<=$maxFile;index++)) do 

	  if [[ -f "${files["$group$index"]}" ]]
	  then
		  file=${files["$group$index"]}

		  if [[ -n "${formats["$group$index"]}" ]] 
		  then
			  format=${formats["$group$index"]}

			  if [[ -n "${titles["$group$index"]}" ]] 
			  then
				  fileTitle=${titles["$group$index"]}
			  else
				  fileTitle="undefined"
			  fi

			  if [[ -n "${colors["$group$index"]}" ]] 
			  then
				  color=${colors["$group$index"]}
			  else
				  color="black"
			  fi

			  if [[ -n "${styles["$group$index"]}" ]] 
			  then
				  style=${styles["$group$index"]}
			  else
				  style="solid"
			  fi

			  if [[ "${format}" == "gmt" ]] 
			  then
				  # GMT Format #
				  if [[ ! -n "${columns["$group$index"]}" ]] 
				  then
					  cp $file ${workingDir}/file.tmp	

				  else					
					  awk '$0~/#/ {next;}
				      { printf("%s %s\n",$1,$'${columns["$group$index"]}'); 	  
				      }' $file > ${workingDir}/file.tmp					
				  fi

			  elif [[ "${format}" == "kunshen" ]] 
			  then
				  if [[ ! -n "${columns["$group$index"]}" ]] 
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
					printf("%s %s\n",dateGMT,$'${columns["$group$index"]}'); 	  
				      }' $file > ${workingDir}/file.tmp

			  elif [[ "${format}" == "matlab" ]] 
			then
				if [[ ! -n "${columns["$group$index"]}" ]] 
				then
					echo "You need select a column for Matlab."				
				fi

				# MATLAB Format #
				 
				awk '$0~/#/ {next;}
				     { year  = substr($1,1,4); 
				       month = substr($1,5,2);
				       day   = substr($1,7,2);
				       hour  = substr($1,9,2);
				       min   = substr($1,11,2);
				       sec   = substr($1,13,2);      
				       dateGMT = year"-"month"-"day"T"hour":"min":"sec;
				       printf("%s %s\n",dateGMT,$'${columns["$group$index"]}'); 	  
				     }' $file > ${workingDir}/file.tmp

			elif [[ "${format}" == "sirocco" ]] 
			  then
				  if [[ ! -n "${columns["$group$index"]}" ]] 
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
					printf("%s %s\n",dateGMT,$'${columns["$group$index"]}'); 	  
				      }' $file > ${workingDir}/file.tmp				

			  elif [[ "${format}" == "ww3" ]] 
			  then

				  if [[ ! -n "${columns["$group$index"]}" ]] 
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
					printf("%s %s\n",dateGMT,$'${columns["$group$index"]}'); 	  
				      }' $file > ${workingDir}/file.tmp	
			  else
				  echo "Unknowed format for file $index."
			  fi

			  # TODO 
			  #offsetsTime[1]="40 min"
			  #offsetsZ[1]=0
			  if [[ -n "${offsetTime["$group$index"]}" ]] 
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
					
					dateCmd = "date -u --date='\''"utcTime " '${offsetTime["$group$index"]}' ""'\'' '"'+%Y%m%d%H%M%S'"'"	
					dateCmd|getline utcTime;
					close (dateCmd); 
					
					  year  = substr(utcTime,1,4); 
						month = substr(utcTime,5,2);
						day   = substr(utcTime,7,2);
						hour  = substr(utcTime,9,2); 
						min   = substr(utcTime,11,2); 
						sec   = substr(utcTime,15,2);
						
						
					dateGMT = year"-"month"-"day"T"hour":"min":"sec;
					printf("%s %s\n",dateGMT,$2);
				    
			      }' ${workingDir}/file.tmp > ${workingDir}/file-time.tmp

			      mv ${workingDir}/file-time.tmp ${workingDir}/file.tmp				
			  fi

			  if [[ -n "${offsetValue["$group$index"]}" ]] 
			  then

				  awk '$0~/#/ {next;}
				  {
					printf("%s %s\n",$1,$2'${offsetValue["$group$index"]}');
				    
			      }' ${workingDir}/file.tmp > ${workingDir}/file-value.tmp

			      mv ${workingDir}/file-value.tmp ${workingDir}/file.tmp
			  fi

			  #if [[ "${index}" == "2" ]]
			  #then
			  #	cp ${workingDir}/file.tmp .
			  #fi
			  
			  if [[ "${style}" == "circle" ]] 
			  then			    
				  psxy ${workingDir}/file.tmp $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Sc0.1 -W0.1p,$color,solid -O -K >> ${outfile}.ps
			  
			  elif [[ "${style}" == "circlef" ]] 
			  then			    
				  psxy ${workingDir}/file.tmp $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -Sc0.1 -G$color -W0.3p,$color,solid -O -K >> ${outfile}.ps
			  elif [[ "${style}" == "direction" ]] 
			  then
			      awk '$0~/#/ {next;}
				NR%8==0{				       
				       printf("%s %s %s 0.12i\n",$1,6,$2);
				  
			     }' ${workingDir}/file.tmp > ${workingDir}/file-time.tmp
			     
			     mv ${workingDir}/file-time.tmp ${workingDir}/file.tmp
                             psxy ${workingDir}/file.tmp $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -SV0.09i+b -W0.8p -G$color -O -K >> ${outfile}.ps
			  else
                                #head ${workingDir}/file.tmp
                              
                                #if [[ $group == 3 ]]
			        #then
				#	psxy ${workingDir}/file.tmp $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJsmall -W1p,$color,$style -O -K >> ${outfile}.ps 
                                #else
			  		psxy ${workingDir}/file.tmp $paramR/${ZminGroup["$group"]}/${ZmaxGroup["$group"]} $paramJ -W1p,$color,$style -O -K >> ${outfile}.ps 
                                #fi
			fi	  
			  
			  #if [[ $group == 1 ]]
			  #then
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
			  #fi
			  
			  if [[ -f "${statFileGroup["$group$index"]}" ]]
			  then 			   
			    pstext ${statFileGroup["$group$index"]} -R0/10/0/10 $paramJText -Gwhite -F+f10p -W0.7p,$color,solid -M -O -K >> ${outfile}.ps
			  fi
			  
			  (( countFiles ++))

		  else
			  echo "Please set a format for file $index."
		  fi		

	  else
		  echo "File $index doesn't exists."
	  fi

  done
  
   echo "5 9.5 ${titlesGroup[$group]}" | pstext -R0/10/0/10 $paramJText -O -K >> ${outfile}.ps	
   
done

pslegend ${workingDir}/legend $paramR/${ZminGroup["1"]}/${ZmaxGroup["1"]} $paramJ -Dx-0.2i/`echo "0.2*$countFiles" | bc -l`i/5i/3.3i/BL -X-`echo "$graphOffsetX*($plotPerLine-1)" | bc -l` -Y-3 -O >> ${outfile}.ps

#echo "5 9.5 $title"  | pstext -R0/10/0/10 $paramJText -Gwhite -F+f22p -To -W0.5p,black,solid -Y5.5 -O >> ${outfile}.ps

ps2raster ${outfile}.ps -A -E$png_resolution -Tg -P

rm -f ${outfile}.ps
rm *.eps
rm -rf ${workingDir}
