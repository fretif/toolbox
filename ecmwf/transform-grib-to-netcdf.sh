#!/bin/bash

# PARAMETRES DU SCRIPT
#-------------------------------

# Time
start_date=2013-02-25
end_date=2013-04-01

# DEBUT DU SCRIPT
#-------------------------------

# Calculate start time in seconds
startSecondTime=`date -u --date="$start_date" "+%s"`
currentSecondTime=`date -u --date="$start_date" "+%s"`

# Calculate end time in seconds
endSecondTime=`date -u --date="$end_date" "+%s"`

while [ $currentSecondTime -le $endSecondTime ]; do

	dd=`date -u --date="@$currentSecondTime" "+%Y%m%d"`	
	
	target=MED.analysis.$dd                                                                                                                                                                                
        echo $target

        if [[ -f grib/$target.grib ]]
        then
                cdo -t ecmwf -f nc copy grib/$target.grib netcdf/$target.nc
                # On recalcule le temps à partir de 1970 et non de la date du fichier
                # => Utile pour concatener plus tard               
                ncap -O -s "time=time+($currentSecondTime/3600)" netcdf/$target.nc netcdf/$target.nc                
                ncatted -O -a units,time,c,c,"hours since 1970-01-01 00:00:00" netcdf/$target.nc
        else
                break;
        fi
	
	# On ajoute un jour
	
	currentSecondTime=`echo "$currentSecondTime + 3600 * 24" | bc `
done

