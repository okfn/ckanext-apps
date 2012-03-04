Apps and Ideas Extension
========================

The Apps and Ideas extension for CKAN adds functionality to associate apps
and ideas to datasets in your CKAN instance.

Installation and Activation
---------------------------

To install the plugin, enter your virtualenv and load the source::

::

    (ckan)$ pip install -e hg+https://bitbucket.org/okfn/ckanext-community#egg=ckanext-community

This will also register a plugin entry point, so you now should be 
able to add the following to your CKAN .ini file::

::

    ckan.plugins = community <other-plugins>
 
After you clear your cache and reload the site, the Comunity plugin
and should be available at http://myckaninstance/apps and http://myckaninstance/ideas

Developers
----------
You can run the test suite for ckanext-community from the ckan directory, the tests
for ckanext-community require nose and mock

::

    (ckan)$ pip install nose mock
    (ckan)$ nosetests -x path/to/ckanext-community/tests --ckan
