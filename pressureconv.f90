! This file is part of ppnc.

! ppnc  Copyright (C) 2015  University of Cambridge

! Ppnc is free software: you can redistribute it and/or modify it under the 
! terms of the GNU Lesser General Public License as published by the Free Software 
! Foundation, either version 3 of the License, or (at your option) any later 
! version.

! Ppnc is distributed in the hope that it will be useful, but WITHOUT ANY 
! WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
! PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

! You should have received a copy of the GNU Lesser General Public License along 
! with ppnc.  If not, see <http://www.gnu.org/licenses/>.

subroutine convert_height2pressure(xmax,ymax,zmax,tmax,pmax,plevels,vv,pp,newvv,fillval)
implicit none
! double precision
INTEGER, PARAMETER :: dp=8

integer, intent(in) :: xmax,ymax,zmax,tmax,pmax
real(kind=dp), dimension(1:pmax), intent(in) :: plevels

! Iris provides a cube [time,model_level_number,latitude,longitude]
real(kind=dp), dimension(1:tmax,1:zmax,1:ymax,1:xmax), intent(in) :: vv

! Iris provides a cube [time,model_level_number,latitude,longitude]
real(kind=dp), dimension(1:tmax,1:zmax,1:ymax,1:xmax), intent(in) :: pp

! Iris expects a cube [time,plev,latitude,longitude]
real(kind=dp), dimension(1:tmax,1:pmax,1:ymax,1:xmax), intent(out) :: newvv

real(kind=dp), intent(in) :: fillval

  real(kind=dp) :: p1,p2,ptarget
  integer :: ix,iy,iz,it,ip
  logical undef
  
  newvv(:,:,:,:)=fillval
  
  
  do it=1,tmax
    do iy=1,ymax
      do ix=1,xmax
        do ip=1,pmax
          !
          ! determine the interval, loop over model levels and interpolate linear in log(p)
          !
          ptarget=log(plevels(ip))
          undef=.false.
          do iz=2,zmax
            p1=log(pp(it,iz-1,iy,ix))
            p2=log(pp(it,iz,iy  ,ix))
              if ( ptarget .lt. p1 .and. ptarget .ge. p2 ) then
                newvv(it,ip,iy,ix)=vv(it,iz-1,iy,ix)+&
                (((vv(it,iz,iy,ix)-vv(it,iz-1,iy,ix))/(p2-p1))*(ptarget-p1))                 
              end if
            end do ! model level loop
        end do ! pressure loop
      end do ! longitude loop
    end do ! latitude loop
  end do ! time

  
end subroutine convert_height2pressure

