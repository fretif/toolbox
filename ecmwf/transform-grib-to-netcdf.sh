#!/bin/bash

# PARAMETRES DU SCRIPT
#-------------------------------

# Time
start_date=2010-06-01
end_date=2010-12-01

# Data
isAnalysis=0
isForecast=1

cdo=~/work/softs/cdo-1.6.4/bin/cdo


# DEBUT DU SCRIPT
#-------------------------------

# Calculate start time in seconds
startSecondTime=`date -u --date="$start_date" "+%s"`
currentSecondTime=`date -u --date="$start_date" "+%s"`

# Calculate end time in seconds
endSecondTime=`date -u --date="$end_date" "+%s"`

while [ $currentSecondTime -le $endSecondTime ]; do

	dd=`date -u --date="@$currentSecondTime" "+%Y%m%d"`	
	
	if [ "$isAnalysis" == "1" ] ; then
	  target=MED.analysis.$dd                                                                                                                                                                                
	
	elif [ "$isForecast" == "1" ] ; then	
	  target=MED.forecast.$dd  
	fi
        echo $target

	if [ "$isAnalysis" == "1" ]
	then
	
	  if [[ -f grib/$target.grib ]]
	  then
		  
	    $cdo -t ecmwf -f nc copy grib/$target.grib netcdf/$target.nc
	    # On recalcule le temps à partir de 1970 et non de la date du fichier
	    # => Utile pour concatener plus tard               
	    ncap -O -s "time=time+($currentSecondTime/3600)" netcdf/$target.nc netcdf/$target.nc                
	    ncatted -O -a units,time,c,c,"hours since 1970-01-01 00:00:00" netcdf/$target.nc		    
			  
	  else
		  echo "$target not found !"
		  break;
	  fi
	
	elif [[ "$isForecast" == "1" ]]
	then
	
	  if [[ -f grib/$target.00.grib ]] && [[ -f grib/$target.12.grib ]]
	  then
	
	    $cdo -t ecmwf -f nc copy grib/$target.00.grib netcdf/$target.00.nc
	    # On recalcule le temps à partir de 1970 et non de la date du fichier
	    # => Utile pour concatener plus tard               
	    ncap -O -s "time=time+($currentSecondTime/3600)" netcdf/$target.00.nc netcdf/$target.00.nc                
	    ncatted -O -a units,time,c,c,"hours since 1970-01-01 00:00:00" netcdf/$target.00.nc
	  
	    $cdo -t ecmwf -f nc copy grib/$target.12.grib netcdf/$target.12.nc
	    # On recalcule le temps à partir de 1970 et non de la date du fichier, on ajoute 12h
	    # => Utile pour concatener plus tard               
	    ncap -O -s "time=time+12+($currentSecondTime/3600)" netcdf/$target.12.nc netcdf/$target.12.nc                
	    ncatted -O -a units,time,c,c,"hours since 1970-01-01 00:00:00" netcdf/$target.12.nc
	    
	    ncrcat netcdf/$target.00.nc netcdf/$target.12.nc -o netcdf/$target.nc
	    rm -f netcdf/$target.00.nc netcdf/$target.12.nc    
	    
	    # Change CLWC,CIWC  variables 
	    ncrename -v CLWC,U100 netcdf/$target.nc
	    ncrename -v CIWC,V100 netcdf/$target.nc
	    ncatted -a long_name,U100,o,c,"100 metre U wind component" netcdf/$target.nc
	    ncatted -a units,U100,o,c,"m s**-1" netcdf/$target.nc
	    ncatted -a long_name,V100,o,c,"100 metre V wind component" netcdf/$target.nc
	    ncatted -a units,V100,o,c,"m s**-1" netcdf/$target.nc	  
			  
	  else
		  echo "$target.00 or $target.12 not found !"
		  break;
	  fi
	fi       
	
	# On ajoute un jour	
	currentSecondTime=`echo "$currentSecondTime + 3600 * 24" | bc `
done

