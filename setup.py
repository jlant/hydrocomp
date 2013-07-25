try:
	from setuptools import setup, find_packages
except ImportError:
	from distutils.core import setup

with open('README.md') as f:    
	readme = f.read()

with open('LICENSE.txt') as f:    
	license = f.read()	
	
setup(
	name = 'hydrocomp',
	version = '0.0.1',
	description = 'Compares timeseries output from a model of a particular parameter (i.e. discharge) with an observed timeseries of the same parameter.'
	long_description = readme,
	author = 'Jeremiah Lant',
	author_email = 'jlant@usgs.gov',
	url = 'https://github.com/jlant-usgs/hydrocomp',
	license = license,
	packages = find_packages()
	)
