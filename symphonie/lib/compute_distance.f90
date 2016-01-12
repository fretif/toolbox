program toto
use ieee_arithmetic
implicit none
double precision rayonterre,pi,lat1,lon1,lat2,lon2,dLat,dLon,a,c,d,lon_,lat_,h_
double precision cellSize,myLatPoint,myLongPoint,minDistance,nearestLatPoint,nearestLongPoint,nearestValuePoint
character filename*100

rayonterre=6370949.00000
pi=acos(-1.)

open(unit=3,file=trim("coord.xy"))
read(3,*,end=103)myLongPoint,myLatPoint	
103 close(3)

minDistance=10000000
nearestLatPoint=0
nearestLongPoint=0
nearestValuePoint=0

filename="data.xyz"

lat1=myLatPoint*pi/180   
lon1=myLongPoint*pi/180

open(unit=3,file=trim(filename))
101 read(3,*,end=100)lon_,lat_,h_	

	if( .NOT. ieee_is_nan(h_) ) then
		
		lat2=lat_*pi/180
		lon2=lon_*pi/180
		dLat=lat2-lat1;
		dLon=lon2-lon1;

		a=sin(dLat/2) * sin(dLat/2) + sin(dLon/2) * sin(dLon/2) * cos(lat1) * cos(lat2); 
		c= 2 * atan2(sqrt(a), sqrt(1-a)); 
		cellSize = rayonterre * c;	
		
		if(cellSize < minDistance) then
			minDistance = cellSize
			nearestLatPoint=lat_
			nearestLongPoint=lon_		
			nearestValuePoint=h_
		endif
	endif
	
  goto 101
100	close(3)
write(6,*)nearestLongPoint,nearestLatPoint,nearestValuePoint
 
end
