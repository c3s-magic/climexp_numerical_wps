# Dillinger

[![Build Status](https://travis-ci.org/c3s-magic/climexp_numerical_wps.svg?branch=master)](https://travis-ci.org/c3s-magic/climexp_numerical_wps)

[![License](https://img.shields.io/github/license/c3s-magic/climexp_numerical_wps.svg)](https://img.shields.io/github/license/c3s-magic/climexp_numerical_wps.svg)

Climate Explorer WPS service (the bird)
  *Climate Explorer WPS service is a bird ...*

A Web Processing Service for Climate Data Analysis.

* Free software: Apache Software License 2.0
* Documentation: https://climexp-numerical-wps.readthedocs.io. (TBD)


### To get an instance running with test data:
```
# Obtain test data:
mkdir ./data/
wget "http://opendap.knmi.nl/knmi/thredds/fileServer/climate_explorer/nino3.nc" -O ./data/nino3.nc
wget "http://opendap.knmi.nl/knmi/thredds/fileServer/climate_explorer/cru_ts3.22.1901.2013.pre.dat.nc" -O ./data/cru_ts3.22.1901.2013.pre.dat.nc

# Build
docker build -t climexp_numerical_wps .

# Start
docker run -it -p 5000:5000 -v `pwd`/data:/data climexp_numerical_wps
```

Credits
-------

This package was created with Cookiecutter_ and the `bird-house/cookiecutter-birdhouse`_ project template.

* Cookiecutter: https://github.com/audreyr/cookiecutter
* `bird-house/cookiecutter-birdhouse`: https://github.com/bird-house/cookiecutter-birdhouse
