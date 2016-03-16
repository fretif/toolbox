#!/bin/bash

#################
#	CONFIG File	#
#################

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

# 1. Set environement
workingDir=`mktemp -d`

# Copy compute distance routine
cp ../lib/compute_distance.exe ${workingDir}/.
# Copy compute distance routine
cp ../lib/grid_rotator_vectors.exe ${workingDir}/.

# 2. Extract the grid
source $basedir/../extract_S_grid/extract_S_grid.sh

# Calculate start time in seconds
parsedStartTime="${startTime:0:4}-${startTime:5:2}-${startTime:8:2} ${startTime:11:2}:${startTime:14:2}:${startTime:17:2}"
startSecondTime=`date --date="$parsedStartTime" "+%s"`

# Calculate end time in seconds
parsedEndTime="${endTime:0:4}-${endTime:5:2}-${endTime:8:2} ${endTime:11:2}:${endTime:14:2}:${endTime:17:2}"
endSecondTime=`date --date="$parsedEndTime" "+%s"`

echo "$long	$lat" > ${workingDir}/coord.xy

rotationAngle=`echo $rotationAngle + 90| bc`

previousTime=0

if test $nearestPointDetail -eq 1
then
	echo "->Nearest point detail..."
	var="point-detail"	
	outfile=${outDir}"${var}_${positionName}.xy"

	echo "Depth" > ${outfile}

	grd2xyz ${scanDir}/grille.nc?h_w > ${workingDir}/data
	join ${workingDir}/grid_t.xy ${workingDir}/data > ${workingDir}/joined.xyz
	awk '{ print  $3" "$5" "$7}' ${workingDir}/joined.xyz > ${workingDir}/data.xyz
	
	# We compute distance between points and we select the nearest
	# The routine return 0,0,0 if not nearest point was found
	`cd ${workingDir}/ && ${workingDir}/compute_distance.exe >> ${outfile}`
	
	rm -f ${workingDir}/data
	rm -f ${workingDir}/joined.xyz
	rm -f ${workingDir}/data.xyz

	echo "Horizontal cell surface" >> ${outfile}

	awk '{ print  $3" "$5" "$7}' ${workingDir}/dxdy_t.xyz > ${workingDir}/data.xyz
	
	# We compute distance between points and we select the nearest
	# The routine return 0,0,0 if not nearest point was found
	`cd ${workingDir}/ && ${workingDir}/compute_distance.exe >> ${outfile}`	
	
	rm -f ${workingDir}/data.xyz 

	if [ -f ${scanDir}/grid.nc ]
	then

		echo "Horizontal cell size" >> ${outfile}	

		grd2xyz ${scanDir}/grid.nc?sqrt_dxdy > ${workingDir}/sqrt_dxdy
		join ${workingDir}/grid_t.xy ${workingDir}/sqrt_dxdy > ${workingDir}/joined.xyz		
		awk '{ print  $3" "$5" "$7}' ${workingDir}/joined.xyz > ${workingDir}/data.xyz	
		
		# We compute distance between points and we select the nearest
		# The routine return 0,0,0 if not nearest point was found
		`cd ${workingDir}/ && ${workingDir}/compute_distance.exe >> ${outfile}`	
		
		rm -f ${workingDir}/joined.xyz
		rm -f ${workingDir}/data.xyz			

	fi

fi

