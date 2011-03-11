import json
from ckan.lib.base import BaseController, c, g, request, \
                          response, session, render, config, abort
from ..dictization import *

class ApiController(BaseController):
                
    def application_details(self, id=None):
        return json.dumps(application_information(application_name=id))

