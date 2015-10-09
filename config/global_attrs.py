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

import os.path
from datetime import datetime
import uuid

class global_attrs():
	def __init__(self, frequency, jobid, version):
		self.attrs = { 
			'branch_time':  0.0,
			'contact' : 'J. Smith <jsmith@nowhere.com> 555-2368',
			'creation_date' : '', #a string representation of the date when the netCDF file was created in the format: 'YYYY-MM-DD-THH:MM:SSZ'. The 'T' and 'Z' are not modified, but the other variables are replaced with the correct time stamp. If using CMOR, this is generated automatically.'
			'experiment' : 'Projection',
			'experiment_id' : 'refC2',
			'forcing' : 'N/A',
			'frequency' : '', # e.g. 'yr', 'mon', 'day', 'subhr', 'fx' (for time-independent fields). Most of this data will be 'mon'. It's probably possible to work this out from the time points of the data.',
			'initialization_method' : 1,
			'institute_id' : 'FOO',
			'institution' : 'FOO, University of FOO, FOO, UK.',
			'model_id' : 'FOO',
			'modeling_realm' : 'atmos',
			'parent_experiment_id' : 'N/A',
			'parent_experiment_rip' : 'N/A',
			'physics_version' : 1,
			'physics_description' : '',
			'product' : 'output',
			'project_id' : 'CCMI1',
			'realization' : 1, #(for first set - this will change if we do additional ensemble members)
			'source' : 'FOO 2013 atmosphere',
			'table_id' : 'Table monthly (31 October 2014)', #see CMOR MIP table, e.g. 'Table monthly (1 February 2014)'
			'tracking_id' : '', #a string that is almost certainly unique to this file and must be generated using the OSSP utility which supports a number of different DCE 1.1 variant UUID options. For CCMI, as for CMIP5, version 4 (random number based) is required. The software can be downloaded from http://www.ossp.org/pkg/lib/uuid/.
			'comment' : 'All data from FOO is submitted on pressure levels, not model levels. The data has been interpolated to pressure using the data on the native hybrid theta levels and the pressure field on the same levels. Both fields have had the same time-meaning applied prior to this post-processing.', # 'Model jobid = XXXXX. Created using Iris version XX. SSTs and Sea-Ice provided by HadGEM2-ES historical and RCP6.0 r2i1p1 ensemble member'
			'history' : '', #'Extracted from files jobida.p*.pp-jobida.p*.pp'
			'references' : """Some References.""",
			'title' : 'FOO model output prepared for CCMI1 Projection',
			'initialization_description' : '' #  This is only required if groups are submitting runs with more than one initialization method.
			}
		
		self.freq_map = { # Mappings for frequency in filename
			'yr': 'annual',
			'mon': 'monthly',
			'day': 'daily',
			'fx': 'fixed',
			'subhr': 'hourly'
		}
		
		self.set_attrs(frequency, jobid, version)
	def set_attrs(self, frequency, jobid, version):
		self.attrs['frequency'] = frequency
		self.attrs['creation_date'] = datetime.now().strftime('%Y-%m-%d-T%H:%M:%SZ')
		self.attrs['tracking_id'] = str(uuid.uuid4())
		self.attrs['history'] = 'Model jobid = %s. Created using Iris version %s. SSTs and Sea-Ice provided by HadGEM2-ES historical and RCP6.0 r2i1p1 ensemble member' %(jobid, version)
		
	def gen_dirname(self,variable_name):
		#ESGF data node directory structure
		#<activity>/<product>/<institute>/<model>/<experiment>/<frequency>/<modeling realm>/
		#<MIP table>/<ensemble member>/<version number>/<variable name>/<CMOR filename>.
		
		dirname = [
			'CCMI-1', #<activity>
			'output1', #<product>
			self.attrs['institute_id'], #<institute>
			self.attrs['model_id'], #<model>
			self.attrs['experiment_id'], #<experiment>
			self.attrs['frequency'], #<frequency>
			self.attrs['modeling_realm'], #<modeling realm>
			self.freq_map[self.attrs['frequency']], #<MIP table>
			'r1i1p1', #<ensemble member>
			'v1', #<version number>
			variable_name #<variable name>
			]
		return os.path.join(dirname)
	
	def gen_filename(self,variable_name, temporal_subset):
		#<variable name>_<MIP table>_<model>_<experiment>_<ensemble member>[_<temporal subset>][_<geographical info>].nc
		filename = [
			variable_name, #<variable name>
			self.freq_map[self.attrs['frequency']], #<MIP table>
			self.attrs['model_id'], #<model>
			self.attrs['experiment_id'], #<experiment>
			'r1i1p1', #<ensemble member>
			temporal_subset, #[<temporal subset>]
			]
		return ('_'.join(filename) + '.nc')



