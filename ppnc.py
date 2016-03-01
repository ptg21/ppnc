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

import os
import datetime
import argparse
import iris
from functools import partial
from data_req import req
from config.global_attrs import global_attrs
import config.tweakables as tweakables


def get_opts():
    parser = argparse.ArgumentParser(description='Convert PP to NETCDF4')
    parser.add_argument('-f', '--files', type=str, nargs='+', required=True, help='List of Filenames')
    parser.add_argument('-o', '--outfile', type=str, nargs=1, default=None, help='Name of Outfile')
    parser.add_argument('-p', '--outprefix', type=str, nargs=1, default=[os.getcwd()], help='OUTPREFIX/outdir/outfile. Defaults to cwd')
    parser.add_argument('-s', '--stash', type=str, nargs=1, default=None, help='STASH to restrict to')
    parser.add_argument('-w', '--saver', type=str, nargs=1, default='iris', help='Save with: iris')
    parser.add_argument('-j', '--jid', type=str, default=None, help='Model JobID')
    parser.add_argument('-g', '--pgrid', type=str, default='THETA', choices=['THETA', 'RHO'], help='Pressure Grid')
    parser.add_argument('-t', '--tsub', type=str, default='201001-201912', help='Temporal Subset, e.g 201001-201912')
    parser.add_argument('-c', '--cellfile', type=str, default=None, help='Grid Cell Area or Volume File')
    parser.add_argument('-m', '--dirmode', type=int, default=0o755, help='Octal mode for creating directories')
    parser.add_argument('-i', '--freq', type=str, nargs=1, default='mon', choices=['yr', 'mon', 'day', 'subhr', 'fx'], help='Frequency')
    return parser.parse_args()


def get_pressure_stash(pgrid):
    if pgrid == 'RHO':
        return 'm01s00i407'
    elif pgrid == 'THETA':
        return 'm01s00i408'


def loadPP(args, reqd):
    """Loads a pp file with a callback"""
    if args.stash:
        constr = [iris.AttributeConstraint(STASH=args.stash[0]), iris.AttributeConstraint(STASH=get_pressure_stash(args.pgrid))]
    else:
        constr = None
    cubes = iris.load(args.files, constraints=constr, callback=reqd.callback)
    return cubes


def makeDirs(dirname, mode):
    if not os.path.exists(dirname):
        os.makedirs(dirname, mode)


def save(args, cube, variable_name):
    if args.saver == 'iris':
        saveiris(args, cube, variable_name)


def saveiris(args, cube, variable_name):
    # Save the output as NETCDF4 classic
    ga = global_attrs(frequency=args.freq, jobid=args.jid, version=iris.__version__)

    # Make the output dir
    if args.outfile is None:
        outdir = os.path.join(*(args.outprefix + ga.gen_dirname(variable_name)))
        outfile = ga.gen_filename(variable_name, temporal_subset=args.tsub)
        outpath = os.path.join(outdir, outfile)
        makeDirs(outdir, args.dirmode)
    else:
        outpath = args.outfile[0]
    saver = iris.fileformats.netcdf.Saver(filename=outpath, netcdf_format='NETCDF4_CLASSIC')
    saver.update_global_attributes(Conventions=iris.fileformats.netcdf.CF_CONVENTIONS_VERSION,
                                   attributes=ga.attrs)
    saver.write(cube, local_keys=['comment', 'associated_files', 'coordinates', 'missing_value', 'conversion_factor', 'cell_measures', '_FillValue'])


def main(args):

    # An object containing the things that are requested and methods to do things with them.
    reqd = req(STASH=args.stash[0])

    # Load pp files, constrain by stash
    cubes = loadPP(args, reqd)

    #    convert stashes to those requested
    mapfunction = partial(reqd.convert, args=args)
    cubes = map(mapfunction, cubes)

    # Convert to pressure levels
    newdata = reqd.create_new_cubes(iris.cube.CubeList(cubes))

    # ValueError: 'missing_value' is not a permitted attribute
    # nasty hack. Do this just before the last operations.
    # May go away in newer iris versions - https://github.com/SciTools/iris/issues/1588
    dict.__setitem__(newdata.attributes, 'missing_value', tweakables.fillval)

    save(args, cube=newdata, variable_name=reqd.var_name)


if __name__ == "__main__":
    args = get_opts()
    print "Using version: %s and Iris %s" % (__version__, iris.__version__)
    print "Started %s: %s at %s" % (args.stash, args.tsub, datetime.datetime.now())
    main(args)
    print "Finished %s: %s at %s" % (args.stash, args.tsub, datetime.datetime.now())
