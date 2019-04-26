from pywps import FORMATS, Process, LiteralInput, LiteralOutput, ComplexOutput
from pywps.app.Common import Metadata


from climexp_numerical import climexp_numerical
import os
from .utils import default_outputs
import logging
LOGGER = logging.getLogger("PYWPS")


class CorrelateField(Process):
    """A nice process saying 'CorrelateField'."""
    def __init__(self):
        inputs = [
            LiteralInput('netcdf_field', 'NetCDF field',
                         abstract='The gridded NetCDF file',
                         keywords=['netcdf', 'grid'],
                         default='cru_ts3.22.1901.2013.pre.dat.nc',
                         data_type='string'),
            LiteralInput('netcdf_timeseries', 'NetCDF timeseries',
                         abstract='The gridded NetCDF file',
                         keywords=['netcdf', 'timeseries'],
                         default='nino3.nc',
                         data_type='string'),
            LiteralInput('months', 'The months to select',
                         abstract='The gridded NetCDF file',
                         keywords=['time', 'selection'],
                         default='1:12',
                         data_type='string'),
            LiteralInput('averaging_method', 'Averaging method',
                         abstract='The averaging method',
                         keywords=['averaging'],
                         default='ave',
                         data_type='string'),
            LiteralInput('lag', 'Lag',
                         abstract='The lag in months',
                         keywords=['netcdf', 'grid'],
                         default='3',
                         data_type='string'),
            LiteralInput('time_frequency', 'Time frequency',
                         abstract='The time time_frequency',
                         keywords=['netcdf', 'grid'],
                         default='mon',
                         data_type='string')]
        outputs = [
             ComplexOutput('data', 'Data',
                          abstract='Generated output NetCDF data of climate explorer correlate_field.',
                          as_reference=True,
                          supported_formats=[FORMATS.NETCDF]),
             *default_outputs()]

        super(CorrelateField, self).__init__(
            self._handler,
            identifier='correlate_field',
            title='CorrelateField',
            abstract='Correlates a time series with other user-defined time series, '
                     'as well as with system-defined time series of the same temporal resolution',
            keywords=['CorrelateField', 'demo'],
            metadata=[
                Metadata('PyWPS', 'https://pywps.org/'),
                Metadata('Birdhouse', 'http://bird-house.github.io/'),
                Metadata('PyWPS Demo', 'https://pywps-demo.readthedocs.io/en/latest/'),
                Metadata('Emu: PyWPS examples', 'https://emu.readthedocs.io/en/latest/'),
            ],
            version='1.5',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )


    def checkValidInputFile(self, inputfile):
      if ("./" in inputfile):
        raise ValueError("The inputfile is not valid")
      return
      
    def _handler(self, request, response):
        response.update_status("starting ...", 0)

        def callback(message):
          self.lastMessage = message
          response.update_status("%s" % message, 50)
        
        try:
          climexp = climexp_numerical.ClimExp()
          climexpBuild = os.getenv("CLIMATE_EXPLORER_BUILD", "../build")
          climexp.setClimExpHome(climexpBuild)
          
          os.chdir(self.workdir);
          
          self.checkValidInputFile(request.inputs["netcdf_field"][0].data)
          self.checkValidInputFile(request.inputs["netcdf_timeseries"][0].data)
          inputfile_netcdf_field = os.path.join("/data", request.inputs["netcdf_field"][0].data);
          inputfile_netcdf_timeseries = os.path.join("/data", request.inputs["netcdf_timeseries"][0].data);
          
          outputfile = os.path.join(self.workdir,"correlate_field.nc");
          
          settings = {
            'observation': inputfile_netcdf_field,
            'model': inputfile_netcdf_timeseries,
            'frequency': request.inputs["time_frequency"][0].data,
            'timeselection': request.inputs["months"][0].data,
            'averaging': request.inputs["averaging_method"][0].data,
            'lag': request.inputs["lag"][0].data,
            'out': outputfile,
            'callback': callback
          }
          status = climexp.correlatefield(** settings)
          if status != 0:
            LOGGER.error(self.lastMessage)
            LOGGER.error(settings)
            
          if not os.path.isfile(outputfile):
            LOGGER.error("Outputfile %s is not written" % outputfile);
            status = 1
            
          response.outputs['success'].data = (status == 0)
          
          if status == 0:
            response.outputs['data'].output_format = FORMATS.NETCDF
            response.outputs['data'].file = outputfile
          #print("Status = %d" % status);        
          response.update_status("done.", 100)
          return response

        except Exception as e:
          LOGGER.error(str(e));
          response.update_status("Failed %s" % str(e), 100)
          response.outputs['success'].data = False
          #return response
          raise(e)
