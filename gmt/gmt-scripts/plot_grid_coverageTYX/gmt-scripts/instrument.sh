#!/bin/bash

psxy  $instrumentFile ${envelope} -Sc0.03 -Gorange -Wthin,black,solid -J -P -O -K >> ${outfile}.ps

awk 'NR%2==1{ printf("%s %s %s\n",$1,$2,$3)}' $instrumentFile > ${workingDir}/label.dat
pstext ${workingDir}/label.dat ${envelope} -To -F+f4p,Arial -D0.15/0 -J -P -O -K >> ${outfile}.ps

awk 'NR%2==0{ printf("%s %s %s\n",$1,$2,$3)}' $instrumentFile > ${workingDir}/label.dat
pstext ${workingDir}/label.dat ${envelope} -To -F+f4p,Arial, -D-0.15/0 -J -P -O -K >> ${outfile}.ps

