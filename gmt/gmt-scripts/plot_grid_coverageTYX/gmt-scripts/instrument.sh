#!/bin/bash

psxy $instrumentFile ${envelope} -Sc${instruCircleSize} -G${instruCircleColor} -Wthinnest,black,solid -J -P -O -K >> ${outfile}.ps

awk 'NR%2==1{ printf("%s %s %s\n",$1,$2,$3)}' $instrumentFile > ${workingDir}/label.dat
pstext ${workingDir}/label.dat ${envelope} -To -F+f${instruFontSize},Helvetica -D${instruDxOffset}/${instruDyOffset} -Gwhite -J -P -O -K >> ${outfile}.ps

awk 'NR%2==0{ printf("%s %s %s\n",$1,$2,$3)}' $instrumentFile > ${workingDir}/label.dat
pstext ${workingDir}/label.dat ${envelope} -To -F+f${instruFontSize},Helvetica -D-${instruDxOffset}/-${instruDyOffset} -Gwhite -J -P -O -K >> ${outfile}.ps

