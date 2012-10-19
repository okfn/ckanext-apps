#!/usr/bin/env python
"""
A script to download all the application images from a CKAN site running the
ckanext-apps extension.

You need access to the site's database to get the IDs of all the images.

Get a file containing a list of your ckanext-apps image IDs from your
PostgreSQL database with this command:

    psql -d {DATABASE} -h {HOST} -U {USER} -c 'SELECT id FROM application_image;' -o {FILENAME} -t

Replace {DATABASE}, {HOST}, {USER} and {FILENAME} with your database name,
the hostname of the machine your database server is running on, your database
username, and the filename to write to. Example:

    psql -d pdeu -h dbserver -U pdeu -c 'SELECT id FROM application_image;' -o image_ids -t

Then feed the image IDs file to this scraper script with this command:

    ./ckanext-apps-scraper.py {BASE_URL} {FILENAME}

where {BASE_URL} is the URL of your CKAN site and {FILENAME} is the filename
from the previous command, for example:

    ./ckanext-apps-scraper.py 'http://publicdata.eu/' image_ids

"""
import sys
import commands
base_url = sys.argv[1]
if not base_url.endswith('/'):
    base_url = base_url + '/'
for image_id in open(sys.argv[2], 'r').readlines():
    stripped = image_id.strip()
    if not stripped:
        continue
    url = "{base_url}app/image/{image_id}".format(base_url=base_url,
            image_id=stripped)
    cmd = "wget -nc '{0}'".format(url)
    status, output = commands.getstatusoutput(cmd)
    print output
