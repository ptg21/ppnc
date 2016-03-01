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

__version__ = "$Id$"

import iris
import numpy
import config.tweakables as tweakables
from config.req_data import req_data


class req():
    def __init__(self, STASH):
        self.STASH = STASH
        self.reqStdName = req_data[self.STASH]['req_standard_name']
        self.reqLongName = req_data[self.STASH]['req_long_name']
        self.cnvfact = req_data[self.STASH]['conversion_factor']
        self.var_name = req_data[self.STASH]['var_name']
        self.units = req_data[self.STASH]['units']
        self.is3D = True
        self.regridded = False

        # Pull in a comment from req_data if set
        if 'comment' in req_data[self.STASH]:
            self.comment = req_data[self.STASH]['comment']
        else:
            self.comment = None

        if 'valid_range' in req_data[self.STASH]:
            self.valid_range = req_data[self.STASH]['valid_range']
        else:
            self.valid_range = None

        if not self.reqStdName in iris.std_names.STD_NAMES:
            iris.std_names.STD_NAMES[self.reqStdName] = {'canonical_units': str(self.units)}

    def callback(self, cube, field, filename):
        if cube.attributes['STASH'] == self.STASH:
            cube.attributes['conversion_factor'] = self.cnvfact
            try:
                    cube.standard_name = self.reqStdName
            except ValueError:
                    cube.long_name = self.reqStdName
            cube.units = req_data[self.STASH]['units']

    def convert(self, cube, args):
        if cube.attributes['STASH'] == self.STASH:
            # make it 64-bit
            cube.data = cube.data.astype(dtype='float64')
            # If conversion_factor not 1, convert
            if self.cnvfact != 1:
                if cube.units.is_dimensionless() or cube.units.is_time():
                    cube.data = (cube.data / self.cnvfact)
                elif 'm-3' in cube.units.definition:
                    if args.cellfile is not None:
                        cellvolume = iris.load(args.cellfile)
                        cube.data = numpy.divide(cube.data, cellvolume[0].data)
                    else:
                        raise ValueError("Need to specify Grid Cell Volume File")

            try:
                cube.standard_name = self.reqStdName
            except ValueError:
                pass
            cube.long_name = self.reqLongName
            cube.units = req_data[self.STASH]['units']
        return cube

    def create_new_cubes(self, cubes):
        stashcube = cubes.extract(iris.AttributeConstraint(STASH=self.STASH))[0]
        # what are the dimensions of this cube
        if stashcube.ndim == 3:
            self.is3D = False
        elif stashcube.ndim == 4:
            self.is3D = True

        newcube = self.convert_pressure(stashcube, cubes)
        return self.add_metadata(newcube, stashcube)

    def mask_outside_valid_range(self, data):
        # If we have a valid range, mask things outside it.
        if self.valid_range:
            return numpy.ma.masked_outside(data, *self.valid_range)
        else:
            return data

    def convert_pressure(self, stashcube, cubes):

        if self.is3D:
            import pressureconv
            """Takes two cubes, vv and air_pressure, converts to pressure levels"""

            # Tolerance for checking whether cubes are equal. These just happen to
            # be the numpy defaults
            rtol = 1e-05
            atol = 1e-08

            # Check if heights are the same, otherwise exit with error
            if not cubes[0].coords('level_height') == []:
                if not numpy.allclose(cubes[0].coords('level_height')[0].points, cubes[1].coords('level_height')[0].points, rtol=rtol, atol=atol):
                    raise ValueError("Coordinates level_height for %s and %s do not match!" % (cubes[0].name(), cubes[1].name()))

            # check if lat/lon are different between vv and pp cubes
            if not compare_lat_lon(cubes=cubes, rtol=rtol, atol=atol):
                # Regrid
                pressure = (cubes.extract(iris.Constraint('air_pressure'))[0])
                pp = pressure.regrid(stashcube, iris.analysis.Linear()).data
                self.regridded = True
            else:
                pp = (cubes.extract(iris.Constraint('air_pressure'))[0]).data
            vv = stashcube.data

            # Use f2py pressureconv to convert to plevels
            newvv = numpy.ma.array(data=pressureconv.convert_height2pressure(plevels=tweakables.plevels, vv=vv, pp=pp, fillval=tweakables.fillval), fill_value=tweakables.fillval, dtype='float32')

            newcube = iris.cube.Cube(self.mask_outside_valid_range(newvv), standard_name=self.reqStdName, var_name=self.var_name, units=self.units, attributes=None, cell_methods=None, dim_coords_and_dims=None, aux_coords_and_dims=None, aux_factories=None)
            return newcube
        else:
            # no pressure to convert.
            cubedata = self.mask_outside_valid_range(numpy.ma.array(data=stashcube.data, fill_value=tweakables.fillval, dtype='float32'))
            return iris.cube.Cube(cubedata, standard_name=self.reqStdName, var_name=self.var_name, units=self.units, attributes=None, cell_methods=None, dim_coords_and_dims=None, aux_coords_and_dims=None, aux_factories=None)

    def add_metadata(self, cube, orig_cube):
        # Preserve the metadata
        cube.metadata = orig_cube.metadata
        cube.attributes['cell_measures'] = 'area: areacella'
        cube.var_name = self.var_name

        # Provide - cell_methods = "time: mean"
        cube.cell_methods = [iris.coords.CellMethod('mean', 'time')]

        # Make the coords
        if self.is3D:
            newcoords = iris.coords.DimCoord(tweakables.plevels,
                                             standard_name='air_pressure',
                                             var_name='plev',
                                             attributes={'positive': 'down'},
                                             units=iris.unit.Unit('Pa'))
        latcoords = coords_to_float64(orig_cube.coords('latitude')[0])
        longcorrds = coords_to_float64(orig_cube.coords('longitude')[0])

        # Rename them
        latcoords.var_name = 'lat'
        longcorrds.var_name = 'lon'

        new_time_unit = iris.unit.Unit('days since 1960-01-01', calendar='360_day')

        orig_cube.coords('time')[0].convert_units(new_time_unit)
        cube.add_dim_coord(orig_cube.coords('time')[0], 0)
        cube.coords('time')[0].var_name = 'time'

        # Stick them on the cube
        if self.is3D:
            cube.add_dim_coord(newcoords, 1)
            cube.add_dim_coord(latcoords, 2)
            cube.add_dim_coord(longcorrds, 3)
        else:
            cube.add_dim_coord(latcoords, 1)
            cube.add_dim_coord(longcorrds, 2)

        for coord in cube.coords():
            if coord.bounds is None:
                set_bounds(coord)

        # Prevent source from being overwritten.
        cube.attributes.pop('source')

        cube.attributes['associated_files'] = "baseURL: http://www.met.reading.ac.uk/ccmi/ gridspecFile: gridspec_atmos_fx_UMUKCA-UCAM_refC2_r0i0p0.nc"

        if self.comment is not None:
            cube.attributes['comment'] = self.comment

        if cube.standard_name.startswith('mole_fraction'):
            cube.attributes['comment'] = "Model output is in mass_fraction, and so data is converted to mole_fraction by dividing by conversion_factor. "
        elif not 'comment' in cube.attributes:
            # If it isn't set, create a blank entry.
            cube.attributes['comment'] = ""

        if self.regridded:
            cube.attributes['comment'] = cube.attributes['comment'] + "Due a mismatch in the latitude/longitude grids between the pressure field and the variable field, the pressure field was bilinearly interpolated in the horizontal prior to the interpolation from model levels onto pressure levels."

        return cube


def compare_lat_lon(cubes, rtol, atol):
    # Are there the same number of points in both
    if len(cubes[0].coords('latitude')[0].points) != len(cubes[1].coords('latitude')[0].points):
        return False
    # Do the points match
    elif not ((numpy.allclose(cubes[0].coords('latitude')[0].points, cubes[1].coords('latitude')[0].points, rtol=rtol, atol=atol)) and (numpy.allclose(cubes[0].coords('longitude')[0].points, cubes[1].coords('longitude')[0].points, rtol=rtol, atol=atol))):
        return False
    else:
        return True


def set_bounds(coord):
    # guess_bounds sets |bounds| too large
    coord.guess_bounds()
    if coord.var_name == 'lat':
        # remove bounds >90.0 or <-90.0
        newbounds = coord.bounds.copy()
        newbounds[0][0] = -90.0
        newbounds[-1][1] = 90.0
        coord.bounds = newbounds
    return coord


def coords_to_float64(coord):
    coord.points = coord.points.astype(dtype='float64')
    return coord
