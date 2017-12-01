"""
../wps.py?request=execute
&service=wps
&version=1.0.0
&identifier=esmvaltool-perfmetrics
&status=true
&storeExecuteResponse=true


"""
import datetime

import shutil

import netCDF4
import urlparse

from pywps.Process import WPSProcess
import os
import logging
from jinja2 import FileSystemLoader, Environment,select_autoescape
import glob


class Process(WPSProcess):
    def __init__(self):
        # init process
        WPSProcess.__init__(self,
                            identifier="esmvaltool-perfmetrics",  # the same as the file name
                            version="1.0",
                            title="Model comparison report",
                            storeSupported="True",
                            statusSupported="True",
                            abstract="Creates a (sample of a) performance metrics report comparing models using ESMValTool.",
                            grassLocation=False)

	model_names = ['', 'None', 'bcc-csm1-1', 'GFDL-ESM2G', 'MPI-ESM-LR', 'MPI-ESM-MR']

        self.model1 = self.addLiteralInput(identifier="model1",
                                               title="Model 1",
                                               type="String",
                                               abstract="Model name",
                                               minOccurs=1,
                                               maxOccurs=1,
                                               default='bcc-csm1-1',
                                               allowedValues=model_names)
        self.model2 = self.addLiteralInput(identifier="model2",
                                               title="Model 2",
                                               type="String",
                                               abstract="Model name",
                                               minOccurs=1,
                                               maxOccurs=1,
                                               default='GFDL-ESM2G',
                                               allowedValues=model_names)
        self.model3 = self.addLiteralInput(identifier="model3",
                                               title="Model 3",
                                               type="String",
                                               abstract="Model name",
                                               minOccurs=1,
                                               maxOccurs=1,
                                               default='MPI-ESM-LR',
                                               allowedValues=model_names)
        self.model4 = self.addLiteralInput(identifier="model4",
                                               title="Model 4",
                                               type="String",
                                               abstract="Model name",
                                               minOccurs=1,
                                               maxOccurs=1,
                                               default='MPI-ESM-MR',
                                               allowedValues=model_names)

	self.variable = self.addLiteralInput(identifier="variable",
                                              title="Variable",
                                              type="String",
                                              default="ta",
                                              minOccurs=1,
                                              maxOccurs=1)

	self.mip = self.addLiteralInput(identifier="mip",
                                              title="MIP of the data",
                                              type="String",
                                              default="Amon",
                                              minOccurs=1,
                                              maxOccurs=1)

	self.experiment = self.addLiteralInput(identifier="experiment",
                                              title="Experiment of the data",
                                              type="String",
                                              default="historical",
                                              minOccurs=1,
                                              maxOccurs=1)

	self.ensemble_member = self.addLiteralInput(identifier="ensemble_member",
                                              title="Ensemble member of the data",
                                              type="String",
                                              default="r1i1p1",
                                              minOccurs=1,
                                              maxOccurs=1)


        self.start_year = self.addLiteralInput(identifier="start_year",
                                              title="First year data used in plot",
                                              type="Integer",
                                              default=2001,
                                              minOccurs=1,
                                              maxOccurs=1)

        self.end_year = self.addLiteralInput(identifier="end_year",
                                            title="Last year data used in plot",
                                            type="Integer",
                                            default=2002,
                                            minOccurs=1,
                                            maxOccurs=1)

        # self.opendapURL = self.addLiteralOutput(identifier="opendapURL",
        #                                         title="opendapURL",
        #                                         type="String", )

	self.plot = self.addComplexOutput(identifier = "plot",
		     title = "TimeseriesPlot",
		     formats = [
			 {"mimeType":"image/png"}
		     ])

    def execute(self):
        self.status.set("starting", 0)

        #print some debugging info

	models = []

	model_values = [self.model1.getValue(), self.model2.getValue(), self.model3.getValue(), self.model4.getValue()]

	for value in model_values:
	    if value != 'None' and value != '':
	        models.append(value)

	variable = self.variable.getValue()
	mip = self.mip.getValue()
	experiment = self.experiment.getValue()
	start_year = self.start_year.getValue()
        end_year = self.end_year.getValue()
 	ensemble_member = self.ensemble_member.getValue()

        logging.debug("models %s, variable %s, mip %s, experiment %s, ensemble_member %s, start_year %s, end_year %s" % (models, variable, mip, experiment, ensemble_member, start_year, end_year))

	# This does not work atm.
        # This allows the NetCDF library to find the users credentials (X509 cert)
        # Set current working directory to user HOME dir
        os.chdir(os.environ['HOME'])

        # Create output folder name
        output_folder_name = "WPS_" + self.identifier + "_" + datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")

        logging.debug(os.environ['POF_OUTPUT_PATH'])

        #OpenDAP Url prefix (hosted by portal)
        output_folder_url = os.environ['POF_OUTPUT_URL'] + output_folder_name

        #Filesystem output path
        output_folder_path = os.path.join(os.environ['POF_OUTPUT_PATH'], output_folder_name)

        logging.debug("output folder path is %s" % output_folder_path)

        #Create output directory
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        #copy input files to scratch (in correct folders for esmvaltool)

        #next, copy input netcdf to a location esmvaltool expects

        # example cmpi5 esgf link
        # http://esgf-data1.ceda.ac.uk/thredds/dodsC/esg_dataroot/cmip5/output1/CSIRO-BOM/ACCESS1-0/historical/mon/atmos/Amon/r1i1p1/v1/tas/tas_Amon_ACCESS1-0_historical_r1i1p1_185001-200512.nc

        # esmvaltool data folder example
        # ETHZ_CMIP5/historical/Amon/ta/bcc-csm1-1/r1i1p1/ta_Amon_bcc-csm1-1_historical_r1i1p1_200001-200212.nc


        	#description = <model> SOME DESCRIPTION FIELDS HERE </model>

        model_descriptions = []
	for model in models:
	    model_descriptions.append('- {name: %s, project: CMIP5, mip: %s, exp: %s, ensemble: %s, start_year: %s, end_year: %s}' % (model, mip, experiment,ensemble_member, start_year, end_year))

        self.status.set("setting up namelist for esmvaltool", 10)

        logging.debug("model descriptions now %s" % model_descriptions)
        logging.debug("variable %s" % variable)

        #create esmvaltool config (using template)
        environment = Environment(loader=FileSystemLoader('/config'))
                                  #autoescape=select_autoescape(['html', 'xml']))

        template = environment.get_template('namelist_perfmetrics_CMIP5_template.yml')

        generated_namelist = template.render(models=model_descriptions, variable=variable, start_year=start_year, end_year=end_year)

        logging.debug("template output = %s" % generated_namelist) 


        #write generated namelist to file

        namelist_path = output_folder_path + "/" + 'namelist_demo.yml'

        namelist_fd = open(namelist_path, 'w')
        namelist_fd.write(generated_namelist)
        namelist_fd.close()


        template = environment.get_template('config-user-template.yml')

        generated_config = template.render(output_folder_path=output_folder_path)

        logging.debug("config template output = %s" % generated_config)

        config_path = output_folder_path + "/" + 'config.yml'

        config_fd = open(config_path, 'w')
        config_fd.write(generated_config)
        config_fd.close()

        #run esmvaltool command

        os.environ['PYTHONIOENCODING'] = 'utf-8'

        self.status.set("running esmvaltool", 20)

        os.chdir('/src/ESMValTool')


        self.cmd(['python', 'esmvaltool/main.py', '-c', config_path, '-n', namelist_path])

        #grep output from output folder

        self.status.set("processing output", 90)

        #output_image = glob.glob(output_folder_path + "/tsline/*.png").pop()
        output_image = glob.glob(output_folder_path + "/plot/*_namelist_demo/perfmetrics_main/*.png").pop()

        self.cmd(['mogrify', '-trim', '-bordercolor', 'white', '-border', '10x10', output_image])

        logging.debug("output image path is %s" % output_image)

#        rel_output_image = os.path.relpath(output_image, output_folder_path)
#        plot_url = output_folder_url + "/" + rel_output_image

        self.plot.setValue(output_image)

        #KNMI WPS Specific Set output

        output_nc = glob.glob(output_folder_path + "/work/*_namelist_demo/perfmetrics_main/*.nc").pop()

        rel_output_nc = os.path.relpath(output_nc, output_folder_path)

        url = output_folder_url + "/" + rel_output_nc

        #self.opendapURL.setValue(url);
        self.status.set("ready", 100);
