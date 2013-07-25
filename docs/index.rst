.. hydrocomp documentation master file, created by
   sphinx-quickstart on Thu Jul 25 14:53:17 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to hydrocomp's documentation!
=====================================

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

Contents:

.. toctree::
   :maxdepth: 2

   overview.rst
   code.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

