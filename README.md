# Web Processing Service for KNMI Climate explorer functions

[![Build Status](https://travis-ci.org/c3s-magic/climexp_numerical_wps.svg?branch=master)](https://travis-ci.org/c3s-magic/climexp_numerical_wps)

[![License](https://img.shields.io/github/license/c3s-magic/climexp_numerical_wps.svg)](https://img.shields.io/github/license/c3s-magic/climexp_numerical_wps.svg)


Climate Explorer WPS service is a Web Processing Service for Climate Data Analysis. This repository contains the code to use the KNMI climate explorer via a Web Processing Service. This code is a WPS wrapper around the KNMI climate explorer software available at https://github.com/c3s-magic/climexp_numerical

* Free software: Apache Software License 2.0
* Documentation: https://climexp-numerical-wps.readthedocs.io. (TBD)


### Which functions from climate explorer are already available via the WPS?

1) Correlatefield: This is a tool to correlate a field series to a point series to give fields of correlation coefficients, probabilities that these are significant, and the fit coefficients a, b and their errors.

### To get an docker container running with test data:
```
# Check this repository out and cd into the folder.
# Obtain test data:
mkdir ./data/
wget "http://opendap.knmi.nl/knmi/thredds/fileServer/climate_explorer/nino3.nc" -O ./data/nino3.nc
wget "http://opendap.knmi.nl/knmi/thredds/fileServer/climate_explorer/cru_ts3.22.1901.2013.pre.dat.nc" -O ./data/cru_ts3.22.1901.2013.pre.dat.nc

# Build
docker build -t climexp_numerical_wps .

# Start
docker run -it -p 5000:5000 -v `pwd`/data:/data climexp_numerical_wps
```

### Use the instance via a WPS client like birdy

Credits
-------

This package was created with `Cookiecutter` and the `bird-house/cookiecutter-birdhouse` project template.

* `Cookiecutter`: https://github.com/audreyr/cookiecutter
* `bird-house/cookiecutter-birdhouse`: https://github.com/bird-house/cookiecutter-birdhouse
