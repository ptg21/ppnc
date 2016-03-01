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
import numpy as np
import argparse
import os
import datetime
from ppnc import save
import config.tweakables as tweakables

# calculates the area of a regular lon-lat gridcell


def calc_area(lon, lat, radians=False):
    """
    Calculates the area of a gridcell on the surface of a sphere. Assumed to be in degrees. Rather than passing in the lat and lon coordinates, instead pass-in the bounds of these coordinates.
    """
    # A = R^2 |sin(lat1)-sin(lat2)| |lon1-lon2| where R is earth radius (6371 kms)
    # A = R^2 * solid angle of latitude-longitude rectangle
    # polar rows (at +/-90) are treated differently.
    import numpy as np
    Pi = np.float128(3.141592653589793238462643383279)
    Earth_Radius_Sq = (np.float128(6371.0 * 1.0E3)) ** 2
    lon = np.float128(lon)
    lat = np.float128(lat)
    if not radians:
        rlon = (lon[:, :] / np.float128(180.0)) * Pi
        rlat = (lat[:, :] / np.float128(180.0)) * Pi
    else:
        rlon = lon[:, :]
        rlat = lat[:, :]
    area = np.zeros((len(rlat), len(rlon)), np.float128)
    j = 0
    while j < len(rlat[:, 0]):
        i = 0
        while i < len(rlon[:, 0]):
            area[j, i] = (Earth_Radius_Sq) * (abs(np.sin(rlat[j, 0]) - np.sin(rlat[j, 1])) * abs(rlon[i, 0] - rlon[i, 1]))
            i += 1
        j += 1
    del Pi
    del Earth_Radius_Sq
    del lon
    del lat
    del rlon
    del rlat
    del i
    del j
    return area


def get_opts_cella():
    parser = argparse.ArgumentParser(description='Output areacella and volcella to NETCDF4')
    parser.add_argument('-a', '--orog', type=str, nargs=1, required=True, help='File containing model orography (surface altitude)')
    parser.add_argument('-l', '--land', type=str, nargs=1, required=True, help='File containing model land area fraction')
    parser.add_argument('-f', '--file', type=str, nargs=1, default=None, help='Optional file containing theta (m01s00i004) for calculation of grid-cell volume. Single time-point only.')
    parser.add_argument('-o', '--outfile', type=str, nargs=1, default=None, help='Name of output file')
    parser.add_argument('-p', '--outprefix', type=str, nargs=1, default=[os.getcwd()], help='OUTPREFIX/outdir/outfile. Defaults to cwd')
    parser.add_argument('-w', '--saver', type=str, nargs=1, default='iris', help='Save with: iris')
    parser.add_argument('-j', '--jid', type=str, default=None, help='Model JobID')
    parser.add_argument('-m', '--dirmode', type=int, default=0o755, help='Octal mode for creating directories')
        ## following are added as constants below
    #parser.add_argument('-i','--freq',type=str, nargs=1,default='fx',choices=['yr', 'mon', 'day', 'subhr', 'fx'],help='Frequency, should be fx (fixed)')
    #parser.add_argument('-t','--tsub', type=str, default=None,help='Temporal Subset, should be None for areacella or volcella, as these are invariant')
    return parser.parse_args()


def loadPP_cella(file=file, stash=None):
    """Loads a pp file with a callback"""
    if stash is not None:
        constr = [iris.AttributeConstraint(STASH=stash)]
    else:
        constr = None
        #print file
        #print constr
    cube = iris.load_cube(file, constr)
    return cube


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


def fix_coords(cube):
    for coord in cube.coords():
        if not isinstance(coord.points, int):
            # want all floats to be double, except for orography
            if coord.standard_name != 'surface_altitude':
                coord.points = coord.points.astype(dtype='float64')

    cube.coord('latitude').var_name = 'lat'
    cube.coord('longitude').var_name = 'lon'

    cube.coord('longitude').guess_bounds()

    # latitude is a special case
    cube.coord('latitude').guess_bounds()
    # remove bounds >90.0 or <-90.0
    newbounds = cube.coord('latitude').bounds.copy()
    newbounds[0][0] = -90.0
    newbounds[-1][1] = 90.0
    cube.coord('latitude').bounds = newbounds

    for coord in cube.coords():
        if coord.bounds is not None:
            if not isinstance(coord.bounds, int):
                coord.bounds = coord.bounds.astype(dtype='float64')

    del newbounds
    return cube


