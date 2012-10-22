Apps and Ideas Extension
========================

DEPRECATED
----------

The ckanext-apps extension is deprecated, it has been replaced by the
`Related Items <http://docs.ckan.org/en/latest/apps-ideas.html>`_ feature in
CKAN core. Tools have been added to this repository to migrate a ckanext-apps
deployment to CKAN Related Items:

1. Update your version of ckanext-apps to the latest commit on the master
   branch and run ``python setup.py develop`` in the ckanext-apps dir.

2. Use the ``ckanext-apps-migrate dump`` command to dump your ckanext-apps
   database tables to a JSON file. You should run the command from the
   ckanext-apps directory. For example::

     ckanext-apps-migrate -c deployment.ini dump > related.json

3. Use the ``ckanext-apps-migrate load`` command to load the dumped
   ckanext-apps data into your CKAN database as Related Items. Again, run the
   command from the ckanext-apps directory. For example::

     ckanext-apps-migrate -c deployment.ini load related.json

   You should now see your applications and ideas as Related Items in CKAN.
   For example, browse to ``/apps`` to see the Related Dashboard. However,
   the images for your related applications will not appear yet.

4. Use the ``ckanext-apps-scraper.py`` included with ckanext-apps to scrape the
   images for your related applications from your site running ckanext-apps.
   Follow the instructions in ``ckanext-apps-scraper.py``.

5. Add an extra public directory to your site (using the ``extra_public_paths``
   setting in your ini file). Inside the extra public directory create a
   directory called ``migrated_application_images``. Move the image files
   downloaded by the scraper into this directory.

   Restart the webserver. You should now see the images for your related
   applications on the related dashboard.

6. Disable the ckanext-apps extension by deleting it from the
   ``ckan.plugins =`` line in your ini file and restarting the web server.

----

The Apps and Ideas extension for CKAN adds functionality to associate apps
and ideas to datasets in your CKAN instance.

Requirement(s)
--------------

If using the Ubuntu 10.04 LTS appliance "package installation" method (Option 
1 in the documentation), you'll need to install python-imaging, e.g.

	sudo apt-get install python-imaging

Installation and Activation
---------------------------

To install the plugin, enter your virtualenv and load the source::


    (ckan)$ pip install -e git+https://github.com/okfn/ckanext-apps#egg=ckanext-apps

This will also register a plugin entry point, so you now should be 
able to add the following to your CKAN .ini file::


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
