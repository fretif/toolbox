program toto
use ieee_arithmetic
implicit none
double precision pi,val_,x0,x1,rayonterre,deg2rad,rad2deg
integer imax,jmax,i,j
integer::narg,cptArg !#of arg & counter of arg
 character filename*100, args*20
 character(len=20)::name !Arg name

double precision,dimension(:,:),allocatable ::               &
       lon_t                                  &
      ,lat_t                                  &
      ,gridrotcos_t                           &
      ,gridrotsin_t              	      & 
      ,mask_t                                 & 
      ,vel_u                                  &
      ,vel_v                                  &
      ,rotvel_u  	                      &
      ,rotvel_v 				  

! Init globa var
pi=acos(-1.)
deg2rad=pi/180.d0
rad2deg=180.d0/pi 
rayonterre=6370949.00000

! Read imax and jmax from arguments
 narg=command_argument_count()
if(narg==2)then
 
  call get_command_argument(1,args)
  read (args, *)imax
  call get_command_argument(2,args)
  read (args, *)jmax

! Allocate tab
allocate(gridrotcos_t        (0:imax,0:jmax)                 ) ; gridrotcos_t=0
allocate(gridrotsin_t        (0:imax,0:jmax)                 ) ; gridrotsin_t=0
allocate(lon_t        (0:imax,0:jmax)                 ) ; lon_t=0
allocate(lat_t        (0:imax,0:jmax)                 ) ; lat_t=0
allocate(vel_u        (0:imax,0:jmax)                 ) ; vel_u=0
allocate(vel_v        (0:imax,0:jmax)                 ) ; vel_v=0
allocate(mask_t        (0:imax,0:jmax)                 ) ; mask_t=0
allocate(rotvel_u        (0:imax,0:jmax)                 ) ; rotvel_u=0
allocate(rotvel_v        (0:imax,0:jmax)                 ) ; rotvel_v=0

! Read longitude_t
      open(unit=3,file='longitude_t')
 101  read(3,*,end=100)i,j,val_
		
	lon_t(i,j)=val_*deg2rad
		
      goto 101
100	close(3)
! Read latitude_t
      open(unit=3,file='latitude_t')
 103  read(3,*,end=102)i,j,val_

	lat_t(i,j)=val_*deg2rad
		
      goto 103
102	close(3)

! Read vel_u
      open(unit=3,file='vel_u')
 113  read(3,*,end=112)i,j,val_
	
	vel_u(i,j)=val_		
		
      goto 113
112	close(3)

! Read vel_v
      open(unit=3,file='vel_v')
 115  read(3,*,end=114)i,j,val_
		vel_v(i,j)=val_		
      goto 115
114	close(3)

! Read mask_t
      open(unit=3,file='mask_t')
 117  read(3,*,end=116)i,j,val_
		mask_t(i,j)=val_		
      goto 117
116	close(3)


! Tableaux de rotation si axes non paralleles lignes lon et lat   !07-03-13
      do j=0,jmax-1
      do i=0,imax-1
	
       x1=lon_t(i+1,j)-lon_t(i-1,j)
	
       if(x1<-pi)x1=x1+2.*pi
       if(x1> pi)x1=x1-2.*pi
       x0=-atan2(lat_t(i+1,j)-lat_t(i-1,j),x1*cos(lat_t(i,j)))     !13-02-13

       gridrotcos_t(i,j)=cos(x0)
       gridrotsin_t(i,j)=sin(x0)

      enddo
      enddo
! rotation u
     do j=0,jmax-1
     do i=0,imax-1

	if(mask_t(i,j)==1  .and. .NOT. ieee_is_nan(vel_u(i  ,j  )) .and. .NOT. ieee_is_nan(vel_u(i+1  ,j  )) .and. .NOT. ieee_is_nan(vel_v(i  ,j  )) .and. .NOT. ieee_is_nan(vel_v(i  ,j+1  ))) then	
	 
		rotvel_u(i,j)=0.5*(                        &
            ( vel_u(i  ,j  )                       &
             +vel_u(i+1,j  ))*gridrotcos_t(i,j)    &
           +( vel_v(i  ,j  )                       &
             +vel_v(i  ,j+1))*gridrotsin_t(i,j)    &
              ) 	
	endif  

        enddo
	enddo
! rotation v
 do j=0,jmax-1
        do i=0,imax-1

	if(mask_t(i,j)==1  .and. .NOT. ieee_is_nan(vel_u(i  ,j  )) .and. .NOT. ieee_is_nan(vel_u(i+1  ,j  )) .and. .NOT. ieee_is_nan(vel_v(i  ,j  )) .and. .NOT. ieee_is_nan(vel_v(i  ,j+1  ))) then	

		rotvel_v(i,j)=0.5*(                        &
           -( vel_u(i  ,j  )                       &
             +vel_u(i+1,j  ))*gridrotsin_t(i,j)    &
           +( vel_v(i  ,j  )                       &
             +vel_v(i  ,j+1))*gridrotcos_t(i,j)    &
              )

	endif 

        enddo
  	enddo


! on ecrit U
open(unit=10,file='vel_u_ew',recl=10000)
    
        do j=jmax-1,0,-1
        do i=2,imax-3

		if(mask_t(i,j)==1) then
		
			write(10,*)lon_t(i,j)*rad2deg,lat_t(i,j)*rad2deg,rotvel_u(i,j)
		else
			write(10,*)lon_t(i,j)*rad2deg,lat_t(i,j)*rad2deg,'NaN'
		endif

        enddo
	enddo
 close(10)

! on ecrit V
open(unit=10,file='vel_v_ns',recl=10000)
    
        do j=jmax-1,0,-1
        do i=2,imax-3	

		if(mask_t(i,j)==1) then  		
			write(10,*)lon_t(i,j)*rad2deg,lat_t(i,j)*rad2deg,rotvel_v(i,j)
		else
			write(10,*)lon_t(i,j)*rad2deg,lat_t(i,j)*rad2deg,'NaN'
		endif

        enddo
  	enddo
 close(10)

endif

end


