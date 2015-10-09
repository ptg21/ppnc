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

declare -A TSUBSET
TSUBSET=( ["g"]="196001-196912" \
["h"]="197001-197912" \
["i"]="198001-198912" \
["j"]="199001-199912" \
["k"]="200001-200912" \
["l"]="201001-201912" \
["m"]="202001-202912" \
["n"]="203001-203912" \
["o"]="204001-204912" \
["p"]="205001-205912" \
["q"]="206001-206912" \
["r"]="207001-207912" \
["s"]="208001-208912" \
["t"]="209001-209912" )

STASH=${1}
UPX=h
PGRID=THETA
# PGRID=RHO

for year in "${!TSUBSET[@]}";do
cat > xipxa.${STASH}.${year}.bjob << EOF
#!/bin/bash
#BSUB -o xipxa.${STASH}.${year}.%J.o
#BSUB -e xipxa.${STASH}.${year}.%J.e
#BSUB -q lotus
#BSUB -J xipxa.${STASH}.${year}
#BSUB -R "select[maxmem > 11000] rusage[mem=11000]"
#BSUB -W 60

# DBG='echo'

WDIR=/home/users/$USER/to-netCDF

PYBIN=/usr/bin/python2.7
JID=xipxa
JPATH=/path/to/jobs/\${JID}/archive
OUTPREFIX=/path/to/output
STASH=$STASH

set -x
set -e

cd \$WDIR
test -d \$OUTDIR || mkdir -p \$OUTDIR || exit 1

\$DBG \$PYBIN ppnc.py  -j \$JID \
        -t "${TSUBSET[$year]}" \
        -p \$OUTPREFIX \
        -s \$STASH \
	--pgrid ${PGRID} \
        -f \${JPATH}/\${JID}a.p${UPX}${year}*.pp
EOF
done
