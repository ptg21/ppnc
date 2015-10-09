Ppnc
====

Ppnc is a collection of python scripts that have been used to extract pp fields 
to cf-netCDF for submission to the CCMI archive.

The code makes extensive use of Iris: 

- https://github.com/SciTools/iris

Requirements
------------

The following python modules are used:

- iris
- numpy

F2PY is used to create the pressureconv modules

- http://cens.ioc.ee/projects/f2py2e/

```
f2py -c -m pressureconv pressureconv.f90
```

Support
-------

These scripts are provided in the hope that someone will find them useful. Due 
to time restrictions, support for using these scripts is not available.

Example Usage
-------------

For usage run:

```python ppnc.py --help```

Edit some of the files under config to fit your particular use case.

- config/global_attrs.py # defines some of the metadata that is written
- config/req_data.py # defines your stashes, conversion factors and units
- config/tweakables.py # defines your fillvalue and pressure levels

An example invocation of ppnc is as follows:

    python ppnc.py -j $JID # Model JobID \
                   -t "203001-203912" # Temporal Subset \
                   -p /path/to/output/files \ 
                   -s $STASH # STASH to restrict to \ 
                   --pgrid THETA # Pressure Grid \
                   -f /path/to/pp/files/*.pp # pp files to use

The submit_scripts folder contains some example bash scripts to create and 
submit jobs on a system running LSF.

Copyright and licence
---------------------

This file is part of ppnc.

ppnc  Copyright (C) 2015  University of Cambridge

Ppnc is free software: you can redistribute it and/or modify it under the terms 
of the GNU Lesser General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version.

Ppnc is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along 
with ppnc.  If not, see <http://www.gnu.org/licenses/>.
