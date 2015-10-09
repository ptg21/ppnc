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

req_data = {
	'm01s34i001':{
		'conversion_factor':1.657,
		'units': iris.unit.Unit('mole mole-1'),
		'standard_name':'mass_fraction_of_ozone_in_air',
		'req_standard_name':'mole_fraction_of_ozone_in_air',
		'req_long_name':'Ozone Volume Mixing Ratio',
		'var_name':'vmro3'
	},
	'm01s16i004':{
		'conversion_factor':1,
		'units': iris.unit.Unit('K'),
		'standard_name':'air_temperature',
		'req_standard_name':'air_temperature',
		'req_long_name':'Air Temperature',
		'var_name':'ta'
	},
	'm01s16i201':{
		'conversion_factor':1,
		'units': iris.unit.Unit('m'),
		'standard_name':'geopotential_height',
		'req_standard_name':'geopotential_height',
		'req_long_name':'Geopotential Height',
		'var_name':'zg'
	},
	'm01s00i002':{
		'conversion_factor':1,
		'units': iris.unit.Unit('m s-1'),
		'standard_name':'eastward_wind',
		'req_standard_name':'eastward_wind',
		'req_long_name':'Eastward Wind',
		'var_name':'ua'
	},
	'm01s00i003':{
		'conversion_factor':1,
		'units': iris.unit.Unit('m s-1'),
		'standard_name':'northward_wind',
		'req_standard_name':'northward_wind',
		'req_long_name':'Northward Wind',
		'var_name':'va'
	},
	'm01s01i232':{
		'conversion_factor':1,
		'units':iris.unit.Unit('K s-1'),
		'standard_name':'tendency_of_air_temperature_due_to_shortwave_heating',
		'req_standard_name':'tendency_of_air_temperature_due_to_shortwave_heating',
		'req_long_name':'Shortwave Heating Rate',
		'var_name':'tntsw'
	},
	'm01s02i232':{
		'conversion_factor':1,
		'units':iris.unit.Unit('K s-1'),
		'standard_name':'tendency_of_air_temperature_due_to_longwave_heating',
		'req_standard_name':'tendency_of_air_temperature_due_to_longwave_heating',
		'req_long_name':'Longwave Heating Rate',
		'var_name':'tntlw'
	},
	'm01s34i146':{
		'conversion_factor':360.0,
		'units':iris.unit.Unit('year'),
		'standard_name':'age_of_stratospheric_air',
		'req_standard_name':'age_of_stratospheric_air',
		'req_long_name':'Mean Age of Stratospheric air',
		'var_name':'mean_age'
	},
	'm01s34i049':{
		'conversion_factor':1.5188,
		'units': iris.unit.Unit('mole mole-1'),
		'standard_name':'mass_fraction_of_nitrous_oxide_in_air',
		'req_standard_name':'mole_fraction_of_nitrous_oxide_in_air',
		'req_long_name':'N2O Volume Mixing Ratio',
		'var_name':'vmrn2o'
	},
	'm01s34i009':{
		'conversion_factor':0.5523,
		'units':iris.unit.Unit('mole mole-1'),
		'standard_name':'mass_fraction_of_methane_in_air',
		'req_standard_name':'mole_fraction_of_methane_in_air',
		'req_long_name':'CH4 Volume Mixing Ratio',
		'var_name':'vmrch4'
	},
	'm01s34i010':{
		'conversion_factor':1.5188,
		'standard_name':'mass_fraction_of_carbon_dioxide_in_air',
		'req_standard_name':'mole_fraction_of_carbon_dioxide_in_air',
		'req_long_name':'CO2 Volume Mixing Ratio',
		'var_name':'vmrco2'
	},
	'm01s34i154':{
		'conversion_factor':1.2604,
		'units':iris.unit.Unit('mole mole-1'),
		'standard_name':'mass_fraction_of_hydrogen_chloride_in_air',
		'req_standard_name':'mole_fraction_of_hydrogen_chloride_in_air',
		'req_long_name':'HCl Volume Mixing Ratio',
		'var_name':'vmrhcl'
	},
	'm01s34i010':{
		'conversion_factor':0.9665,
		'units':iris.unit.Unit('mole mole-1'),
		'standard_name':'mass_fraction_of_carbon_monoxide_in_air',
		'req_standard_name':'mole_fraction_of_carbon_monoxide_in_air',
		'req_long_name':'CO Volume Mixing Ratio',
		'var_name':'vmrco'
	},
	'm01s34i1052':{
		'conversion_factor':1.588,
		'units':iris.unit.Unit('mole mole-1'),
		'standard_name':'mass_fraction_of_nitrogen_dioxide_in_air',
		'req_standard_name':'mole_fraction_of_nitrogen_dioxide_in_air',
		'req_long_name':'NO2 Volume Mixing Ratio',
		'var_name':'vmrno2'
	},
	'm01s34i002':{
		'conversion_factor':1.036,
		'units':iris.unit.Unit('mole mole-1'),
		'standard_name':'mass_fraction_of_nitrogen_monoxide_in_air',
		'req_standard_name':'mole_fraction_of_nitrogen_monoxide_in_air',
		'req_long_name':'NO Volume Mixing Ratio',
		'var_name':'vmrno'
	},
		'm01s34i052':{
		'conversion_factor':2.7970,
		'units':iris.unit.Unit('mole mole-1'),
		'standard_name':'mass_fraction_of_hydrogen_bromide_in_air',
		'req_standard_name':'mole_fraction_of_hydrogen_bromide_in_air',
		'req_long_name':'HBr Volume Mixing Ratio',
		'var_name':'vmrhbr'
	},
	'm01s00i265':{
		'conversion_factor':1,
		'units':iris.unit.Unit('1'),
		'standard_name':'cloud_area_fraction_in_atmosphere_layer',
		'req_standard_name':'cloud_area_fraction',
		'req_long_name':'Total Cloud Fraction',
		'var_name':'clt'
	}
}
