#!/bin/bash

# This file is part of ppnc.

# ppnc  Copyright (C) 2015  University of Cambridge

# Ppnc is free software: you can redistribute it and/or modify it under the 
# terms of the GNU Lesser General Public License as published by the Free Software 
# Foundation, either version 3 of the License, or (at your option) any later 
# version.

# Ppnc is distributed in the hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
# PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License along 
# with ppnc.  If not, see <http://www.gnu.org/licenses/>.

# bash multiple-sub.sh xipxa.m01s34i009.k.bjob xipxa.m01s34i009.l.bjob xipxa.m01s34i009.m.bjob xipxa.m01s34i009.n.bjob xipxa.m01s34i009.o.bjob xipxa.m01s34i009.p.bjob xipxa.m01s34i009.q.bjob xipxa.m01s34i009.r.bjob xipxa.m01s34i009.s.bjob xipxa.m01s34i009.t.bjob
BSUB=bsub

for job in ${@};do
	if [ "${job}" == "${1}" ];then
		OUT=`$BSUB < ${1}`
		LJOB=`echo $OUT | sed -rn  's/Job <([0-9]+)>.*/\1/p'`
		echo $LJOB
	else
		OUT=`$BSUB -w "done(${LJOB})" < ${job}`
		echo "$BSUB -w \"done(${LJOB})\" < ${job}"
		LJOB=`echo $OUT | sed -rn  's/Job <([0-9]+)>.*/\1/p'`
		echo $LJOB
	fi
done
