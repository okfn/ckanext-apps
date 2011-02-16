from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-community',
	version=version,
	description="Apps and Ideas submissions and browsing.",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='CKAN',
	author_email='CKAN',
	url='http://',
	license='mit',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.community'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
    [ckan.plugins]
	# Add plugins here, eg
	community=ckanext.community:Community
	""",
)