def main(args):
    # we need these for manipulating files, but we don't want these
    # as command-line arguments. Add to Namespace now.
    args.freq = 'fx'
    args.tsub = None

# Load pp files, constrain by stash
    # Calculations will be done assuming a THETA grid as the base model grid
    # surface temperature - on theta grid. Need 2D field to overwrite
    area = loadPP_cella(file=args.orog, stash='m01s00i033')
    # model orography
    orog = loadPP_cella(file=args.orog, stash='m01s00i033')
    # land fraction
    land = loadPP_cella(file=args.land, stash='m01s00i505')
    # theta field - need 3D for volume calculation
    if args.file is not None:
        theta = loadPP_cella(file=args.file, stash='m01s00i004')
        if len(theta.coord('time').points) != 1:
            raise ValueError('Only one time-point required for calculation of grid-cell volume')
#
# CALCULATE SURFACE AREA
    # set lat/lon bounds
    area = fix_coords(area)
    sarea = calc_area(area.coord('longitude').bounds, area.coord('latitude').bounds)
    area.rename('areacella')
    area.long_name = 'Atmosphere Grid-Cell Area'
    area.standard_name = 'cell_area'
    area.var_name = 'areacella'
    area.units = 'm2'
    area.data = np.float32(sarea)
    # remove all cell_methods
    area.cell_methods = None
    del area.attributes['STASH']

    # add-in attributes to variable
    area.attributes['associated_files'] = "baseURL: http://www.met.reading.ac.uk/ccmi/ gridspecFile: gridspec_atmos_fx_UMUKCA-UCAM_refC2_r0i0p0.nc"
    area.attributes['comment'] = "For atmospheres with more than 1 mesh (e.g., staggered grids), report areas that apply to surface vertical fluxes of energy."
    area.attributes['history'] = "Surface area calculated from model THETA grid using the equation for the surface area of a sphere. Lat/lon points taken from model orography (surface_altitude) field"

    # make sure there is a fill value
    area.data = np.ma.asarray(area.data, dtype='float32')
    np.ma.set_fill_value(area.data, tweakables.fillval)

#
# CALCULATE OROGRAPHY (SURFACE_ALTITUDE)
    # set lat/lon bounds
    orog = fix_coords(orog)
    orog.data = np.float32(orog.data)
    orog.rename('surface_altitude')
    orog.long_name = 'Surface Altitude'
    orog.standard_name = 'surface_altitude'
    orog.var_name = 'orog'
    # remove all cell_methods
    orog.cell_methods = None
    orog.attributes['cell_measures'] = 'area: areacella'

    # add-in attributes to variable
    orog.attributes['associated_files'] = "baseURL: http://www.met.reading.ac.uk/ccmi/ gridspecFile: gridspec_atmos_fx_UMUKCA-UCAM_refC2_r0i0p0.nc"
    orog.attributes['comment'] = 'height above the geoid; as defined here, ""the geoid"" is a surface of constant geopotential that, if the ocean were at rest, would coincide with mean sea level. Under this definition, the geoid changes as the mean volume of the ocean changes (e.g., due to glacial melt, or global warming of the ocean).  Report here the height above the present-day geoid.  Over ocean, report as 0.0'

    # make sure there is a fill value
    orog.data = np.ma.asarray(orog.data, dtype='float32')
    np.ma.set_fill_value(orog.data, tweakables.fillval)

