#!/bin/bash

awk '{ 
       year  = substr($1,1,4); 
       month = substr($1,5,2);
       day   = substr($1,7,2);
       hour  = substr($1,9,2);
       min   = substr($1,11,2);
       sec   = substr($1,13,2); 
       parsedTime = year"-"month"-"day" "hour":"min":"sec;
	
       dateCmd = "date -u --date='\''"parsedTime"'\'' +%s"
       dateCmd|getline currentTyphonTime;
       close (dateCmd);

       if(currentTyphonTime <= "'$currentSecondTime'") {
				
	       month = substr($1,5,2);
	       day   = substr($1,7,2);
	       hour  = substr($1,9,2);      

	       time= year"/"month"/"day" "hour"h";	
	       printf("%s %s %s\n",$2,$3,time);
       }
     }' $typhonFile > ${workingDir}/typhon_track.dat

awk 'NR % 2 == 1{ print $0;}' ${workingDir}/typhon_track.dat > ${workingDir}/typhon_label.dat

psxy  ${workingDir}/typhon_track.dat ${envelope} -i0,1 -W4p,black,solid -J -P -O -K >> ${outfile}.ps
#pstext ${workingDir}/typhon_label.dat ${envelope} -To -W0.3p,black,solid -F+f10p,Helvetica,-=0.5p,black+a0 -D0.4/1.3 -J -P -O -K >> ${outfile}.ps
