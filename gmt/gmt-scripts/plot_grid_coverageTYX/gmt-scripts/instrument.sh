#!/bin/bash

psxy  $instrumentFile ${envelope} -Gred -W2p -J -P -O -K >> ${outfile}.ps

echo "3.066668 42.704167" | psxy ${envelope} -Sc0.3c -Gorange -Wthin,black,solid -J -P -O -K -V >> ${outfile}.ps
#psxy ${envelope} $instrumentFile/cigu-bouy.xy -S -Gred -Wfaint,black,solid -J -P -O -K >> ${outfile}.ps
#psxy ${envelope} $instrumentFile/meteo.xy -S -Gorange -Wfaint,black,solid -J -P -O -K >> ${outfile}.ps
#psxy ${envelope} $instrumentFile/tide.xy -S -Gpurple -Wfaint,black,solid -J -P -O -K >> ${outfile}.ps

