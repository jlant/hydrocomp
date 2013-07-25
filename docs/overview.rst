Overview
===========

**hydrocomp** is a project that contains python modules that compare timeseries output from a model of 
a particular parameter (i.e. discharge) with an observed timeseries of the same parameter and compute
differences and statitics between modeled and observed hydrologic parameters. For example, the model
timeseries can be a rainfall-runoff model output of estimated discharge and the observed timeseries can 
be an USGS NWIS data file that contains discharge as a hydrologic parameter.

The following are the statistics calculated:

	* Nash-Sutcliffe
	
	* R Squared Coefficient
	
	* Mean Squared Error
	
	* Absolute Error
	
	* Relative Error
	
	* Percent Error
	
	* Percent Difference

Details
-------

*hydrocomp.py* is a module that contains functions to calculate, print, and plot comparision 
data and statitics.

In the *hydrocomp.py* module, *main()* prompts user for observed and model files. Processes 
each file, prints information, and plots data and statistics. Information is printed to the 
screen. Plots are saved to a directory called 'figs' which is created in the same directory as 
the data file. Currently, if an NWIS data file is selected as the observed file a log file called 
'nwis_error.log' is created if any errors are found in the data file.

*nwispy.py* is a module that contains functions to read, print, and plot data from an USGS NWIS
data file. The NWIS data file can be either a daily or instantaneous data file. The data file 
can contain any number of parameters; i.e. discharge, gage height, temperature, sediement 
concentration, etc.

	USGS NWIS data files can be found at: 

		http://waterdata.usgs.gov/nwis/rt

*statistics.py* is a module that contains functions to calculate all the statistics.

*helpers.py* is a module that currently contains functions to subset dates and find common date 
ranges between the model and observed data files.

*water.py* is a module that reads output from an application called WATER (gui wrapper around a 
Kentucky modified version of the rainfall-runoff model called Topmodel.

Author
------

Jeremiah Lant

jlant@usgs.gov

