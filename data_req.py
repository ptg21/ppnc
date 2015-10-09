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

import iris, numpy
import config.tweakables as tweakables
from config.req_data import req_data

class req():
	def __init__(self,STASH):
		self.STASH = STASH
		self.reqStdName = req_data[self.STASH]['req_standard_name']
		self.reqLongName = req_data[self.STASH]['req_long_name']
		self.cnvfact = req_data[self.STASH]['conversion_factor']
		self.var_name = req_data[self.STASH]['var_name']

	def callback(self,cube, field, filename):
		if cube.attributes['STASH'] == self.STASH:
			cube.attributes['conversion_factor']=self.cnvfact
			try:
			    cube.standard_name=self.reqStdName
			except ValueError:
			    cube.long_name=self.reqStdName
			cube.units=req_data[self.STASH]['units']

	def convert(self,cube):
		if cube.attributes['STASH'] == self.STASH:
			# make it 64-bit
			cube.data = cube.data.astype(dtype='float64')
			
			# If conversion_factor not 1, convert
			if self.cnvfact != 1:
				cube.data = (cube.data/self.cnvfact)
			
			try:
				cube.standard_name = self.reqStdName
			except ValueError:
				pass
				#cube.long_name=self.reqStdName
			cube.long_name = self.reqLongName
			cube.units=req_data[self.STASH]['units']
		return cube
  
	def coords_to_float64(self,coord):
		coord.points = coord.points.astype(dtype='float64')
		return coord
	
	def set_bounds (self,coord):
		# guess_bounds sets |bounds| too large
		coord.guess_bounds()
		if (coord.var_name == 'lat'):
			# remove bounds >90.0 or <-90.0
			newbounds = coord.bounds.copy()
			newbounds[0][0] = -90.0
			newbounds[-1][1] = 90.0
			coord.bounds = newbounds
		return coord
	def compare_lat_lon(self,cubes, rtol, atol):
		# Are there the same number of points in both
		if len(cubes[0].coords('latitude')[0].points) != len(cubes[1].coords('latitude')[0].points):
			return False
		# Do the points match
		elif not ((numpy.allclose(cubes[0].coords('latitude')[0].points, cubes[1].coords('latitude')[0].points, rtol=rtol, atol=atol)) and (numpy.allclose(cubes[0].coords('longitude')[0].points, cubes[1].coords('longitude')[0].points, rtol=rtol, atol=atol))):
			return False
		else:
			return True
		
	def convert_pressure(self,cubes):
		import pressureconv
		"""Takes two cubes, vv and air_pressure, converts to pressure levels"""
		regridded = False
		stashcube = cubes.extract(iris.AttributeConstraint(STASH=self.STASH))[0]
		
		# Tolerance for checking whether cubes are equal. These just happen to be the numpy defaults
		rtol=1e-05
		atol=1e-08

		# Check if heights are the same, otherwise exit with error
		if not cubes[0].coords('level_height') == []:
			if not numpy.allclose(cubes[0].coords('level_height')[0].points,cubes[1].coords('level_height')[0].points, rtol=rtol, atol=atol):
				raise ValueError("Coordinates level_height for %s and %s do not match!" %(cubes[0].name(), cubes[1].name()))
		
		# check if lat/lon are different between vv and pp cubes
		if not self.compare_lat_lon(cubes=cubes, rtol=rtol, atol=atol):
			# Regrid
			pressure = (cubes.extract(iris.Constraint('air_pressure'))[0])
			pp=pressure.regrid(stashcube,iris.analysis.Linear()).data
			regridded = True
		else:
			pp = (cubes.extract(iris.Constraint('air_pressure'))[0]).data
		vv = stashcube.data

		# Use f2py pressureconv to convert to plevels
		newvv = numpy.ma.array(data=pressureconv.convert_height2pressure(plevels=tweakables.plevels,vv=vv,pp=pp,fillval=tweakables.fillval),fill_value=tweakables.fillval,dtype='float32')
		newcube = iris.cube.Cube(newvv, standard_name=self.reqStdName, var_name=self.var_name, units=iris.std_names.STD_NAMES[self.reqStdName]['canonical_units'], attributes=None, cell_methods=None, dim_coords_and_dims=None, aux_coords_and_dims=None, aux_factories=None) 
		# Preserve the metadata
		newcube.metadata = stashcube.metadata
		newcube.attributes['cell_measures'] = 'area: areacella'
		newcube.var_name = self.var_name
		
		# Provide - cell_methods = "time: mean"		
		newcube.cell_methods = [iris.coords.CellMethod('mean', 'time')]
		
		# Make the coords
		newcoords = iris.coords.DimCoord(tweakables.plevels, standard_name='air_pressure', var_name='plev',  attributes={'positive': 'down'}, units=iris.unit.Unit('Pa'))
		latcoords = self.coords_to_float64(stashcube.coords('latitude')[0])
		longcorrds = self.coords_to_float64(stashcube.coords('longitude')[0])
		
		# Rename them
		latcoords.var_name = 'lat'
		longcorrds.var_name = 'lon'

		new_time_unit = iris.unit.Unit('days since 1960-01-01', calendar='360_day')

		stashcube.coords('time')[0].convert_units(new_time_unit)
		newcube.add_dim_coord(stashcube.coords('time')[0],0)
		newcube.coords('time')[0].var_name='time'
		
		# Stick them on the cube
		newcube.add_dim_coord(newcoords,1)
		newcube.add_dim_coord(latcoords,2)
		newcube.add_dim_coord(longcorrds,3)
		
		for coord in newcube.coords():
			if coord.bounds == None:
				self.set_bounds(coord)
		# Prevent source from being overwritten.
		newcube.attributes.pop('source')
		newcube.attributes['associated_files'] = "baseURL: http://www.met.reading.ac.uk/ccmi/ gridspecFile: gridspec.nc"
		
		if newcube.standard_name.startswith('mole_fraction'):
			newcube.attributes['comment'] = "Model output is in mass_fraction, and so data is converted to mole_fraction by dividing by conversion_factor. "
		elif not ('comment' in newcube.attributes):
			# If it isn't set, create a blank entry.
			newcube.attributes['comment'] = ""
		
		if regridded:
			newcube.attributes['comment'] = newcube.attributes['comment'] + "Due a mismatch in the latitude/longitude grids between the pressure field and the variable field, the pressure field was bilinearly interpolated in the horizontal prior to the interpolation from model levels onto pressure levels."
		
		return newcube