# 3. Scan Symphonie Output Dir
for infile in ${scanDir}/*.nc; do 

	file=$(basename "$infile")
	filename="${file%.*}"	

	if [[ "$filename" == "grille" ]]
	then
		# we skip the grille file
		continue
	fi
	
	parsedTime="${filename:0:4}-${filename:4:2}-${filename:6:2} ${filename:9:2}:${filename:11:2}:${filename:13:2}"	
	currentTime=`date --date="$parsedTime" "+%d %B %Y - %H:%M:%S"`
	currentSecondTime=`date --date="$parsedTime" "+%s"`	
	
	if [[ $currentSecondTime == $previousTime || $currentSecondTime < $startSecondTime || $currentSecondTime > $endSecondTime ]]
	then
		# we skip this date 				   
		continue
	fi  

	previousTime=$currentSecondTime  

	echo "Current file : $filename"

	parsedTime="${filename:0:4}-${filename:4:2}-${filename:6:2}T${filename:9:2}:${filename:11:2}:${filename:13:2}"	

	if test $ssh -eq 1
	then

		echo "->Sea surface height..."
		var="ssh_w"	
		outfile=${outDir}"track_${var}_${positionName}.xy"

		grd2xyz ${infile}?${var} > ${workingDir}/data
		join ${workingDir}/grid_t.xy ${workingDir}/data > ${workingDir}/joined.xyz
		awk '{ print  $3" "$5" "$7}' ${workingDir}/joined.xyz > ${workingDir}/data.xyz

		# Old version, we use the gmt interpolation
		#xyz2grd data.xyz $envelope -I${Xsize}+/${Ysize}+ -Ggrid.grd
		#nearneighbor ${workingDir}/data.xyz $envelope -I${Xsize}+/${Ysize}+ -S6k -N4/1 -G${workingDir}/data.grd		
		#grdtrack ${workingDir}/coord.xy -G${workingDir}/data.grd > ${workingDir}/point.xy
	
		# We compute distance between points and we select the nearest
		# The routine return 0,0,0 if not nearest point was found
		`cd ${workingDir}/ && ${workingDir}/compute_distance.exe > ${workingDir}/point.xy`		
	
		if [ $printNearestPointCoordinate -eq 1 ] 
		then
			cat ${workingDir}/point.xy		
		fi		

		awk '{print "'$parsedTime'\t"$3}' ${workingDir}/point.xy >> $outfile

		rm -f ${workingDir}/data
		rm -f ${workingDir}/joined.xyz
		rm -f ${workingDir}/data.xyz 
		rm -f ${workingDir}/point.xy

	fi

	if test $surfaceTemperature -eq 1
	then

		echo "->Sea surface temperature..."
		var="tem"	
		outfile=${outDir}"track_${var}_${positionName}.xy"

		grd2xyz ${infile}?${var}[0,$surfaceLevel] > ${workingDir}/data
		join ${workingDir}/grid_t.xy ${workingDir}/data > ${workingDir}/joined.xyz
		awk '{ print  $3" "$5" "$7}' ${workingDir}/joined.xyz > ${workingDir}/data.xyz

		# We compute distance between points and we select the nearest
		# The routine return 0,0,0 if not nearest point was found
		`cd ${workingDir}/ && ${workingDir}/compute_distance.exe > ${workingDir}/point.xy`		
	
		if [ $printNearestPointCoordinate -eq 1 ] 
		then
			cat ${workingDir}/point.xy		
		fi		

		awk '{print "'$parsedTime'\t"$3}' ${workingDir}/point.xy >> $outfile

		rm -f ${workingDir}/data
		rm -f ${workingDir}/joined.xyz
		rm -f ${workingDir}/data.xyz 
		rm -f ${workingDir}/point.xy

	fi

	if test $barotropicCurrent -eq 1
	then
		echo "->Barotropic current..."	
	
		grd2xyz ${infile}?velbar_u-velbarobc_u > ${workingDir}/vel_u
		grd2xyz ${infile}?velbar_v_velbarobc_v > ${workingDir}/vel_v

		`cd ${workingDir}/ && ${workingDir}/grid_rotator_vectors.exe ${Xsize_grid_t} ${Ysize_grid_t}`

		#extract u component from grid
		mv ${workingDir}/vel_u_ew ${workingDir}/data.xyz	

		`cd ${workingDir}/ && ${workingDir}/compute_distance.exe > ${workingDir}/point.xy`		
	
		if [ $printNearestPointCoordinate -eq 1 ] 
		then
			cat ${workingDir}/point.xy		
		fi

		awk '{print $3}' ${workingDir}/point.xy >> ${workingDir}/point_u.xy
		current_u=${workingDir}/point_u.xy

		rm -f ${workingDir}/point.xy

		#extract v component from grid
		mv ${workingDir}/vel_v_ns ${workingDir}/data.xyz

		`cd ${workingDir}/ && ${workingDir}/compute_distance.exe > ${workingDir}/point.xy`

		awk '{print $3}' ${workingDir}/point.xy >> ${workingDir}/point_v.xy
		current_v=${workingDir}/point_v.xy

		rm -f ${workingDir}/vel_u  ${workingDir}/vel_u_ew ${workingDir}/vel_v ${workingDir}/vel_v_ns 
		rm -f ${workingDir}/joined.xyz ${workingDir}/point.xy
		rm -f ${workingDir}/data.xyz 	

		# speed
		var="barotropic-current_speed"	
		outfile=${outDir}"track_${var}_${positionName}.xy"
		
		gmtmath $current_u SQR $current_v SQR ADD SQRT = ${workingDir}/speed.xyz
		awk '{print "'$parsedTime'\t"$1}' ${workingDir}/speed.xyz >> $outfile	

		# direction
		var="barotropic-current_dir"
		outfile=${outDir}"track_${var}_${positionName}.xy"

		#vector component to angle
		gmtmath $current_u $current_v ATAN2 = ${workingDir}/dir.xyz
		#rad to deg
		gmtmath ${workingDir}/dir.xyz R2D 180 ADD = ${workingDir}/dir_deg.xyz		

		awk '{print "'$parsedTime'\t"$1}' ${workingDir}/dir_deg.xyz >> $outfile	
		
		rm -f ${workingDir}/point_u.xy
		rm -f ${workingDir}/point_v.xy
		
	fi

	if test $surfaceCurrent -eq 1
	then

		echo "->Surface current..." 
		
		grd2xyz ${infile}?vel_u[0,$surfaceLevel] > ${workingDir}/vel_u
		grd2xyz ${infile}?vel_v[0,$surfaceLevel] > ${workingDir}/vel_v

		`cd ${workingDir}/ && ${workingDir}/grid_rotator_vectors.exe ${Xsize_grid_t} ${Ysize_grid_t}`

		#extract u component from grid
		mv ${workingDir}/vel_u_ew ${workingDir}/data.xyz	

		`cd ${workingDir}/ && ${workingDir}/compute_distance.exe > ${workingDir}/point.xy`		
	
		if [ $printNearestPointCoordinate -eq 1 ] 
		then
			cat ${workingDir}/point.xy		
		fi

		awk '{print $3}' ${workingDir}/point.xy >> ${workingDir}/point_u.xy
		current_u=${workingDir}/point_u.xy

		rm -f ${workingDir}/point.xy

		#extract v component from grid
		mv ${workingDir}/vel_v_ns ${workingDir}/data.xyz

		`cd ${workingDir}/ && ${workingDir}/compute_distance.exe > ${workingDir}/point.xy`

		awk '{print $3}' ${workingDir}/point.xy >> ${workingDir}/point_v.xy
		current_v=${workingDir}/point_v.xy

		rm -f ${workingDir}/vel_u  ${workingDir}/vel_u_ew ${workingDir}/vel_v ${workingDir}/vel_v_ns 
		rm -f ${workingDir}/joined.xyz ${workingDir}/point.xy
		rm -f ${workingDir}/data.xyz

		# speed
		var="surface-current_speed"	
		outfile=${outDir}"track_${var}_${positionName}.xy"
		
		gmtmath ${current_u} SQR ${current_v} SQR ADD SQRT = ${workingDir}/speed.xyz
		awk '{print "'$parsedTime'\t"$1}' ${workingDir}/speed.xyz >> $outfile		

		# direction
		var="surface-current_dir"
		outfile=${outDir}"track_${var}_${positionName}.xy"

		#vector component to angle
		gmtmath $current_u $current_v ATAN2 = ${workingDir}/dir.xyz
		#rad to deg
		gmtmath ${workingDir}/dir.xyz R2D 180 ADD = ${workingDir}/dir_deg.xyz		

		awk '{print "'$parsedTime'\t"$1}' ${workingDir}/dir_deg.xyz >> $outfile	
		
		rm -f ${workingDir}/point_u.xy
		rm -f ${workingDir}/point_v.xy
		rm -f ${workingDir}/speed.xyz ${workingDir}/dir.xyz ${workingDir}/dir_deg.xyz
		
	fi	

	if test $middleCurrent -eq 1
	then
		echo "->Middle current..."
	
		grd2xyz ${infile}?vel_u[0,$middleLevel] > ${workingDir}/vel_u
		grd2xyz ${infile}?vel_v[0,$middleLevel] > ${workingDir}/vel_v

		`cd ${workingDir}/ && ${workingDir}/grid_rotator_vectors.exe ${Xsize_grid_t} ${Ysize_grid_t}`

		#extract u component from grid
		mv ${workingDir}/vel_u_ew ${workingDir}/data.xyz	

		`cd ${workingDir}/ && ${workingDir}/compute_distance.exe > ${workingDir}/point.xy`		
	
		if [ $printNearestPointCoordinate -eq 1 ] 
		then
			cat ${workingDir}/point.xy		
		fi

		awk '{print $3}' ${workingDir}/point.xy >> ${workingDir}/point_u.xy
		current_u=${workingDir}/point_u.xy

		rm -f ${workingDir}/point.xy

		#extract v component from grid
		mv ${workingDir}/vel_v_ns ${workingDir}/data.xyz

		`cd ${workingDir}/ && ${workingDir}/compute_distance.exe > ${workingDir}/point.xy`

		awk '{print $3}' ${workingDir}/point.xy >> ${workingDir}/point_v.xy
		current_v=${workingDir}/point_v.xy

		rm -f ${workingDir}/vel_u  ${workingDir}/vel_u_ew ${workingDir}/vel_v ${workingDir}/vel_v_ns 
		rm -f ${workingDir}/joined.xyz ${workingDir}/point.xy
		rm -f ${workingDir}/data.xyz
		
		# speed
		var="middle-current_speed"	
		outfile=${outDir}"track_${var}_${positionName}.xy"
		
		gmtmath ${current_u} SQR ${current_v} SQR ADD SQRT = ${workingDir}/speed.xyz
		awk '{print "'$parsedTime'\t"$1}' ${workingDir}/speed.xyz >> $outfile		

		# direction
		var="middle-current_dir"
		outfile=${outDir}"track_${var}_${positionName}.xy"

		#vector component to angle
		gmtmath $current_u $current_v ATAN2 = ${workingDir}/dir.xyz
		#rad to deg
		gmtmath ${workingDir}/dir.xyz R2D 180 ADD = ${workingDir}/dir_deg.xyz		

		awk '{print "'$parsedTime'\t"$1}' ${workingDir}/dir_deg.xyz >> $outfile	
		
		rm -f ${workingDir}/point_u.xy
		rm -f ${workingDir}/point_v.xy
		rm -f ${workingDir}/speed.xyz ${workingDir}/dir.xyz ${workingDir}/dir_deg.xyz
				
	fi	

	if test $bottomCurrent -eq 1
	then
		echo "->Bottom current..."

		grd2xyz ${infile}?vel_u[0,$bottomLevel] > ${workingDir}/vel_u
		grd2xyz ${infile}?vel_v[0,$bottomLevel] > ${workingDir}/vel_v

		`cd ${workingDir}/ && ${workingDir}/grid_rotator_vectors.exe ${Xsize_grid_t} ${Ysize_grid_t}`

		#extract u component from grid
		mv ${workingDir}/vel_u_ew ${workingDir}/data.xyz	

		`cd ${workingDir}/ && ${workingDir}/compute_distance.exe > ${workingDir}/point.xy`		
	
		if [ $printNearestPointCoordinate -eq 1 ] 
		then
			cat ${workingDir}/point.xy		
		fi

		awk '{print $3}' ${workingDir}/point.xy >> ${workingDir}/point_u.xy
		current_u=${workingDir}/point_u.xy

		rm -f ${workingDir}/point.xy

		#extract v component from grid
		mv ${workingDir}/vel_v_ns ${workingDir}/data.xyz

		`cd ${workingDir}/ && ${workingDir}/compute_distance.exe > ${workingDir}/point.xy`

		awk '{print $3}' ${workingDir}/point.xy >> ${workingDir}/point_v.xy
		current_v=${workingDir}/point_v.xy

		rm -f ${workingDir}/vel_u  ${workingDir}/vel_u_ew ${workingDir}/vel_v ${workingDir}/vel_v_ns 
		rm -f ${workingDir}/joined.xyz ${workingDir}/point.xy
		rm -f ${workingDir}/data.xyz
		
		# speed
		var="bottom-current_speed"	
		outfile=${outDir}"track_${var}_${positionName}.xy"
		
		gmtmath ${current_u} SQR ${current_v} SQR ADD SQRT = ${workingDir}/speed.xyz
		awk '{print "'$parsedTime'\t"$1}' ${workingDir}/speed.xyz >> $outfile		

		# direction
		var="bottom-current_dir"
		outfile=${outDir}"track_${var}_${positionName}.xy"

		#vector component to angle
		gmtmath $current_u $current_v ATAN2 = ${workingDir}/dir.xyz
		#rad to deg
		gmtmath ${workingDir}/dir.xyz R2D 180 ADD = ${workingDir}/dir_deg.xyz		

		awk '{print "'$parsedTime'\t"$1}' ${workingDir}/dir_deg.xyz >> $outfile	
		
		rm -f ${workingDir}/point_u.xy
		rm -f ${workingDir}/point_v.xy
		rm -f ${workingDir}/speed.xyz ${workingDir}/dir.xyz ${workingDir}/dir_deg.xyz
				
	fi

	if test $windStress -eq 1
	then

		echo "->Wind stress..." 
		
		grd2xyz ${infile}?wstress_u[0] > ${workingDir}/vel_u
		grd2xyz ${infile}?wstress_v[0] > ${workingDir}/vel_v

		`cd ${workingDir}/ && ${workingDir}/grid_rotator_vectors.exe ${Xsize_grid_t} ${Ysize_grid_t}`

		#extract u component from grid
		mv ${workingDir}/vel_u_ew ${workingDir}/data.xyz	

		`cd ${workingDir}/ && ${workingDir}/compute_distance.exe > ${workingDir}/point.xy`		
	
		if [ $printNearestPointCoordinate -eq 1 ] 
		then
			cat ${workingDir}/point.xy		
		fi

		awk '{print $3}' ${workingDir}/point.xy >> ${workingDir}/point_u.xy
		current_u=${workingDir}/point_u.xy

		rm -f ${workingDir}/point.xy

		#extract v component from grid
		mv ${workingDir}/vel_v_ns ${workingDir}/data.xyz

		`cd ${workingDir}/ && ${workingDir}/compute_distance.exe > ${workingDir}/point.xy`

		awk '{print $3}' ${workingDir}/point.xy >> ${workingDir}/point_v.xy
		current_v=${workingDir}/point_v.xy

		rm -f ${workingDir}/vel_u  ${workingDir}/vel_u_ew ${workingDir}/vel_v ${workingDir}/vel_v_ns 
		rm -f ${workingDir}/joined.xyz ${workingDir}/point.xy
		rm -f ${workingDir}/data.xyz

		# speed
		var="wind-stress_speed"	
		outfile=${outDir}"track_${var}_${positionName}.xy"
		
		gmtmath ${current_u} SQR ${current_v} SQR ADD SQRT = ${workingDir}/speed.xyz
		awk '{print "'$parsedTime'\t"$1}' ${workingDir}/speed.xyz >> $outfile		

		# direction
		var="wind-stress_dir"
		outfile=${outDir}"track_${var}_${positionName}.xy"

		#vector component to angle
		gmtmath $current_u $current_v ATAN2 = ${workingDir}/dir.xyz
		#rad to deg
		gmtmath ${workingDir}/dir.xyz R2D 180 ADD = ${workingDir}/dir_deg.xyz		

		awk '{print "'$parsedTime'\t"$1}' ${workingDir}/dir_deg.xyz >> $outfile	
		
		rm -f ${workingDir}/point_u.xy
		rm -f ${workingDir}/point_v.xy
		rm -f ${workingDir}/speed.xyz ${workingDir}/dir.xyz ${workingDir}/dir_deg.xyz
		
	fi

	if test $hs -eq 1
	then

		echo "->Wave significant height..."
		var="hs_wave_t"	
		outfile=${outDir}"track_${var}_${positionName}.xy"

		grd2xyz ${infile}?${var} > ${workingDir}/data
		join ${workingDir}/grid_t.xy ${workingDir}/data > ${workingDir}/joined.xyz
		awk '{ print  $3" "$5" "$7}' ${workingDir}/joined.xyz > ${workingDir}/data.xyz

		# Old version, we use the gmt interpolation
		#xyz2grd data.xyz $envelope -I${Xsize}+/${Ysize}+ -Ggrid.grd
		#nearneighbor ${workingDir}/data.xyz $envelope -I${Xsize}+/${Ysize}+ -S6k -N4/1 -G${workingDir}/data.grd		
		#grdtrack ${workingDir}/coord.xy -G${workingDir}/data.grd > ${workingDir}/point.xy
	
		# We compute distance between points and we select the nearest
		# The routine return 0,0,0 if not nearest point was found
		`cd ${workingDir}/ && ${workingDir}/compute_distance.exe > ${workingDir}/point.xy`		
	
		if [ $printNearestPointCoordinate -eq 1 ] 
		then
			cat ${workingDir}/point.xy		
		fi		

		awk '{print "'$parsedTime'\t"$3}' ${workingDir}/point.xy >> $outfile

		rm -f ${workingDir}/data
		rm -f ${workingDir}/joined.xyz
		rm -f ${workingDir}/data.xyz 
		rm -f ${workingDir}/point.xy

	fi	

	if test $waveDir -eq 1
	then

		echo "->Wave direction..."
		var="dir_wave_t"	
		outfile=${outDir}"track_${var}_${positionName}.xy"

		grd2xyz ${infile}?${var} > ${workingDir}/data
		join ${workingDir}/grid_t.xy ${workingDir}/data > ${workingDir}/joined.xyz
		awk '{ print  $3" "$5" "$7}' ${workingDir}/joined.xyz > ${workingDir}/data.xyz

		# Old version, we use the gmt interpolation
		#xyz2grd data.xyz $envelope -I${Xsize}+/${Ysize}+ -Ggrid.grd
		#nearneighbor ${workingDir}/data.xyz $envelope -I${Xsize}+/${Ysize}+ -S6k -N4/1 -G${workingDir}/data.grd		
		#grdtrack ${workingDir}/coord.xy -G${workingDir}/data.grd > ${workingDir}/point.xy
	
		# We compute distance between points and we select the nearest
		# The routine return 0,0,0 if not nearest point was found
		`cd ${workingDir}/ && ${workingDir}/compute_distance.exe > ${workingDir}/point.xy`		
	
		if [ $printNearestPointCoordinate -eq 1 ] 
		then
			cat ${workingDir}/point.xy		
		fi		

		awk '{print "'$parsedTime'\t"$3}' ${workingDir}/point.xy >> $outfile

		rm -f ${workingDir}/data
		rm -f ${workingDir}/joined.xyz
		rm -f ${workingDir}/data.xyz 
		rm -f ${workingDir}/point.xy

	fi

	if test $wavePeriod -eq 1
	then

		echo "->Wave period..."
		var="t_wave_t"	
		outfile=${outDir}"track_${var}_${positionName}.xy"

		grd2xyz ${infile}?${var} > ${workingDir}/data
		join ${workingDir}/grid_t.xy ${workingDir}/data > ${workingDir}/joined.xyz
		awk '{ print  $3" "$5" "$7}' ${workingDir}/joined.xyz > ${workingDir}/data.xyz

		# Old version, we use the gmt interpolation
		#xyz2grd data.xyz $envelope -I${Xsize}+/${Ysize}+ -Ggrid.grd
		#nearneighbor ${workingDir}/data.xyz $envelope -I${Xsize}+/${Ysize}+ -S6k -N4/1 -G${workingDir}/data.grd		
		#grdtrack ${workingDir}/coord.xy -G${workingDir}/data.grd > ${workingDir}/point.xy
	
		# We compute distance between points and we select the nearest
		# The routine return 0,0,0 if not nearest point was found
		`cd ${workingDir}/ && ${workingDir}/compute_distance.exe > ${workingDir}/point.xy`		
	
		if [ $printNearestPointCoordinate -eq 1 ] 
		then
			cat ${workingDir}/point.xy		
		fi		

		awk '{print "'$parsedTime'\t"$3}' ${workingDir}/point.xy >> $outfile

		rm -f ${workingDir}/data
		rm -f ${workingDir}/joined.xyz
		rm -f ${workingDir}/data.xyz 
		rm -f ${workingDir}/point.xy

	fi
done

rm -rf ${workingDir}
