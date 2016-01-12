#!/bin/bash

if [[ -z "$1" ]]
then

	echo "You must specify a configuration file as arguments."
	echo "This is an example of a configuration file :"
	echo "# Directory parameters
scanDir=\"/work/thesis/fieldsites/taiwan/modelling/large-scale/hydro/model/GRAPHIQUES/KUNSHEN-RIVERS-001/\"
outDir=\"/work/thesis/fieldsites/taiwan/modelling/large-scale/hydro/model/GRAPHIQUES/KUNSHEN-RIVERS-001/basic-processing/regular-grid\"

# Time parameters
startTime=\"2011-09-01T12:00:00\"
endTime=\"2011-09-01T12:00:05\"

# Grid vertical information
bottomLevel=0
middleLevel=19
surfaceLevel=39

# Mesh size parameters
longCenter=120.104575
latCenter=23.135639
ratioLine=3

# Interpolation parameters
searchRadius=\"1.2k\"
sector=\"4/2\"

# Variables to extract
bathy=1
meshSize=1
ssh=0
surfaceTemperature=0
surfaceSalinity=0
surfaceCurrent=0
middleCurrent=0
bottomCurrent=0
barotropicCurrent=0

# Optional
Xincr=0.025k
Yincr=0.025k
#Xmin=121.30000
#Xmax=122.166667
#Ymin=23.05
#Ymax=23.500000"

	exit 1
fi

# 1. Import config file

basedir="${0%/*}"
source $basedir/$1

# 2. Check config file

#scanDir
if [[ ! -n "$scanDir" ]] 
then
	path=`pwd`
else
	path=$scanDir
fi

#outDir
if [[ ! -n "$outDir" ]] 
then
	echo "Please define 'outDir' variable. Abort"
	exit
else
	mkdir -p $outDir
fi

#startTime
if [[ ! -n "$startTime" ]] 
then
	echo "Please define 'startTime' variable. Abort"
	exit
fi

workingDir=`mktemp -d`
#make a file of the tmp dir
workingDirFile=`echo "$workingDir" | sed -r 's/\//a/g'`
touch $workingDirFile

if [ ! -f ${path}/grille.nc ]
then
	echo "The file grille.nc doesn't exist"
    exit 1
fi

# 2. Extract the grid
source $basedir/../extract_S_grid/extract_S_grid.sh

# Copy compute distance routine
cp ../lib/grid_rotator_vectors.exe ${workingDir}/.

# Calculate start time in seconds
parsedStartTime="${startTime:0:4}-${startTime:5:2}-${startTime:8:2} ${startTime:11:2}:${startTime:14:2}:${startTime:17:2}"
startSecondTime=`date -u --date="$parsedStartTime" "+%s"`

# Calculate end time in seconds
parsedEndTime="${endTime:0:4}-${endTime:5:2}-${endTime:8:2} ${endTime:11:2}:${endTime:14:2}:${endTime:17:2}"
endSecondTime=`date -u --date="$parsedEndTime" "+%s"`

# Extract from the grid
if test $bathy -eq 1
then
	grd2xyz ${path}/grille.nc?h_w > ${workingDir}/data
	join ${workingDir}/grid_t.xy ${workingDir}/data > ${workingDir}/joined1.xyz	
	join ${workingDir}/joined1.xyz ${workingDir}/dxdy_t.xyz > ${workingDir}/joined.xyz	
	awk '{ print  $3" "$5" "$7" "$13}' ${workingDir}/joined.xyz > ${workingDir}/data.xyz	
	nearneighbor ${workingDir}/data.xyz $envelope_grid_t -I${Xincr_grid_t}/${Yincr_grid_t} -S${searchRadius} -N${sector} -W -G${outDir}/bathy.grd

	rm -f ${workingDir}/data
	rm -f ${workingDir}/joined.xyz ${workingDir}/joined1.xyz
	rm -f ${workingDir}/data.xyz 	
fi	

if test $mask -eq 1
then
	grd2xyz ${path}/grille.nc?mask_t > ${workingDir}/data
	join ${workingDir}/grid_t.xy ${workingDir}/data > ${workingDir}/joined1.xyz	
	join ${workingDir}/joined1.xyz ${workingDir}/dxdy_t.xyz > ${workingDir}/joined.xyz	
	awk '{ print  $3" "$5" "$7" "$13}' ${workingDir}/joined.xyz > ${workingDir}/data.xyz	
	nearneighbor ${workingDir}/data.xyz $envelope_grid_t -I${Xincr_grid_t}/${Yincr_grid_t} -S${searchRadius} -N${sector} -W -G${outDir}/mask_t.grd

	rm -f ${workingDir}/data
	rm -f ${workingDir}/joined.xyz ${workingDir}/joined1.xyz
	rm -f ${workingDir}/data.xyz 	
fi

