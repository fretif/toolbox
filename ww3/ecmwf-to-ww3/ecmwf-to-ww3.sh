#!/bin/bash

inputDir="/home/retf/work/fieldsites/med-cruesim/modelling/ecmwf/netcdf/pool/"
inputFile="previ-Med*"
outputDir=""
outputFile="previ-Med-wind-ww3.nc"

ncrcat -v U10M,V10M ${inputDir}${inputFile} ${outputDir}temp.nc
ncpdq -a '-lat' ${outputDir}temp.nc ${outputDir}${outputFile}
rm -f ${outputDir}temp.nc

