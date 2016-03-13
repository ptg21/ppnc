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

import iris

req_data = {
    'm01s34i001': {
        'conversion_factor': 1.657,
        'units': iris.unit.Unit('mole mole-1'),
        'standard_name': 'mass_fraction_of_ozone_in_air',
        'req_standard_name': 'mole_fraction_of_ozone_in_air',
        'req_long_name': 'Ozone Volume Mixing Ratio',
        'var_name': 'vmro3'
    },
    'm01s16i004': {
        'conversion_factor': 1,
        'units': iris.unit.Unit('K'),
        'standard_name': 'air_temperature',
        'req_standard_name': 'air_temperature',
        'req_long_name': 'Air Temperature',
        'var_name': 'ta'
    },
    'm01s01i232': {
        'conversion_factor': 1,
        'units': iris.unit.Unit('K s-1'),
        'standard_name': 'tendency_of_air_temperature_due_to_shortwave_heating',
        'req_standard_name': 'tendency_of_air_temperature_due_to_shortwave_heating',
        'req_long_name': 'Shortwave Heating Rate',
        'var_name': 'tntsw'
    },
    'm01s02i232': {
        'conversion_factor': 1,
        'units': iris.unit.Unit('K s-1'),
        'standard_name': 'tendency_of_air_temperature_due_to_longwave_heating',
        'req_standard_name': 'tendency_of_air_temperature_due_to_longwave_heating',
        'req_long_name': 'Longwave Heating Rate',
        'var_name': 'tntlw'
    },
    'm01s34i146': {
        'conversion_factor': 360.0,
        'units': iris.unit.Unit('year'),
        'standard_name': 'age_of_stratospheric_air',
        'req_standard_name': 'age_of_stratospheric_air',
        'req_long_name': 'Alternate Stratospheric Age of Air',
        'var_name': 'altaoa',
        'valid_range': (0.0, 50.0),
        'comment': 'Model output is in days, and so data is converted to years by dividing by conversion_factor'
    },
    'm01s34i049': {
        'conversion_factor': 1.5188,
        'units': iris.unit.Unit('mole mole-1'),
        'standard_name': 'mass_fraction_of_nitrous_oxide_in_air',
        'req_standard_name': 'mole_fraction_of_nitrous_oxide_in_air',
        'req_long_name': 'N2O Volume Mixing Ratio',
        'var_name': 'vmrn2o'
    },
    'm01s34i009': {
        'conversion_factor': 0.5523,
        'units': iris.unit.Unit('mole mole-1'),
        'standard_name': 'mass_fraction_of_methane_in_air',
        'req_standard_name': 'mole_fraction_of_methane_in_air',
        'req_long_name': 'CH4 Volume Mixing Ratio',
        'var_name': 'vmrch4'
    },
    'm01s02i052': {
        'conversion_factor': 1.5188,
        'standard_name': 'mass_fraction_of_carbon_dioxide_in_air',
        'req_standard_name': 'mole_fraction_of_carbon_dioxide_in_air',
        'req_long_name': 'CO2 Volume Mixing Ratio',
        'var_name': 'vmrco2'
    },
    'm01s34i154': {
        'conversion_factor': 1.2604,
        'units': iris.unit.Unit('mole mole-1'),
        'standard_name': 'mass_fraction_of_hydrogen_chloride_in_air',
        'req_standard_name': 'mole_fraction_of_hydrogen_chloride_in_air',
        'req_long_name': 'HCl Volume Mixing Ratio',
        'var_name': 'vmrhcl'
    },
    'm01s34i010': {
        'conversion_factor': 0.9665,
        'units': iris.unit.Unit('mole mole-1'),
        'standard_name': 'mass_fraction_of_carbon_monoxide_in_air',
        'req_standard_name': 'mole_fraction_of_carbon_monoxide_in_air',
        'req_long_name': 'CO Volume Mixing Ratio',
        'var_name': 'vmrco',
        'valid_range': (0.0, 1.0)
    },
    'm01s34i1052': {
        'conversion_factor': 1.588,
        'units': iris.unit.Unit('mole mole-1'),
        'standard_name': 'mass_fraction_of_nitrogen_dioxide_in_air',
        'req_standard_name': 'mole_fraction_of_nitrogen_dioxide_in_air',
        'req_long_name': 'NO2 Volume Mixing Ratio',
        'var_name': 'vmrno2'
    },
    'm01s34i002': {
        'conversion_factor': 1.036,
        'units': iris.unit.Unit('mole mole-1'),
        'standard_name': 'mass_fraction_of_nitrogen_monoxide_in_air',
        'req_standard_name': 'mole_fraction_of_nitrogen_monoxide_in_air',
        'req_long_name': 'NO Volume Mixing Ratio',
        'var_name': 'vmrno'
    },
    'm01s34i052': {
        'conversion_factor': 2.7970,
        'units': iris.unit.Unit('mole mole-1'),
        'standard_name': 'mass_fraction_of_hydrogen_bromide_in_air',
        'req_standard_name': 'mole_fraction_of_hydrogen_bromide_in_air',
        'req_long_name': 'HBr Volume Mixing Ratio',
        'var_name': 'vmrhbr',
        'valid_range': (0.0, 1.0)
    },
    'm01s00i265': {
        'conversion_factor': 0.01,
        'units': iris.unit.Unit('%'),
        'standard_name': 'cloud_area_fraction_in_atmosphere_layer',
        'req_standard_name': 'cloud_area_fraction',
        'req_long_name': 'Total Cloud Fraction',
        'var_name': 'clt',
        'valid_range': (0.0, 101.0)
    },
    'm01s34i301': {
        'conversion_factor': 'Grid box volume',
        'units': iris.unit.Unit('mole m-3 s-1'),
        'standard_name': 'tendency_of_mole_concentration_of_ozone_due_to_chemical_production_by_HO2_plus_NO',
        'req_standard_name': 'tendency_of_mole_concentration_of_ozone_due_to_chemical_production_by_HO2_plus_NO',
        'req_long_name': 'Chemical Production Rate of O3 via HO2+NO',
        'var_name': 'prodo3viaho2'
    },
    'm01s05i216': {
        'conversion_factor': 1,
        'units': iris.unit.Unit('kg m-2 s-1'),
        'standard_name': 'precipitation_flux',
        'req_standard_name': 'precipitation_flux',
        'req_long_name': 'Precipitation',
        'var_name': 'pr',
        'comment': 'At surface; includes both liquid and solid phases from all types of clouds (both large-scale and convective)',
        'valid_range': (0.0, 0.1)
    },
    'm01s00i409': {
        'conversion_factor': 1,
        'units': iris.unit.Unit('Pa'),
        'standard_name': 'surface_air_pressure',
        'req_standard_name': 'surface_air_pressure',
        'req_long_name': 'Surface Air Pressure',
        'var_name': 'ps',
        'valid_range': (0, 1000000),
        'comment': 'Surface pressure (not mean sea-level pressure), 2-D field to calculate the 3-D pressure field from hybrid coordinates'
    },
    'm01s30i451': {
        'conversion_factor': 1,
        'units': iris.unit.Unit('Pa'),
        'standard_name': 'tropopause_air_pressure',
        'req_standard_name': 'tropopause_air_pressure',
        'req_long_name': 'Tropopause Air Pressure',
        'var_name': 'ptp',
        'valid_range': (0, 100000),
        'comment': '2D monthly mean thermal tropopause calculated using WMO tropopause definition on 3d temperature'
    },
    'm01s03i332': {
        'conversion_factor': 1,
        'units': iris.unit.Unit('W m-2'),
        'standard_name': 'toa_outgoing_longwave_flux',
        'req_standard_name': 'toa_outgoing_longwave_flux',
        'req_long_name': 'TOA Outgoing Longwave Radiation',
        'var_name': 'rlut',
        'valid_range': (-0.1, 10000),
        'comment': 'At the top of the atmosphere (to be compared with satellite measurements)'
    },
    'm01s02i206': {
        'conversion_factor': 1,
        'units': iris.unit.Unit('W m-2'),
        'standard_name': 'toa_outgoing_longwave_flux_assuming_clear_sky',
        'req_standard_name': 'toa_outgoing_longwave_flux_assuming_clear_sky',
        'req_long_name': 'TOA Outgoing Clear-Sky Longwave Radiation',
        'var_name': 'rlutcs',
        'valid_range': (-0.1, 10000),
    },
    'm01s01i208': {
        'conversion_factor': 1,
        'units': iris.unit.Unit('W m-2'),
        'standard_name': 'toa_outgoing_shortwave_flux',
        'req_standard_name': 'toa_outgoing_shortwave_flux',
        'req_long_name': 'TOA Outgoing Shortwave Radiation',
        'var_name': 'rsut',
        'valid_range': (-0.1, 10000),
        'comment': 'At the top of the atmosphere'
    },
    'm01s01i209': {
        'conversion_factor': 1,
        'units': iris.unit.Unit('W m-2'),
        'standard_name': 'toa_outgoing_shortwave_flux_assuming_clear_sky',
        'req_standard_name': 'toa_outgoing_shortwave_flux_assuming_clear_sky',
        'req_long_name': 'TOA Outgoing Clear-Sky Shortwave Radiation',
        'var_name': 'rsutcs',
        'valid_range': (-0.1, 10000),
    },
    'm01s30i452': {
        'conversion_factor': 1,
        'units': iris.unit.Unit('K'),
        'standard_name': 'tropopause_air_temperature',
        'req_standard_name': 'tropopause_air_temperature',
        'req_long_name': 'Tropopause Air Temperature',
        'var_name': 'tatp',
        'valid_range': (0, 400),
        'comment': '2D monthly mean thermal tropopause calculated using WMO tropopause definition on 3d temperature'
    },
    'm01s34i172': {
        'conversion_factor': 1,
        'units': iris.unit.Unit('DU'),
        'standard_name': 'equivalent_thickness_at_stp_of_atmosphere_ozone_content',
        'req_standard_name': 'equivalent_thickness_at_stp_of_atmosphere_ozone_content',
        'req_long_name': 'Total Ozone Column',
        'var_name': 'toz',
        'valid_range': (0, 5000),
        'comment': 'Total ozone column in DU'
    },
    'm01s00i002': {
        'conversion_factor': 1,
        'units': iris.unit.Unit('m s-1'),
        'standard_name': 'eastward_wind',
        'req_standard_name': 'eastward_wind',
        'req_long_name': 'Eastward Wind',
        'var_name': 'ua',
        'valid_range': (-1000, 1000),
    },
    'm01s00i003': {
        'conversion_factor': 1,
        'units': iris.unit.Unit('m s-1'),
        'standard_name': 'northward_wind',
        'req_standard_name': 'northward_wind',
        'req_long_name': 'Northward Wind',
        'var_name': 'va',
        'valid_range': (-1000, 1000),
    },
    'm01s00i010': {
        'conversion_factor': 0.6213,
        'units': iris.unit.Unit('mole mole-1'),
        'standard_name': 'mole_fraction_of_water_vapor_in_air',
        'req_standard_name': 'mole_fraction_of_water_vapor_in_air',
        'req_long_name': 'Water Vapour Volume Mixing Ratio',
        'var_name': 'vmrh2o',
        'valid_range': (0, 1),
    },
    'm01s34i007': {
        'conversion_factor': 2.175,
        'units': iris.unit.Unit('mole mole-1'),
        'standard_name': 'mole_fraction_of_nitric_acid_in_air',
        'req_standard_name': 'mole_fraction_of_nitric_acid_in_air',
        'req_long_name': 'HNO3 Volume Mixing Ratio',
        'var_name': 'vmrhno3',
        'valid_range': (0, 1),
    },
    'm01s16i201': {
        'conversion_factor': 1,
        'units': iris.unit.Unit('m'),
        'standard_name': 'geopotential_height',
        'req_standard_name': 'geopotential_height',
        'req_long_name': 'Geopotential Height',
        'var_name': 'zg',
        'valid_range': (0, 500000),
    },
    'm01s30i453': {
        'conversion_factor': 1,
        'units': iris.unit.Unit('m'),
        'standard_name': 'tropopause_altitude',
        'req_standard_name': 'tropopause_altitude',
        'req_long_name': 'Tropopause Altitude',
        'var_name': 'ztp',
        'valid_range': (0, 40000),
        'comment': '2D monthly mean thermal tropopause calculated using WMO tropopause definition on 3d temperature'
    }
}
