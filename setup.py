from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-apps',
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
	namespace_packages=['ckanext', 'ckanext.apps'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
        "PIL>=1.1.6",
	],
	entry_points=\
	"""
    [ckan.plugins]
	apps=ckanext.apps.plugin:Apps
	""",
)