#
# CALCULATE LAND AREA FRACTION
    # set lat/lon bounds
    land = fix_coords(land)
    land.long_name = 'Land Area Fraction'
    land.data = 100.0 * np.float32(land.data)
    land.units = '%'
    land.attributes['STASH'] = str(land.attributes['STASH']) + '*100.0'
    # remove all cell_methods
    land.cell_methods = None
    land.attributes['cell_measures'] = 'area: areacella'
    land.var_name = 'sftlf'

    # add-in attributes to variable
    land.attributes['associated_files'] = "baseURL: http://www.met.reading.ac.uk/ccmi/ gridspecFile: gridspec_atmos_fx_UMUKCA-UCAM_refC2_r0i0p0.nc"
    land.attributes['comment'] = "For atmospheres with more than 1 mesh (e.g., staggered grids), report areas that apply to surface vertical fluxes of energy."

    # make sure there is a fill value
    land.data = np.ma.asarray(land.data, dtype='float32')
    np.ma.set_fill_value(land.data, tweakables.fillval)

    if args.file is not None:
        # CALCULATE CORRECT ALTITUDES
        # add the orography as an auxillary coordinate
        auxcoord = iris.coords.AuxCoord(orog.data, standard_name=str(orog.standard_name), long_name="orography", var_name="orog", units=orog.units)
        # added in to lat/lon data_dims=(ht=0,lat=1,lon=2) - only a single time point allowed
        theta.add_aux_coord(auxcoord, (1, 2, ))

        # now calculate the correct altitude above sea-level
        factory = iris.aux_factory.HybridHeightFactory(delta=theta.coord("level_height"), sigma=theta.coord("sigma"), orography=theta.coord("surface_altitude"))

        # now create the 'altitude' derrived coordinate
        theta.add_aux_factory(factory)

        # make altitude it's own 3D cube - copy theta as a basis
        alt = theta.copy()
        # remove any time information
        alt.remove_coord('time')
        ## time_bnds is removed when time is
        #alt.remove_coord('time_bnds')
        alt.remove_coord('forecast_reference_time')
        alt.remove_coord('forecast_period')
        # remove all cell_methods
        alt.cell_methods = None
        # copy in the data from the theta derived coordinate
        alt.data = theta.coord('altitude').points
        alt.rename('altitude')
        alt.long_name = str(alt.name)
        alt.units = 'm'
        del alt.attributes['STASH']
        # set lat/lon bounds
        alt = fix_coords(alt)

        # CALCULATE VOLUME
        # now calculate cell volume - copy altitude
        vol = alt.copy()
        # lowest level compared to surface
        vol.data[0, :, :] = (alt.data[0, :, :] - orog.data[:, :]) * area.data[:, :]
        # other levels compared to level below
        for i in np.arange(1, len(vol.coord('model_level_number').points)):
            vol.data[i, :, :] = (alt.data[i, :, :] - alt.data[i - 1, :, :]) * area.data[:, :]
        vol.rename('cell_volume')
        vol.long_name = 'Atmosphere Grid-Cell Volume'
        # cell_volume is not a standard name
        #area.standard_name='cell_volume'
        vol.var_name = 'cell_volume'
        vol.units = 'm3'
        # add-in variable attributes
        vol.attributes['associated_files'] = "baseURL: http://www.met.reading.ac.uk/ccmi/ gridspecFile: gridspec_atmos_fx_UMUKCA-UCAM_refC2_r0i0p0.nc"

        # make sure there is a fill value
        vol.data = np.ma.asarray(vol.data, dtype='float32')
        np.ma.set_fill_value(vol.data, tweakables.fillval)

    # no time dimension, so do not have as unlimited
    iris.FUTURE.netcdf_no_unlimited = True

    # ValueError: 'missing_value' is not a permitted attribute
    # nasty hack. Do this just before the last operations.
    # May go away in newer iris versions - https://github.com/SciTools/iris/issues/1588
    dict.__setitem__(area.attributes, 'missing_value', tweakables.fillval)
    dict.__setitem__(orog.attributes, 'missing_value', tweakables.fillval)
    dict.__setitem__(land.attributes, 'missing_value', tweakables.fillval)
    if args.file is not None:
        dict.__setitem__(vol.attributes, 'missing_value', tweakables.fillval)

    save(args, cube=area, variable_name='areacella')
    save(args, cube=orog, variable_name='orog')
    save(args, cube=land, variable_name='sftlf')
    if args.file is not None:
        save(args, cube=vol, variable_name='volcella')


if __name__ == "__main__":
    args = get_opts_cella()
    print "Using version: %s and Iris %s" % (__version__, iris.__version__)
    print "Started %s" % (datetime.datetime.now())
    main(args)
    print "Finished %s" % (datetime.datetime.now())
