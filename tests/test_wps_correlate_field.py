import pytest

from pywps import Service
from pywps.tests import client_for, assert_response_success

from .common import get_output
from climexp_numerical_wps.processes.correlate_field import CorrelateField


def test_wps_correlate_field():
    client = client_for(Service(processes=[CorrelateField()]))
    datainputs = "netcdf_field=cru_ts3.22.1901.2013.pre.dat.nc;"
    datainputs += "netcdf_timeseries=nino3.nc;months=1:12;averaging_method=ave;lag=3;time_frequency=mon"
    resp = client.get(
        "?service=WPS&request=Execute&version=1.0.0&identifier=correlate_field&datainputs={}".format(
            datainputs))
    assert_response_success(resp)
    assert get_output(resp.xml) == {'data': '', 'success': 'False'}
