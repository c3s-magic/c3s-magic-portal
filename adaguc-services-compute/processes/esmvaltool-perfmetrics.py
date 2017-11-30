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
                            abstract="Creates a report comparing models using ESMValTool (takes about 30 minutes).",
                            grassLocation=False)

	model_names = ['None', 'ACCESS1-0', 'ACCESS1-3', 'bcc-csm1-1', 'EC-EARTH', 'MIROC5']

        self.model1 = self.addLiteralInput(identifier="model1",
                                               title="Model 1",
                                               type="String",
                                               abstract="Model name",
                                               minOccurs=1,
                                               maxOccurs=1,
                                               default='ACCESS1-0',
                                               allowedValues=model_names)
        self.model2 = self.addLiteralInput(identifier="model2",
                                               title="Model 2",
                                               type="String",
                                               abstract="Model name",
                                               minOccurs=1,
                                               maxOccurs=1,
                                               default='ACCESS1-3',
                                               allowedValues=model_names)
        self.model3 = self.addLiteralInput(identifier="model3",
                                               title="Model 3",
                                               type="String",
                                               abstract="Model name",
                                               minOccurs=1,
                                               maxOccurs=1,
                                               allowedValues=model_names)
        self.model4 = self.addLiteralInput(identifier="model4",
                                               title="Model 4",
                                               type="String",
                                               abstract="Model name",
                                               minOccurs=1,
                                               maxOccurs=1,
                                               allowedValues=model_names)

	self.variable = self.addLiteralInput(identifier="variable",
                                              title="Variable",
                                              type="String",
                                              default="tas",
                                              minOccurs=1,
                                              maxOccurs=1)

	self.period = self.addLiteralInput(identifier="period",
                                              title="Period of the data",
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


        self.startYear = self.addLiteralInput(identifier="startYear",
                                              title="First year data used in plot",
                                              type="Integer",
                                              default=2003,
                                              minOccurs=1,
                                              maxOccurs=1)

        self.endYear = self.addLiteralInput(identifier="endYear",
                                            title="Last year data used in plot",
                                            type="Integer",
                                            default=2005,
                                            minOccurs=1,
                                            maxOccurs=1)

        self.opendapURL = self.addLiteralOutput(identifier="opendapURL",
                                                title="opendapURL",
                                                type="String", )

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
	    if value != 'None':
	        models.append(value)

	variable = self.variable.getValue()
	period = self.period.getValue()
	experiment = self.experiment.getValue()
	start_year = self.startYear.getValue()
        end_year = self.endYear.getValue()
 	ensemble_member = self.ensemble_member.getValue()

        logging.debug("models %s, variable %s, period %s, experiment %s, ensemble_member %s, start_year %s, end_year %s" % (models, variable, period, experiment, ensemble_member, start_year, end_year))

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
	    model_descriptions.append('CMIP5_ETHZ %s %s %s %s %s %s @{MODELPATH}/ETHZ_CMIP5/' % ( model, period, experiment, ensemble_member, start_year, end_year))

        self.status.set("setting up namelist for esmvaltool", 10)

        logging.debug("model descriptions now %s" % model_descriptions)
        logging.debug("variable %s" % variable)

        #create esmvaltool config (using template)
        environment = Environment(loader=FileSystemLoader('/namelists'))
                                  #autoescape=select_autoescape(['html', 'xml']))

        template = environment.get_template('namelist_demo.xml')

        generated_namelist = template.render(models=model_descriptions, variable=variable, work_dir=output_folder_path)

        logging.debug("template output = %s" % generated_namelist)

        #write generated namelist to file

        namelist_path = output_folder_path + "/" + 'namelist_demo.xml'

        namelist_fd = open(namelist_path, 'w')
        namelist_fd.write(generated_namelist)
        namelist_fd.close()

        #run esmvaltool command

        self.status.set("running esmvaltool", 20)

        os.chdir('/src/ESMValTool')

        self.cmd(['python', 'main.py', namelist_path])

        #grep output from output folder

        self.status.set("processing output", 90)

        output_image = glob.glob(output_folder_path + "/tsline/*.png").pop()

        logging.debug("output image path is %s" % output_image)

#        rel_output_image = os.path.relpath(output_image, output_folder_path)
#        plot_url = output_folder_url + "/" + rel_output_image

        self.plot.setValue(output_image)

        #KNMI WPS Specific Set output

        output_nc = glob.glob(output_folder_path + "/tsline/*.nc").pop()

        rel_output_nc = os.path.relpath(output_nc, output_folder_path)

        url = output_folder_url + "/" + rel_output_nc

        self.opendapURL.setValue(url);
        self.status.set("ready", 100);
