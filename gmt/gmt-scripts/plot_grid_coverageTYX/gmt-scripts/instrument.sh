#!/bin/bash

#psxy  $instrumentFile ${envelope} -Sc -J -P -O -K >> ${outfile}.ps

psxy ${envelope} $instrumentFile/adcp.xy -S -Ggreen -Wfaint,black,solid -J -P -O -K >> ${outfile}.ps
psxy ${envelope} $instrumentFile/cigu-bouy.xy -S -Gred -Wfaint,black,solid -J -P -O -K >> ${outfile}.ps
#psxy ${envelope} $instrumentFile/meteo.xy -S -Gorange -Wfaint,black,solid -J -P -O -K >> ${outfile}.ps
psxy ${envelope} $instrumentFile/tide.xy -S -Gpurple -Wfaint,black,solid -J -P -O -K >> ${outfile}.ps