if test $meshSize -eq 1
then

	if [[ -f ${path}/grid.nc ]]
	then
		# Extract the data (sqrt_dxdy)
		grd2xyz ${path}/grid.nc?sqrt_dxdy > ${workingDir}/sqrt_dxdy
		join ${workingDir}/grid_t.xy ${workingDir}/sqrt_dxdy > ${workingDir}/joined1.xyz
		join ${workingDir}/joined1.xyz ${workingDir}/dxdy_t.xyz > ${workingDir}/joined.xyz	
		awk '{ print  $3" "$5" "$7" "$13}' ${workingDir}/joined.xyz > ${workingDir}/sqrt_dxdy.xyz		
		rm -f ${workingDir}/joined.xyz  ${workingDir}/joined1.xyz

		# Compute MinMax
		gmtinfo -C ${workingDir}/sqrt_dxdy.xyz > ${workingDir}/minmax
		Zmin=`cat ${workingDir}/minmax | cut -f "5"`
		Zmax=`cat ${workingDir}/minmax | cut -f "6"`

		# Interpole data	
		nearneighbor ${workingDir}/sqrt_dxdy.xyz $envelope_grid_t -I${Xincr_grid_t}/${Yincr_grid_t} -S${searchRadius} -N${sector} -W -G${outDir}/sqrt_dxdy.grd
	
		# Compute radius line
		grepZ=`echo $Zmax | cut -d'.' -f"1"`
		cat ${workingDir}/sqrt_dxdy.xyz | grep "$grepZ\." > ${workingDir}/large_circle.xyz

		nbLine=`wc -l ${workingDir}/large_circle.xyz | cut -d" " -f "1"`	
	
		lineCount=$[($ratioLine*$nbLine)/100]
	
		awk '{if(NR%'$lineCount' == 0) 
		     {	printf("%s %s %s\n",$1,$2,$3);     
			printf("%s %s %s\n",'$longCenter','$latCenter',0);   
		     }}' ${workingDir}/large_circle.xyz > ${outDir}/radius.xyz	

		rm -f ${workingDir}/data
		rm -f ${workingDir}/joined.xyz
		rm -f ${workingDir}/data.xyz 

	else
		echo "Mesh size requires grid.nc"
	fi
		
fi

function var2d_t {
	join ${workingDir}/grid_t.xy ${workingDir}/data > ${workingDir}/joined1.xyz
	join ${workingDir}/joined1.xyz ${workingDir}/dxdy_t.xyz > ${workingDir}/joined.xyz	
	awk '{ print  $3" "$5" "$7" "$13}' ${workingDir}/joined.xyz > ${workingDir}/data.xyz
	nearneighbor ${workingDir}/data.xyz $envelope_grid_t -I${Xincr_grid_t}/${Yincr_grid_t} -S${searchRadius} -N${sector} -W -G${workingDir}/${filename}-${var}.nc

	#add variable time and set time with current time step	
	ncecat -h -O -u time ${workingDir}/${filename}-${var}.nc ${workingDir}/${filename}-${var}.nc
	ncap2 -h -O -s "time[time]={${currentSecondTime}};" ${workingDir}/${filename}-${var}.nc ${workingDir}/${filename}-${var}.nc		
	#add meta data on time variable
	ncatted -h -a calendar,time,c,c,"gregorian" ${workingDir}/${filename}-${var}.nc
	ncatted -h -a long_name,time,c,c,"time" ${workingDir}/${filename}-${var}.nc
	ncatted -h -a units,time,c,c,"seconds since 1970-01-01 00:00:00" ${workingDir}/${filename}-${var}.nc

	#we add to the pool
	if [[ ! -f "${outDir}/${var}.nc" ]] 
	then
		mv ${workingDir}/${filename}-${var}.nc ${outDir}/${var}.nc
	else
		ncrcat -h -O ${outDir}/${var}.nc ${workingDir}/${filename}-${var}.nc -o ${outDir}/${var}.nc
	fi

	rm -f ${workingDir}/data
	rm -f ${workingDir}/joined.xyz ${workingDir}/joined1.xyz
	rm -f ${workingDir}/data.xyz 
}

function vector2d {
	`cd ${workingDir}/ && ${workingDir}/grid_rotator_vectors.exe ${Xsize_grid_t} ${Ysize_grid_t}`
	#Interpolates
	nearneighbor ${workingDir}/vel_u_ew  $envelope_grid_t -I${Xincr_grid_t}/${Yincr_grid_t} -S${searchRadius} -N${sector} -G${workingDir}/${filename}-${var}.nc
	ncrename -h -v z,u ${workingDir}/${filename}-${var}.nc
        nearneighbor ${workingDir}/vel_v_ns $envelope_grid_t -I${Xincr_grid_t}/${Yincr_grid_t} -S${searchRadius} -N${sector} -G${workingDir}/${filename}-${var}_v.nc
	ncrename -h -v z,v ${workingDir}/${filename}-${var}_v.nc

	ncks -h -A ${workingDir}/${filename}-${var}_v.nc ${workingDir}/${filename}-${var}.nc

	#add variable time and set time with current time step	
	ncecat -h -O -u time ${workingDir}/${filename}-${var}.nc ${workingDir}/${filename}-${var}.nc
	ncap2 -h -O -s "time[time]={${currentSecondTime}};" ${workingDir}/${filename}-${var}.nc ${workingDir}/${filename}-${var}.nc		
	#add meta data on time variable
	ncatted -h -a calendar,time,c,c,"gregorian" ${workingDir}/${filename}-${var}.nc
	ncatted -h -a long_name,time,c,c,"time" ${workingDir}/${filename}-${var}.nc
	ncatted -h -a units,time,c,c,"seconds since 1970-01-01 00:00:00" ${workingDir}/${filename}-${var}.nc

	#we add to the pool
	if [[ ! -f "${outDir}/${var}.nc" ]] 
	then
		mv ${workingDir}/${filename}-${var}.nc ${outDir}/${var}.nc
	else
		ncrcat -h -O ${outDir}/${var}.nc ${workingDir}/${filename}-${var}.nc -o ${outDir}/${var}.nc
	fi

	rm -f ${workingDir}/vel_u  ${workingDir}/vel_u_ew ${workingDir}/vel_v ${workingDir}/vel_v_ns ${workingDir}/${filename}-${var}_v.nc
	rm -f ${workingDir}/joined.xyz
	rm -f ${workingDir}/data.xyz 	
}

