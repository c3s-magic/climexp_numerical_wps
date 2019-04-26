Climate Explorer WPS service
===============================

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
   :target: http://climexp_numerical_wps.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/maartenplieger/climexp_numerical_wps.svg?branch=master
   :target: https://travis-ci.org/maartenplieger/climexp_numerical_wps
   :alt: Travis Build

.. image:: https://img.shields.io/github/license/maartenplieger/climexp_numerical_wps.svg
    :target: https://github.com/maartenplieger/climexp_numerical_wps/blob/master/LICENSE.txt
    :alt: GitHub license

.. image:: https://badges.gitter.im/bird-house/birdhouse.svg
    :target: https://gitter.im/bird-house/birdhouse?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
    :alt: Join the chat at https://gitter.im/bird-house/birdhouse


Climate Explorer WPS service (the bird)
  *Climate Explorer WPS service is a bird ...*

A Web Processing Service for Climate Data Analysis.

* Free software: Apache Software License 2.0
* Documentation: https://climexp-numerical-wps.readthedocs.io. (TBD)

```
docker build -t climexp_numerical_wps .
docker run -it -p 5000:5000 -v /home/c3smagic/data:/data climexp_numerical_wps


Credits
-------

This package was created with Cookiecutter_ and the `bird-house/cookiecutter-birdhouse`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`bird-house/cookiecutter-birdhouse`: https://github.com/bird-house/cookiecutter-birdhouse
