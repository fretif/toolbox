#!/bin/csh

#################################################################
#------------------------------- 								#
# MARS request - aide mémoire									#
#-------------------------------								#
												#
#------------------------------- 								#
# class												#
#-------------------------------								#
# od 	Operational archive 									#
# er 	REANALYSE 										#
# e4 	REANALYSE40 										#
# ei 	ERA Interim 
# voir http://apps.ecmwf.int/codes/grib/format/mars/class/

#------------------------------- 
# stream
#-------------------------------
# oper 	Atmospheric model 
# scda 	Atmospheric model (short cutoff) 
# dcda 	Atmospheric model (delayed cutoff) 
# fsob 	Forecast sensitivity to observations 
# voir http://apps.ecmwf.int/codes/grib/format/mars/stream/

#------------------------------- 
# expver : is the version of the data.
#-------------------------------
# 1	Production data 

#------------------------------- 
# type
#-------------------------------
# an 	Analysis 
# fc 	Forecast 
# voir http://apps.ecmwf.int/codes/grib/format/mars/type/

#------------------------------- 
# levtype
#-------------------------------
# ml	Model level
# pl	Pressure level
# sfc	Surface
# pv	Poential vorticity
# pt	Potential temperature
# dp	Depth

#-------------------------------
# area
#-------------------------------
# North/West/South/East;									#
# if South > North, the values are swapped and a warning issued;				#
# southern latitudes and western longitudes must be given as 					#
# negative numbers										#
												#
#-------------------------------								#
# param												#
#-------------------------------								#
# voir http://apps.ecmwf.int/codes/grib/param-db/						#
#												#
#####################################################################

# PARAMETRES DU SCRIPT
#-------------------------------

# Time
set start_date=2013-02-25
set end_date=2013-04-01

# Grid
set area=48/-10/30/38
set grid=0.125/0.125

# Data
set getAnalysis=1
set getForecast=0

# Repertoire de travail
cd /scratch/ms/fr/tohw/med-previ

# DEBUT DU SCRIPT
#-------------------------------

# Calculate start time in seconds
set startSecondTime=`date -u --date="$start_date" "+%s"`
set currentSecondTime=`date -u --date="$start_date" "+%s"`

# Calculate end time in seconds
set endSecondTime=`date -u --date="$end_date" "+%s"`

while ( $currentSecondTime <= $endSecondTime )

	set dd=`date -u --date="@$currentSecondTime" "+%Y%m%d"`

	if ($getAnalysis == 1) then
	
	# 1. On recupere les analyses à 6h
	
		cat >request <<EOF
  retrieve,
  date=$dd,
  class=od,
  stream=oper,
  expver=1,
  type=an,
  levtype=sfc,
  time=00/06/12/18,		
  # Parameters= LSM,U10,V10,SP,MSL,T2M,D2M
  param=172.128/165.128/166.128/134.128/151.128/167.128/168.128,
  area=$area,
  grid=$grid,
  target=MED.analysis.$dd.grib
EOF

	    	echo 'mars request for '$dd
			mars request  # executes the program created above

	    	if ( $? != 0 ) then # Check MARS exit code.
			echo " The MARS request failed for $dd."
			exit 1 
		endif #end-check-exit-code
	endif #end-analysis

      if ($getForecast == 1) then
	
	# 2. On recupere les previsions à 1h 
	
		cat >request <<EOF
  retrieve,
  date=$dd,
  class=od,
  stream=oper,
  expver=1,
  type=fc,
  levtype=sfc,
  time=00/12,	
  step=01/to/12/by/01,	
  # Parameters= LSM,SP,MSL,SSHF,SLHF,U10,V10,T2M,D2M,SSRD,STRD,SSR,STR,TP
  param=172.128/134.128/151.128/146.128/147.128/165.128/166.128/167.128/168.128/169.128/175.128/176.128/177.128/228.128,	
  area=$area,
  grid=$grid,
  target=MED.forecast.$dd.grib
EOF

		echo 'mars request for '$dd
		mars request  # executes the program created above
 
		if ( $? != 0 ) then # Check MARS exit code.  
			echo " The MARS request failed for $dd."
			exit 1
		endif #end-check-exit-code
	endif #end-forecast

	
	# 3. On ajoute un jour
	
	set currentSecondTime=`echo "$currentSecondTime + 3600 * 24" | bc `

end #end-while

exit 0

# Pour mettre la dimensions temps en ilimité: 
for f in *.nc; do ncks --mk_rec_dmn time $f -o myfileunlimited.nc ; mv myfileunlimited.nc $f ; done