# 4. Scan file directory
for infile in ${path}/*.nc; do 

	file=$(basename "$infile")
	filename="${file%.*}"	

	if [[ "$filename" == "grille" ]]
	then
		# we skip the grille file
		continue
	fi
	
	parsedTime="${filename:0:4}-${filename:4:2}-${filename:6:2} ${filename:9:2}:${filename:11:2}:${filename:13:2}"	
	currentSecondTime=`date -u --date="$parsedTime" "+%s"`		
	
	if [[ $currentSecondTime < $startSecondTime || $currentSecondTime > $endSecondTime ]]
	then
		# we skip this date 		   
		continue
	fi   

	echo "Current file : $filename"

	parsedTime="${filename:0:4}-${filename:4:2}-${filename:6:2}T${filename:9:2}:${filename:11:2}:${filename:13:2}"	

	if test $ssh -eq 1
	then

		var="sea-surface-height"

		grd2xyz ${infile}?ssh > ${workingDir}/data

		var2d_t;
		
	fi

	if test $ib -eq 1
	then

		var="inverse-barometer"

		grd2xyz ${infile}?barometre_inverse > ${workingDir}/data

		var2d_t;
		
	fi

	if test $hs -eq 1
	then

		var="hs-wave"

		grd2xyz ${infile}?hs_wave_t > ${workingDir}/data

		var2d_t;
		
	fi

	if test $surfaceTemperature -eq 1
	then

		var="sea-surface-temperature"

		grd2xyz ${infile}?tem[0,$surfaceLevel] > ${workingDir}/data

		var2d_t;
		
	fi

	if test $surfaceSalinity -eq 1
	then

		var="sea-surface-salinity"

		grd2xyz ${infile}?sal[0,$surfaceLevel] > ${workingDir}/data

		var2d_t;
		
	fi	

	if test $surfaceCurrent -eq 1
	then

		var="surface-current"

		grd2xyz ${infile}?vel_u[0,$surfaceLevel] > ${workingDir}/vel_u
		grd2xyz ${infile}?vel_v[0,$surfaceLevel] > ${workingDir}/vel_v

		vector2d;	
	fi	

	if test $middleCurrent -eq 1
	then

		var="middle-current"

		grd2xyz ${infile}?vel_u[0,$middleLevel] > ${workingDir}/vel_u
		grd2xyz ${infile}?vel_v[0,$middleLevel] > ${workingDir}/vel_v

		vector2d;		
	fi	

	if test $bottomCurrent -eq 1
	then

		var="bottom-current"

		grd2xyz ${infile}?vel_u[0,$bottomLevel] > ${workingDir}/vel_u
		grd2xyz ${infile}?vel_v[0,$bottomLevel] > ${workingDir}/vel_v

		vector2d; 		
	fi
	
	if test $barotropicCurrent -eq 1
	then

		var="barotropic-current"

		grd2xyz ${infile}?velbar_u-velbarobc_u > ${workingDir}/vel_u
		grd2xyz ${infile}?velbar_v_velbarobc_v > ${workingDir}/vel_v

		vector2d;	
	fi

	if test $windStress -eq 1
	then

		var="wind-stress"

		grd2xyz ${infile}?wstress_u > ${workingDir}/vel_u
		grd2xyz ${infile}?wstress_v > ${workingDir}/vel_v

		vector2d;	
	fi
	
	if test $two -eq 1
	then

		var="two"

		grd2xyz ${infile}?twox > ${workingDir}/vel_u
		grd2xyz ${infile}?twoy > ${workingDir}/vel_v

		vector2d;	
	fi
	
	if test $taw -eq 1
	then

		var="taw"

		grd2xyz ${infile}?tawx > ${workingDir}/vel_u
		grd2xyz ${infile}?tawy > ${workingDir}/vel_v

		vector2d;	
	fi
	
	if test $twoSubTaw -eq 1
	then

		var="two-taw"

		grd2xyz ${infile}?twox-tawx > ${workingDir}/vel_u
		grd2xyz ${infile}?twoy-tawy > ${workingDir}/vel_v

		vector2d;	
	fi	

done

rm -rf ${workingDir} ${workingDirFile}
