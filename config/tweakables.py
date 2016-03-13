#!/usr/bin/env python

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

__version__ = "$Format:%h$"

import numpy

# Plevels in Pa
plevels = (numpy.array([100000., 85000., 70000., 50000., 40000., 30000., 25000., 20000., 17000., 15000., 13000., 11500., 10000., 9000., 8000., 7000., 5000., 3000., 2000., 1500., 1000., 700., 500., 300., 200., 150., 100., 50., 30., 20., 10.], dtype='float64'))

fillval = 1e+20

data_version = 1
